import uuid
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Cluster(Base):
    __tablename__ = "clusters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    signature: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    start_ts: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    end_ts: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    severity_max: Mapped[str] = mapped_column(String(16), nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=0)
    sample_messages: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    involved_sources: Mapped[str] = mapped_column(Text, nullable=False, default="[]")

    events: Mapped[list["UnifiedEvent"]] = relationship(back_populates="cluster")


class UnifiedEvent(Base):
    __tablename__ = "unified_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_type: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp_utc: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    entity: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    cluster_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("clusters.id"), nullable=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    cluster: Mapped[Cluster | None] = relationship(back_populates="events")


class DriftBaseline(Base):
    __tablename__ = "drift_baselines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    target_host: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_label: Mapped[str] = mapped_column(String(255), nullable=False)
    scan_type: Mapped[str] = mapped_column(String(16), nullable=False)
    ssh_session_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    paths: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    probes_enabled: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    fingerprint: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    scan_interval_seconds: Mapped[int] = mapped_column(Integer, default=300)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    snapshots: Mapped[list["DriftSnapshot"]] = relationship(back_populates="baseline", cascade="all, delete-orphan")


class DriftSnapshot(Base):
    __tablename__ = "drift_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    baseline_id: Mapped[str] = mapped_column(String(36), ForeignKey("drift_baselines.id"), nullable=False, index=True)
    fingerprint: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    drift_detected: Mapped[int] = mapped_column(Integer, default=0)
    drift_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(String(16), default="info")
    scanned_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), index=True)

    baseline: Mapped[DriftBaseline] = relationship(back_populates="snapshots")


class RvtoolsImport(Base):
    __tablename__ = "rvtools_imports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename: Mapped[str] = mapped_column(String(512), nullable=False)
    source_label: Mapped[str] = mapped_column(String(255), default="rvtools")
    imported_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), index=True)
    tab_counts: Mapped[str] = mapped_column(Text, default="{}")
    total_rows: Mapped[int] = mapped_column(Integer, default=0)
    findings_generated: Mapped[int] = mapped_column(Integer, default=0)

    rows: Mapped[list["RvtoolsRow"]] = relationship(back_populates="rvtools_import", cascade="all, delete-orphan")


class RvtoolsRow(Base):
    __tablename__ = "rvtools_rows"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    import_id: Mapped[str] = mapped_column(String(36), ForeignKey("rvtools_imports.id"), nullable=False, index=True)
    tab_name: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    row_index: Mapped[int] = mapped_column(Integer, nullable=False)
    entity_name: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    entity_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    row_data: Mapped[str] = mapped_column(Text, nullable=False)

    rvtools_import: Mapped[RvtoolsImport] = relationship(back_populates="rows")
