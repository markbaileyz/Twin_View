import json
from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import RvtoolsRow

router = APIRouter(prefix='/inventory', tags=['inventory'])


def _to_int(value, default=0):
    try:
        return int(float(value))
    except Exception:
        return default


def build_hierarchy(rows: list[dict]):
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for row in rows:
        dc = row.get('Datacenter') or row.get('DC') or 'Unknown-DC'
        cluster = row.get('Cluster') or 'Unknown-Cluster'
        host = row.get('Host') or 'Unknown-Host'
        vm_name = row.get('VM') or row.get('Name') or 'Unknown-VM'
        tree[dc][cluster][host].append(
            {
                'name': vm_name,
                'powerstate': row.get('Powerstate') or row.get('Power State') or 'unknown',
                'os': row.get('OS according to the configuration file') or row.get('OS') or 'unknown',
                'cpu': _to_int(row.get('CPUs') or row.get('vCPUs') or 0),
                'memory_mb': _to_int(row.get('Memory') or row.get('Memory MB') or 0),
                'entity_type': 'vm',
            }
        )

    dcs = []
    total_clusters = total_hosts = total_vms = 0
    for dc_name, clusters in sorted(tree.items()):
        cluster_nodes = []
        dc_hosts = dc_vms = 0
        for cluster_name, hosts in sorted(clusters.items()):
            host_nodes = []
            cluster_vms = 0
            for host_name, vms in sorted(hosts.items()):
                host_nodes.append({'name': host_name, 'vms': vms, 'vm_count': len(vms), 'entity_type': 'host'})
                cluster_vms += len(vms)
            cluster_nodes.append({'name': cluster_name, 'hosts': host_nodes, 'host_count': len(host_nodes), 'vm_count': cluster_vms, 'entity_type': 'cluster'})
            dc_hosts += len(host_nodes)
            dc_vms += cluster_vms

        total_clusters += len(cluster_nodes)
        total_hosts += dc_hosts
        total_vms += dc_vms
        dcs.append({'name': dc_name, 'clusters': cluster_nodes, 'cluster_count': len(cluster_nodes), 'host_count': dc_hosts, 'vm_count': dc_vms, 'entity_type': 'datacenter'})

    return dcs, total_clusters, total_hosts, total_vms


@router.get('/hierarchy/{import_id}')
def hierarchy(import_id: str, db: Session = Depends(get_db)):
    raw_rows = db.execute(select(RvtoolsRow).where(RvtoolsRow.import_id == import_id, RvtoolsRow.tab_name.in_(["vInfo", "tabvInfo"]))).scalars().all()
    parsed = []
    for row in raw_rows:
        try:
            parsed.append(json.loads(row.row_data))
        except Exception:
            continue
    datacenters, total_clusters, total_hosts, total_vms = build_hierarchy(parsed)
    return {
        'import_id': import_id,
        'datacenters': datacenters,
        'total_datacenters': len(datacenters),
        'total_clusters': total_clusters,
        'total_hosts': total_hosts,
        'total_vms': total_vms,
    }


@router.get('/flat/{import_id}')
def flat(import_id: str, entity_type: str | None = None, tab_name: str | None = None, limit: int = 200, offset: int = 0, db: Session = Depends(get_db)):
    query = select(RvtoolsRow).where(RvtoolsRow.import_id == import_id)
    if entity_type:
        query = query.where(RvtoolsRow.entity_type == entity_type)
    if tab_name:
        query = query.where(RvtoolsRow.tab_name == tab_name)
    rows = db.execute(query.order_by(RvtoolsRow.row_index).offset(offset).limit(limit)).scalars().all()

    total_q = select(func.count()).select_from(RvtoolsRow).where(RvtoolsRow.import_id == import_id)
    if entity_type:
        total_q = total_q.where(RvtoolsRow.entity_type == entity_type)
    if tab_name:
        total_q = total_q.where(RvtoolsRow.tab_name == tab_name)
    total = db.scalar(total_q) or 0

    items = []
    for row in rows:
        try:
            parsed = json.loads(row.row_data)
        except Exception:
            parsed = {}
        items.append({
            'id': row.id,
            'tab_name': row.tab_name,
            'entity_name': row.entity_name,
            'entity_type': row.entity_type,
            'row_data': parsed,
        })

    return {'items': items, 'total': total, 'offset': offset, 'limit': limit}
