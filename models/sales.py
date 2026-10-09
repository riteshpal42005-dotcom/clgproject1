
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class Sales(Base):
    __tablename__ = "sales"

    id = Column(String, primary_key=True, index=True)
    business_id = Column(
        String,
        ForeignKey("businesses.id"),
        nullable=False,
        index=True
    )
    invoice_number = Column(String, nullable=False)
    sale_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False, default="completed")
    total_amount = Column(Numeric(12, 2), nullable=False, default=0)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
