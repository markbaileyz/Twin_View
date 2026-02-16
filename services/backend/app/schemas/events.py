from datetime import datetime
from pydantic import BaseModel


class UnifiedEventResponse(BaseModel):
    id: str
    source_type: str
    source_name: str
    timestamp_utc: datetime
    severity: str
    category: str
    message: str
    entity: str | None = None
    cluster_id: str | None = None


class EventsListResponse(BaseModel):
    events: list[UnifiedEventResponse]
    total: int
