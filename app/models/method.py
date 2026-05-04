from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.domain.enums import MarketType, MethodStatus, PeriodType


class Method(Base):
    __tablename__ = "methods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    market: Mapped[MarketType] = mapped_column(String(50), nullable=False)
    period: Mapped[PeriodType] = mapped_column(String(50), nullable=False)
    status: Mapped[MethodStatus] = mapped_column(
        String(50),
        nullable=False,
        default=MethodStatus.ACTIVE,
        server_default=MethodStatus.ACTIVE.value,
    )
    minute_start: Mapped[int] = mapped_column(Integer, nullable=False)
    minute_end: Mapped[int] = mapped_column(Integer, nullable=False)
    score_filter: Mapped[str | None] = mapped_column(String(20), nullable=True)
    min_dangerous_attacks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_total_shots: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_shots_on_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_corners: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_red_cards: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    min_odd: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    max_odd: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    historical_hit_rate: Mapped[Decimal] = mapped_column(Numeric(8, 6), nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    fair_odd: Mapped[Decimal] = mapped_column(Numeric(18, 10), nullable=False)
    min_edge: Mapped[Decimal] = mapped_column(
        Numeric(10, 4),
        nullable=False,
        default=Decimal("0.08"),
        server_default="0.08",
    )
    stake_units: Mapped[Decimal] = mapped_column(
        Numeric(10, 4),
        nullable=False,
        default=Decimal("0.5"),
        server_default="0.5",
    )
    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="zeus",
        server_default="zeus",
    )
    zeus_query: Mapped[str | None] = mapped_column(Text, nullable=True)
    scanner_condition: Mapped[str | None] = mapped_column(Text, nullable=True)
    entry_rule: Mapped[str | None] = mapped_column(Text, nullable=True)
    validation_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
