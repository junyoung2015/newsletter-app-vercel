from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Users(Base):
	__tablename__ = "users"

	id: Mapped[str] = mapped_column(String(36), primary_key=True)
	email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
	password_hash: Mapped[str] = mapped_column(String(64), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

