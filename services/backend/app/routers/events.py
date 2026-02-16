from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import UnifiedEvent

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def list_events(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    q = select(UnifiedEvent).order_by(UnifiedEvent.timestamp_utc.desc()).offset(offset).limit(limit)
    events = db.execute(q).scalars().all()
    total = db.scalar(select(func.count()).select_from(UnifiedEvent))
    return {"events": [{"id": e.id, "source_type": e.source_type, "source_name": e.source_name, "timestamp_utc": e.timestamp_utc, "severity": e.severity, "category": e.category, "message": e.message, "entity": e.entity, "cluster_id": e.cluster_id} for e in events], "total": total}
