import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import DriftBaseline, DriftSnapshot

router = APIRouter(prefix="/drift", tags=["drift"])


class DriftTargetCreate(BaseModel):
    target_host: str
    target_label: str
    scan_type: str
    ssh_session_id: str | None = None
    paths: list[str]
    probes_enabled: list[str]
    scan_interval_seconds: int = 300


@router.post('/targets')
def create_target(req: DriftTargetCreate, db: Session = Depends(get_db)):
    baseline = DriftBaseline(
        target_host=req.target_host,
        target_label=req.target_label,
        scan_type=req.scan_type,
        ssh_session_id=req.ssh_session_id,
        paths=json.dumps(req.paths),
        probes_enabled=json.dumps(req.probes_enabled),
        fingerprint=json.dumps({}),
        scan_interval_seconds=req.scan_interval_seconds,
    )
    db.add(baseline)
    db.commit()
    db.refresh(baseline)
    return {"status": "created", "baseline": {"id": baseline.id, "target_host": baseline.target_host, "target_label": baseline.target_label}}


@router.get('/targets')
def list_targets(db: Session = Depends(get_db)):
    rows = db.execute(select(DriftBaseline).order_by(DriftBaseline.created_at.desc())).scalars().all()
    return {"targets": [{"id": r.id, "target_host": r.target_host, "target_label": r.target_label, "scan_type": r.scan_type} for r in rows], "total": len(rows)}


@router.get('/targets/{baseline_id}')
def get_target(baseline_id: str, db: Session = Depends(get_db)):
    row = db.get(DriftBaseline, baseline_id)
    if not row:
        raise HTTPException(status_code=404, detail="baseline not found")
    return {"id": row.id, "target_host": row.target_host, "target_label": row.target_label, "scan_type": row.scan_type}


@router.delete('/targets/{baseline_id}')
def delete_target(baseline_id: str, db: Session = Depends(get_db)):
    row = db.get(DriftBaseline, baseline_id)
    if row:
        db.delete(row)
        db.commit()
    return {"status": "deleted", "baseline_id": baseline_id}


@router.post('/targets/{baseline_id}/rebaseline')
def rebaseline(baseline_id: str, db: Session = Depends(get_db)):
    row = db.get(DriftBaseline, baseline_id)
    if not row:
        raise HTTPException(status_code=404, detail="baseline not found")
    return {"status": "rebaselined", "baseline": {"id": row.id, "target_label": row.target_label}}


@router.get('/targets/{baseline_id}/snapshots')
def snapshots(baseline_id: str, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    rows = db.execute(
        select(DriftSnapshot).where(DriftSnapshot.baseline_id == baseline_id).order_by(DriftSnapshot.scanned_at.desc()).offset(offset).limit(limit)
    ).scalars().all()
    total = db.scalar(select(func.count()).select_from(DriftSnapshot).where(DriftSnapshot.baseline_id == baseline_id)) or 0
    return {"snapshots": [{"id": s.id, "baseline_id": s.baseline_id, "drift_detected": bool(s.drift_detected), "severity": s.severity} for s in rows], "total": total}


@router.post('/scan')
def force_scan(body: dict):
    return {"status": "accepted", "result": {"baseline_id": body.get("baseline_id"), "queued": True}}


@router.get('/probes')
def probes():
    return {
        "probes": {
            "dir_sizes": {"description": "Total byte size of directory", "path_independent": False, "command_template": "du -sb {path}"},
            "file_counts": {"description": "Count files", "path_independent": False, "command_template": "find {path} -type f | wc -l"},
            "service_fingerprint": {"description": "Service state checksum", "path_independent": True, "command_template": "systemctl list-units --type=service"},
        }
    }
