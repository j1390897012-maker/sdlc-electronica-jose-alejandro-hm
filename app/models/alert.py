"""Modelo ORM del recurso Alert (alerta)."""

from datetime import UTC, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class AlertModel(Base):
    """Mapeo de la tabla `alerts`."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"),
        index=True,
    )

    reading_id: Mapped[int] = mapped_column(
        ForeignKey("readings.id"),
        index=True,
    )

    value: Mapped[float]

    threshold: Mapped[float]

    status: Mapped[str] = mapped_column(
        String(20),
        default="open",
    )

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
    )