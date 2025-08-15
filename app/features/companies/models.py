from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from uuid import UUID, uuid4
from datetime import datetime

from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True),
        primary_key=True,
        default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    domain: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    projects = relationship(
        "Project",
        back_populates="company", cascade="all, delete-orphan"
    )

    users = relationship(
        "User",
        back_populates="company", cascade="all, delete-orphan"
    )

    memberships = relationship(
        "ProjectMembership",
        back_populates="company", cascade="all, delete-orphan"
    )
