from datetime import datetime
from . import db
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, VARCHAR, func, Boolean, DateTime


class User(db.Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(300), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    role: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)