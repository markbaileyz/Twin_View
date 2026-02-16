import asyncio
from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.correlator.clustering import process_event
from app.db.models import Base, Cluster, UnifiedEvent


def test_process_event_creates_cluster_and_event():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        asyncio.run(
            process_event(
                {
                    "source_type": "demo",
                    "source_name": "demo-generator",
                    "severity": "warning",
                    "category": "alarm",
                    "message": "Host esxi-01 not responding",
                    "entity": "esxi-01",
                    "timestamp_utc": datetime.now(timezone.utc),
                },
                db,
            )
        )
        assert db.query(UnifiedEvent).count() == 1
        assert db.query(Cluster).count() == 1
    finally:
        db.close()
