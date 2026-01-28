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
            ("Martillo de Carpintero", "Herramientas Manuales", 15.99, 50, "Martillo resistente de acero forjado con mango ergonómico.", "https://images.unsplash.com/photo-1586864387967-d02ef85d93e8?w=500&auto=format&fit=crop&q=60"),
            ("Destornillador Phillips", "Herramientas Manuales", 5.50, 100, "Punta magnética y mango antideslizante.", "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=500&auto=format&fit=crop&q=60"),
            ("Llave Inglesa Ajustable", "Herramientas Manuales", 12.00, 30, "Apertura máxima de 30mm, acero cromado.", "https://images.unsplash.com/photo-1632212938186-b49f9976378c?w=500&auto=format&fit=crop&q=60"),
            
            # Eléctricas
            ("Taladro Percutor 500W", "Herramientas Eléctricas", 85.00, 20, "Potente taladro con función de percusión para concreto.", "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=500&auto=format&fit=crop&q=60"),
            ("Sierra Circular", "Herramientas Eléctricas", 120.00, 15, "Cortes precisos en madera y metal ligero.", "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=500&auto=format&fit=crop&q=60"),
            ("Lijadora Orbital", "Herramientas Eléctricas", 45.00, 25, "Acabados suaves, incluye bolsa recolectora de polvo.", "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=500&auto=format&fit=crop&q=60"),
            
            # Construcción
            ("Saco de Cemento 50kg", "Construcción", 8.50, 200, "Cemento de alta resistencia para estructuras.", "https://images.unsplash.com/photo-1518709388487-19cbbf454924?w=500&auto=format&fit=crop&q=60"),
            ("Ladrillo Rojo Estándar", "Construcción", 0.45, 5000, "Ladrillo cocido para muros resistentes.", "https://images.unsplash.com/photo-1517646331032-9e8563c520a1?w=500&auto=format&fit=crop&q=60"),
            
            # Seguridad
            ("Casco de Seguridad", "Seguridad", 14.50, 60, "Protección certificada color amarillo.", "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=500&auto=format&fit=crop&q=60"),
            ("Guantes de Trabajo", "Seguridad", 3.99, 150, "Reforzados con cuero para manejo de cargas.", "https://images.unsplash.com/photo-1616423664033-68dd2667d028?w=500&auto=format&fit=crop&q=60"),
            
            # Plomería
            ("Tubo PVC 3m", "Plomería", 7.00, 100, "Tubo de media pulgada para agua potable.", "https://images.unsplash.com/photo-1595116712399-281df68102f4?w=500&auto=format&fit=crop&q=60"),
            ("Llave de Paso", "Plomería", 9.25, 40, "Bronce fundido, cierre esférico.", "https://images.unsplash.com/photo-1585664811087-47f65f68a2bf?w=500&auto=format&fit=crop&q=60")
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
        print("Seeding complete!")

if __name__ == "__main__":
    seed()
