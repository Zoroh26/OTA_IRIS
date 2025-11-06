from datetime import UTC, datetime
from sqlalchemy import CheckConstraint, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class CustomerType(Base):
    __tablename__ = "customer_type"

    customer_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    type_name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True)
    created_by: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Active")
    description: Mapped[str] = mapped_column(
        Text, nullable=False, default="No description provided")
    created_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default_factory=lambda: datetime.now(UTC)
    )

    __table_args__ = (
        CheckConstraint("LENGTH(TRIM(type_name)) >= 2",
                        name="chk_type_name_length"),
        CheckConstraint("LENGTH(TRIM(description)) BETWEEN 2 AND 500",
                        name="chk_description_length"),
        CheckConstraint(
            "type_name ~ '^[A-Za-z0-9 \\-_]+$'", name="chk_type_name_format"),
        CheckConstraint("created_by > 0", name="chk_created_by_positive"),
        CheckConstraint("updated_by > 0", name="chk_updated_by_positive"),
        CheckConstraint("updated_at >= created_at",
                        name="chk_updated_after_created"),
        CheckConstraint("status IN ('Active', 'Inactive')",
                        name="chk_status_values"),
    )
