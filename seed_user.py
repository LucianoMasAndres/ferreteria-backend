import sys
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)

def seed_user():
    print("Seeding user...")
    with engine.connect() as conn:
        if not result.fetchone():
            conn.execute(
                text("""
                    INSERT INTO clients (name, lastname, email, password, telephone) 
                    VALUES ('Admin', 'User', 'admin@ferreteria.com', 'password123', '12345678')
                """)
            )
            conn.commit()
            print("Created user: admin@ferreteria.com / password123")
        else:
            conn.execute(
                text("UPDATE clients SET password = 'password123' WHERE email = 'admin@ferreteria.com'")
            )
            conn.commit()
            print("Updated user password to: password123")

if __name__ == "__main__":
    seed_user()
