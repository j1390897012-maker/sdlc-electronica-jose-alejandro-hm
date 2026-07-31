from datetime import UTC, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.sensor import SensorModel


class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"),
        index=True,
    )

    value: Mapped[float]

    unit: Mapped[str] = mapped_column(
        String(20),
    )

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
    )

    sensor: Mapped["SensorModel"] = relationship(
        back_populates="readings",
    )