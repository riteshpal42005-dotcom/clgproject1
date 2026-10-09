
from sqlalchemy import (
    Column, String, Integer, Numeric, ForeignKey,
    UniqueConstraint
)
from core.database import Base


class Products(Base):
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint(
            "business_id", "sku",
            name="uq_products_business_sku"
        ),
    )

    id = Column(String, primary_key=True, index=True)
    business_id = Column(
        String,
        ForeignKey("businesses.id"),
        nullable=False,
        index=True,
    )
    sku = Column(String, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    unit_price = Column(Numeric(12, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    low_stock_threshold = Column(Integer, nullable=False, default=10)
