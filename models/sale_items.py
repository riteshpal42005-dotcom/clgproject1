
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from core.database import Base


class SaleItems(Base):
    __tablename__ = "sale_items"

    id = Column(String, primary_key=True, index=True)

    sale_id = Column(
        String,
        ForeignKey("sales.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    product_id = Column(
        String,
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
