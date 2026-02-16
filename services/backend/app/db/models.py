import uuid
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Cluster(Base):
    __tablename__ = "clusters"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    signature: Mapped[str] = mapped_column(String(16), index=True)
    start_ts: Mapped[DateTime] = mapped_column(DateTime, index=True)
    end_ts: Mapped[DateTime] = mapped_column(DateTime)
    severity_max: Mapped[str] = mapped_column(String(16))
    count: Mapped[int] = mapped_column(Integer, default=0)
    sample_messages: Mapped[str] = mapped_column(Text, default="[]")
    involved_sources: Mapped[str] = mapped_column(Text, default="[]")
    events: Mapped[list["UnifiedEvent"]] = relationship(back_populates="cluster")


class UnifiedEvent(Base):
    __tablename__ = "unified_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_type: Mapped[str] = mapped_column(String(16), index=True)
    source_name: Mapped[str] = mapped_column(String(255))
    timestamp_utc: Mapped[DateTime] = mapped_column(DateTime, index=True)
    severity: Mapped[str] = mapped_column(String(16), index=True)
    category: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(Text)
    entity: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    cluster_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("clusters.id"), index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    cluster: Mapped[Cluster | None] = relationship(back_populates="events")
