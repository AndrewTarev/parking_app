import asyncio
from datetime import datetime, timedelta
from typing import List

from sqlalchemy import ForeignKey, String, UniqueConstraint, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base import Base
from src.core.database.db_helper import db_helper


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    credit_card: Mapped[str] = mapped_column(String(50), nullable=False)
    car_number: Mapped[str] = mapped_column(String(10), nullable=False)

    parking: Mapped[List["Parking"]] = relationship(
        secondary="client_parking", back_populates="client"
    )

    __table_args__ = (UniqueConstraint("name", "surname"),)


class Parking(Base):
    __tablename__ = "parking"
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    opened: Mapped[bool] = mapped_column(nullable=False, default=True)
    count_places: Mapped[int] = mapped_column(nullable=False, default=10)
    count_available_places: Mapped[int] = mapped_column(nullable=False, default=10)

    client: Mapped[List["Client"]] = relationship(
        secondary="client_parking", back_populates="parking"
    )


class ClientParking(Base):
    __tablename__ = "client_parking"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client.id", ondelete="CASCADE"), nullable=False
    )
    parking_id: Mapped[int] = mapped_column(
        ForeignKey("parking.id", ondelete="CASCADE"), nullable=False
    )
    time_in: Mapped[datetime] = mapped_column(default=datetime.now())
    time_out: Mapped[datetime] = mapped_column(default=None, nullable=True)

    @hybrid_property
    def check_time_parking(self):
        if self.time_out is not None and self.time_in is not None:
            time_difference_seconds = (self.time_out - self.time_in).total_seconds()
            hours_difference = time_difference_seconds / 3600
            return hours_difference
        else:
            return None


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await db_helper.engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())
