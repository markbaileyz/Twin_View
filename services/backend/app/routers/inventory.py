from collections import defaultdict
from fastapi import APIRouter

router = APIRouter(prefix='/inventory', tags=['inventory'])


def build_hierarchy(rows: list[dict]):
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for row in rows:
        dc = row.get('Datacenter') or row.get('DC') or 'Unknown-DC'
        cl = row.get('Cluster') or 'Unknown-Cluster'
        host = row.get('Host') or 'Unknown-Host'
        vm = row.get('VM') or row.get('Name') or 'Unknown-VM'
        tree[dc][cl][host].append({'name': vm, 'powerstate': row.get('Powerstate', 'unknown'), 'os': row.get('OS according to the configuration file', 'unknown'), 'cpu': int(row.get('CPUs', 0) or 0), 'memory_mb': int(row.get('Memory', 0) or 0)})
    dcs = []
    for dc_name, clusters in sorted(tree.items()):
        cluster_nodes = []
        host_total = vm_total = 0
        for cl_name, hosts in sorted(clusters.items()):
            host_nodes = []
            c_vm = 0
            for h_name, vms in sorted(hosts.items()):
                c_vm += len(vms)
                host_nodes.append({'name': h_name, 'vms': vms, 'vm_count': len(vms), 'entity_type': 'host'})
            host_total += len(host_nodes)
            vm_total += c_vm
            cluster_nodes.append({'name': cl_name, 'hosts': host_nodes, 'host_count': len(host_nodes), 'vm_count': c_vm, 'entity_type': 'cluster'})
        dcs.append({'name': dc_name, 'clusters': cluster_nodes, 'cluster_count': len(cluster_nodes), 'host_count': host_total, 'vm_count': vm_total, 'entity_type': 'datacenter'})
    return dcs


@router.get('/hierarchy/{import_id}')
def hierarchy(import_id: str):
    return {'import_id': import_id, 'datacenters': [], 'total_datacenters': 0, 'total_clusters': 0, 'total_hosts': 0, 'total_vms': 0}
