
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from core.database import Base


class Businesses(Base):
    __tablename__ = "businesses"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
