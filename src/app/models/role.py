from datetime import UTC, datetime
from sqlalchemy import CheckConstraint, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Role(Base):
    __tablename__ = "role"

    role_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False)
    role_name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Active")
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, default_factory=lambda: datetime.now(UTC))

    __table_args__ = (
        CheckConstraint("LENGTH(TRIM(role_name)) >= 2",
                        name="chk_role_name_length"),
        CheckConstraint(
            "role_name ~ '^[A-Za-z0-9 \-_]+$'", name="chk_role_name_format"),
        CheckConstraint("status IN ('Active', 'Inactive')",
                        name="chk_status_values"),
    )
