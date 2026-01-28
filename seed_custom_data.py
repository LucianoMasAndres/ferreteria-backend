import sys
from sqlalchemy import create_engine, text

# Connection string
# Connection string
import os

# Connection string
# Check for DATABASE_URL (Render) or fall back to local dev
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://postgres:postgres@ecommerce_postgres_dev:5432/postgres")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def seed():
    print("Seeding database...")
    with engine.connect() as conn:
        # 1. Create Categories
        categories = [
            ("Herramientas Manuales", "Martillos, destornilladores y llaves"),
            ("Herramientas Eléctricas", "Taladros, sierras y lijadoras"),
            ("Construcción", "Cementos, yeso y materiales básicos"),
            ("Seguridad", "Cascos, guantes y protección"),
            ("Plomería", "Tubos, llaves y accesorios de baño")
        ]
        
        category_ids = {}
        
        for name, desc in categories:
            # Check if exists first to avoid dupes
            result = conn.execute(text("SELECT id_key FROM categories WHERE name = :name"), {"name": name})
            row = result.fetchone()
            if not row:
                result = conn.execute(
                    text("INSERT INTO categories (name) VALUES (:name) RETURNING id_key"),
                    {"name": name}
                )
                category_ids[name] = result.scalar()
                print(f"Created Category: {name}")
            else:
                category_ids[name] = row[0]
                print(f"Category exists: {name}")
            
        conn.commit()

        # 2. Create Products
        products = [
            # Manuales
            ("Martillo de Carpintero", "Herramientas Manuales", 15.99, 50, "Martillo resistente de acero forjado con mango ergonómico.", "https://placehold.co/600x400/orange/white?text=Martillo+Carpintero"),
            ("Destornillador Phillips", "Herramientas Manuales", 5.50, 100, "Punta magnética y mango antideslizante.", "https://placehold.co/600x400/orange/white?text=Destornillador+Phillips"),
            ("Llave Inglesa Ajustable", "Herramientas Manuales", 12.00, 30, "Apertura máxima de 30mm, acero cromado.", "https://placehold.co/600x400/orange/white?text=Llave+Inglesa"),
            
            # Eléctricas
            ("Taladro Percutor 500W", "Herramientas Eléctricas", 85.00, 20, "Potente taladro con función de percusión para concreto.", "https://placehold.co/600x400/333/orange?text=Taladro+Percutor"),
            ("Sierra Circular", "Herramientas Eléctricas", 120.00, 15, "Cortes precisos en madera y metal ligero.", "https://placehold.co/600x400/333/orange?text=Sierra+Circular"),
            ("Lijadora Orbital", "Herramientas Eléctricas", 45.00, 25, "Acabados suaves, incluye bolsa recolectora de polvo.", "https://placehold.co/600x400/333/orange?text=Lijadora+Orbital"),
            
            # Construcción
            ("Saco de Cemento 50kg", "Construcción", 8.50, 200, "Cemento de alta resistencia para estructuras.", "https://placehold.co/600x400/grey/white?text=Cemento+50kg"),
            ("Ladrillo Rojo Estándar", "Construcción", 0.45, 5000, "Ladrillo cocido para muros resistentes.", "https://placehold.co/600x400/red/white?text=Ladrillo+Rojo"),
            
            # Seguridad
            ("Casco de Seguridad", "Seguridad", 14.50, 60, "Protección certificada color amarillo.", "https://placehold.co/600x400/yellow/black?text=Casco+Seguridad"),
            ("Guantes de Trabajo", "Seguridad", 3.99, 150, "Reforzados con cuero para manejo de cargas.", "https://placehold.co/600x400/brown/white?text=Guantes+Trabajo"),
            
            # Plomería
            ("Tubo PVC 3m", "Plomería", 7.00, 100, "Tubo de media pulgada para agua potable.", "https://placehold.co/600x400/blue/white?text=Tubo+PVC"),
            ("Llave de Paso", "Plomería", 9.25, 40, "Bronce fundido, cierre esférico.", "https://placehold.co/600x400/gold/black?text=Llave+de+Paso")
        ]

        for name, cat_name, price, stock, desc, img in products:
            cat_id = category_ids.get(cat_name)
            if not cat_id:
                print(f"Skipping {name}, category not found")
                continue

            # Assuming 'name' is unique constraint or strictly checking for existence
            # Adjust query based on actual schema constraints if needed.
            # Here we just insert blindly for simplicity as table was empty, 
            # but let's check name to be safe in case of re-runs.
            # Check if exists
            result = conn.execute(text("SELECT id_key FROM products WHERE name = :name"), {"name": name})
            row = result.fetchone()
            
            if not row:
                conn.execute(
                    text("""
                        INSERT INTO products (name, price, stock, category_id, image_url) 
                        VALUES (:name, :price, :stock, :cat_id, :img)
                    """),
                    {"name": name, "price": price, "stock": stock, "cat_id": cat_id, "img": img}
                )
                print(f"Added Product: {name}")
            else:
                # Update image if missing
                conn.execute(
                    text("UPDATE products SET image_url = :img WHERE id_key = :id"),
                    {"img": img, "id": row[0]}
                )
                print(f"Updated Product Image: {name}")
                
        conn.commit()
        conn.commit()

        # 3. Create Admin User
        admin_email = "admin@ferreteria.com"
        result = conn.execute(text("SELECT id_key FROM clients WHERE email = :email"), {"email": admin_email})
        row = result.fetchone()

        if not row:
            conn.execute(
                text("""
                    INSERT INTO clients (name, lastname, email, password, telephone) 
                    VALUES (:name, :lastname, :email, :password, :telephone)
                """),
                {
                    "name": "Admin",
                    "lastname": "User",
                    "email": admin_email,
                    "password": "password123", # Plaintext as per controller logic
                    "telephone": "12345678"
                }
            )
            print(f"Created Admin User: {admin_email}")
        else:
            # Ensure password is correct
            conn.execute(
                text("UPDATE clients SET password = :password WHERE email = :email"),
                {"password": "password123", "email": admin_email}
            )
            print(f"Admin User exists. Password reset to: password123")
            
        conn.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    seed()
