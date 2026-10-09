from datetime import datetime
from decimal import Decimal


def parse_sale_date(value):
    """Convert a CSV date string into a Python datetime object."""
    if isinstance(value, datetime):
        return value
    value = str(value).strip()
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d")


def transform_products(raw_products: list[dict], business_id: str) -> list[dict]:
    transformed = []
    for row in raw_products:
        if not row.get("product_id"):
            continue
        transformed.append({
            "id": row["product_id"].strip(),
            "business_id": business_id,
            "sku": row["sku"].strip(),
            "name": row["name"].strip(),
            "category": (row.get("category") or "").strip() or None,
            "unit_price": Decimal(str(row["unit_price"]).strip()),
            "stock_quantity": int(str(row["stock_quantity"]).strip()),
            "low_stock_threshold": int(str(row["low_stock_threshold"]).strip()),
        })
    return transformed


def transform_sales_and_items(
    raw_sales: list[dict], raw_sale_items: list[dict], business_id: str
) -> tuple[list[dict], list[dict]]:
    # Calculate totals from sale items
    totals = {}
    transformed_items = []
    for row in raw_sale_items:
        if not row.get("sale_item_id"):
            continue
        sale_id = row["sale_id"].strip()
        quantity = int(str(row["quantity"]).strip())
        unit_price = Decimal(str(row["unit_price"]).strip())

        totals[sale_id] = totals.get(sale_id, Decimal("0.00")) + (quantity * unit_price)

        transformed_items.append({
            "id": row["sale_item_id"].strip(),
            "sale_id": sale_id,
            "product_id": row["product_id"].strip(),
            "quantity": quantity,
            "unit_price": unit_price,
        })

    transformed_sales = []
    for row in raw_sales:
        if not row.get("sale_id"):
            continue
        sale_id = row["sale_id"].strip()
        transformed_sales.append({
            "id": sale_id,
            "business_id": business_id,
            "invoice_number": row["invoice_number"].strip(),
            "sale_date": parse_sale_date(row["sale_date"]),
            "status": row.get("status", "completed").strip(),
            "total_amount": totals.get(sale_id, Decimal("0.00")),
        })

    return transformed_sales, transformed_items


def transform_all(raw_data: dict, business_id: str) -> dict:
    products = transform_products(raw_data["products"], business_id)
    sales, sale_items = transform_sales_and_items(
        raw_data["sales"], raw_data["sale_items"], business_id
    )
    return {
        "products": products,
        "sales": sales,
        "sale_items": sale_items,
    }
