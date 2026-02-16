import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.correlator.normalizer import compute_signature, normalize
from app.db.models import Cluster, UnifiedEvent
from app.ws.broadcaster import telemetry_broadcaster

SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2, "critical": 3}


def max_severity(a: str, b: str) -> str:
    return a if SEVERITY_ORDER.get(a, 0) >= SEVERITY_ORDER.get(b, 0) else b


async def process_event(event_data: dict, db: Session) -> UnifiedEvent:
    event_ts = event_data.get("timestamp_utc") or datetime.now(timezone.utc)
    event = UnifiedEvent(
        source_type=event_data["source_type"],
        source_name=event_data["source_name"],
        timestamp_utc=event_ts,
        severity=event_data["severity"],
        category=event_data["category"],
        message=event_data["message"],
        entity=event_data.get("entity"),
        raw_json=json.dumps(event_data.get("raw_json")) if event_data.get("raw_json") else None,
    )
    sig = compute_signature(event.category, normalize(event.message), event.entity, event.source_type)
    cutoff = event_ts - timedelta(minutes=settings.CLUSTER_WINDOW_MINUTES)
    cluster = db.execute(
        select(Cluster).where(Cluster.signature == sig, Cluster.start_ts >= cutoff, Cluster.count < settings.CLUSTER_MAX_EVENTS)
        .order_by(Cluster.start_ts.desc())
        .limit(1)
    ).scalar_one_or_none()

    if cluster:
        cluster.end_ts = event_ts
        cluster.count += 1
        cluster.severity_max = max_severity(cluster.severity_max, event.severity)
        samples = json.loads(cluster.sample_messages)
        if len(samples) < settings.CLUSTER_MAX_SAMPLES:
            samples.append(event.message)
            cluster.sample_messages = json.dumps(samples)
        sources = set(json.loads(cluster.involved_sources))
        sources.add(event.source_name)
        cluster.involved_sources = json.dumps(sorted(list(sources)))
    else:
        cluster = Cluster(
            signature=sig,
            start_ts=event_ts,
            end_ts=event_ts,
            severity_max=event.severity,
            count=1,
            sample_messages=json.dumps([event.message]),
            involved_sources=json.dumps([event.source_name]),
        )
        db.add(cluster)
        db.flush()

    event.cluster_id = cluster.id
    db.add(event)
    db.commit()
    db.refresh(event)

    await telemetry_broadcaster.broadcast({"type": "event", "data": {"id": event.id, "message": event.message, "severity": event.severity, "category": event.category, "source_type": event.source_type, "source_name": event.source_name, "timestamp_utc": str(event.timestamp_utc), "entity": event.entity, "cluster_id": event.cluster_id}})
    await telemetry_broadcaster.broadcast({"type": "cluster_update", "data": {"id": cluster.id, "signature": cluster.signature, "start_ts": str(cluster.start_ts), "end_ts": str(cluster.end_ts), "severity_max": cluster.severity_max, "count": cluster.count, "sample_messages": json.loads(cluster.sample_messages), "involved_sources": json.loads(cluster.involved_sources)}})
    return event
