from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db import Base


class ReadingModel(Base):

    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_id: Mapped[str] = mapped_column(index=True)

    value: Mapped[float]

    unit: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )