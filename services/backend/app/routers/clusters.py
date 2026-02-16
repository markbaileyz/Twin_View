import json
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import Cluster

router = APIRouter(prefix="/clusters", tags=["clusters"])


@router.get("")
def list_clusters(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    rows = db.execute(select(Cluster).order_by(Cluster.start_ts.desc()).offset(offset).limit(limit)).scalars().all()
    total = db.scalar(select(func.count()).select_from(Cluster))
    return {"clusters": [{"id": c.id, "signature": c.signature, "start_ts": c.start_ts, "end_ts": c.end_ts, "severity_max": c.severity_max, "count": c.count, "sample_messages": json.loads(c.sample_messages), "involved_sources": json.loads(c.involved_sources)} for c in rows], "total": total}
