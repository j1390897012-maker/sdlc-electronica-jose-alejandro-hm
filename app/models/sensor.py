from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.reading import ReadingModel


class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )
    sensor_type: Mapped[str] = mapped_column(String(50))
    unit: Mapped[str] = mapped_column(String(20))

    readings: Mapped[list["ReadingModel"]] = relationship(
        back_populates="sensor",
        cascade="all, delete-orphan",
    )