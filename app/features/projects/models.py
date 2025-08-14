from sqlalchemy import (
    ForeignKey, String, DateTime, 
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from uuid import UUID, uuid4

from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    company_id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="projects")

    memberships = relationship(
        "ProjectMembership",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class ProjectMembership(Base):
    __tablename__ = "project_memberships"

    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    company_id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="memberships")
    user = relationship("User", back_populates="memberships")
    company = relationship("Company", back_populates="memberships")

    __table_args__ = (
        UniqueConstraint("project_id", "user_id"),
    )