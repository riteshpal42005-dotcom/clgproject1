import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.database import Base, engine
from models import Businesses, Products, Sales, SaleItems
from etl_pipeline.extract import extract_all
from etl_pipeline.transform import transform_all
from etl_pipeline.load import load_data, BUSINESS_ID, BUSINESS_NAME


def run_etl():
    """Run full ETL workflow: Extract -> Transform -> Load."""
    print("\n[1/4] Ensuring database tables exist in Supabase...")
    Base.metadata.create_all(bind=engine)
    print("      Database tables verified.")

    print("\n[2/4] Extracting raw data from CSV files...")
    raw_data = extract_all()
    print(f"      Extracted {len(raw_data['products'])} products, "
          f"{len(raw_data['sales'])} sales, "
          f"{len(raw_data['sale_items'])} sale items.")

    print("\n[3/4] Transforming and validating data...")
    transformed_data = transform_all(raw_data, BUSINESS_ID)
    print("      Data transformation complete.")

    print("\n[4/4] Loading data into Supabase...")
    load_data(
        products_data=transformed_data["products"],
        sales_data=transformed_data["sales"],
        sale_items_data=transformed_data["sale_items"],
        business_id=BUSINESS_ID,
        business_name=BUSINESS_NAME,
    )
    print("\n ETL process completed successfully!\n")


if __name__ == "__main__":
    run_etl()
