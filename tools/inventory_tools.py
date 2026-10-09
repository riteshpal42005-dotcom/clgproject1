
from agents import function_tool
from sqlalchemy import select
from core.database import SessionLocal
from models import Products


@function_tool
def get_all_products() -> str:
    """Retrieve product names, prices, stock quantities,
    and low-stock thresholds for the current business."""

    with SessionLocal() as db:
        products = db.scalars(
            select(Products).order_by(Products.name)
        ).all()

        if not products:
            return "No products were found in the database."

        results = []

        for product in products:
            results.append(
                f"Product: {product.name}, "
                f"SKU: {product.sku}, "
                f"Price: {product.unit_price}, "
                f"Stock: {product.stock_quantity}, "
                f"Low-stock threshold: "
                f"{product.low_stock_threshold}"
            )

        return "\n".join(results)


@function_tool
def get_low_stock_products() -> str:
    """Retrieve products whose stock is at or below
    their configured low-stock threshold."""

    with SessionLocal() as db:
        products = db.scalars(
            select(Products).where(
                Products.stock_quantity
                <= Products.low_stock_threshold
            ).order_by(Products.stock_quantity)
        ).all()

        if not products:
            return "No low-stock products were found."

        return "\n".join(
            f"{p.name}: {p.stock_quantity} units remaining "
            f"(threshold: {p.low_stock_threshold})"
            for p in products
        )
