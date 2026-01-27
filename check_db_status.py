import sys
import os
from sqlalchemy import create_engine, inspect, text

# Add current dir to path to import backend modules if needed, 
# but for now we just want to check the DB connection.

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

def check_db():
    print(f"Connecting to {DATABASE_URL}...")
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        print("Successfully connected to the database!")
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print("\nExisting Tables:")
        if not tables:
            print("  [WARNING] No tables found! Migrations might not have run.")
        else:
            for table in tables:
                print(f"  - {table}")
                
            # Check for products
            if 'products' in tables:
                result = connection.execute(text("SELECT count(*) FROM products"))
                count = result.scalar()
                print(f"\nProduct Count: {count}")
            
    except Exception as e:
        print(f"\n[ERROR] Failed to connect: {e}")
        print("Make sure the Docker container 'ecommerce_postgres_dev' is running.")

if __name__ == "__main__":
    check_db()
