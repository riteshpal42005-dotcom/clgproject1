import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from core.database import SessionLocal
from models import Businesses, Products, Sales, SaleItems

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Default business for imported data
BUSINESS_ID = "business-001"
BUSINESS_NAME = "My Business"


def read_csv(filename: str) -> list[dict]:
    """Read a CSV file and return non-empty rows as dictionaries."""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    with file_path.open("r", newline="", encoding="utf-8-sig") as file:
        lines = [line for line in file if line.strip()]
        return list(csv.DictReader(lines))


def parse_sale_date(value):
    """Convert a CSV date into a Python datetime."""
    if isinstance(value, datetime):
        return value
    value = str(value).strip()

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d")


def load_data(products_data=None, sales_data=None, sale_items_data=None, business_id=BUSINESS_ID, business_name=BUSINESS_NAME):
    """Load products, sales, and sale_items data into the database."""
    if products_data is None:
        products_data = read_csv("products.csv")
    if sales_data is None:
        sales_data = read_csv("sales.csv")
    if sale_items_data is None:
        sale_items_data = read_csv("sale_items.csv")

    with SessionLocal() as db:
        try:
            # 1. Create or ensure business exists
            business = db.get(Businesses, business_id)

            if business is None:
                business = Businesses(
                    id=business_id,
                    name=business_name,
                )
                db.add(business)
                db.flush()

            # 2. Load products
            products_count = 0
            for row in products_data:
                product_id = row.get("id") or row.get("product_id")
                if not product_id:
                    continue
                product_id = str(product_id).strip()

                product = db.get(Products, product_id)

                values = {
                    "business_id": business_id,
                    "sku": str(row["sku"]).strip(),
                    "name": str(row["name"]).strip(),
                    "category": (row.get("category") or "").strip() or None,
                    "unit_price": Decimal(str(row["unit_price"])),
                    "stock_quantity": int(str(row["stock_quantity"])),
                    "low_stock_threshold": int(str(row["low_stock_threshold"])),
                }

                if product is None:
                    db.add(Products(id=product_id, **values))
                else:
                    for key, value in values.items():
                        setattr(product, key, value)
                products_count += 1

            db.flush()

            # 3. Calculate sale totals if not pre-calculated
            totals = {}
            for row in sale_items_data:
                sale_id = str(row["sale_id"]).strip()
                qty = int(str(row["quantity"]).strip())
                price = Decimal(str(row["unit_price"]).strip())
                totals[sale_id] = totals.get(sale_id, Decimal("0.00")) + (qty * price)

            # 4. Load sales
            sales_count = 0
            for row in sales_data:
                sale_id = row.get("id") or row.get("sale_id")
                if not sale_id:
                    continue
                sale_id = str(sale_id).strip()

                sale = db.get(Sales, sale_id)

                total_amount = row.get("total_amount")
                if total_amount is None:
                    total_amount = totals.get(sale_id, Decimal("0.00"))
                else:
                    total_amount = Decimal(str(total_amount))

                values = {
                    "business_id": business_id,
                    "invoice_number": str(row["invoice_number"]).strip(),
                    "sale_date": parse_sale_date(row["sale_date"]),
                    "status": str(row.get("status", "completed")).strip(),
                    "total_amount": total_amount,
                }

                if sale is None:
                    db.add(Sales(id=sale_id, **values))
                else:
                    for key, value in values.items():
                        setattr(sale, key, value)
                sales_count += 1

            db.flush()

            # 5. Load sale items
            items_count = 0
            for row in sale_items_data:
                item_id = row.get("id") or row.get("sale_item_id")
                if not item_id:
                    continue
                item_id = str(item_id).strip()

                item = db.get(SaleItems, item_id)

                values = {
                    "sale_id": str(row["sale_id"]).strip(),
                    "product_id": str(row["product_id"]).strip(),
                    "quantity": int(str(row["quantity"])),
                    "unit_price": Decimal(str(row["unit_price"])),
                }

                if item is None:
                    db.add(SaleItems(id=item_id, **values))
                else:
                    for key, value in values.items():
                        setattr(item, key, value)
                items_count += 1

            # Save all changes together
            db.commit()

            print("========================================")
            print("  ETL Pipeline: Data Loaded into Supabase")
            print("========================================")
            print(f"Business:             {business_name} ({business_id})")
            print(f"Products loaded:      {products_count}")
            print(f"Sales loaded:         {sales_count}")
            print(f"Sale items loaded:    {items_count}")
            print("Status:               SUCCESS")
            print("========================================")

        except Exception as err:
            db.rollback()
            print(f"Error during ETL loading: {err}")
            raise


if __name__ == "__main__":
    load_data()
