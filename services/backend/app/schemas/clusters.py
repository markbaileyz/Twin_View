from datetime import datetime
from pydantic import BaseModel


class ClusterResponse(BaseModel):
    id: str
    signature: str
    start_ts: datetime
    end_ts: datetime
    severity_max: str
    count: int
    sample_messages: list[str]
    involved_sources: list[str]


class ClustersListResponse(BaseModel):
    clusters: list[ClusterResponse]
    total: int
