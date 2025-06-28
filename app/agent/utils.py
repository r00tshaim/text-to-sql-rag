import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Define consistent DB path and helpers (create DB in current directory)
DB_FILE_PATH = "example.db"
DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_ecommerce_db():
    schema_statements = [
        "DROP TABLE IF EXISTS ProductReview;",
        "DROP TABLE IF EXISTS Offer;",
        "DROP TABLE IF EXISTS OrderItem;",
        "DROP TABLE IF EXISTS Orders;",
        "DROP TABLE IF EXISTS Product;",
        "DROP TABLE IF EXISTS User;",

        """
        CREATE TABLE User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            address TEXT
        );
        """,

        """
        CREATE TABLE Product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL
        );
        """,

        """
        CREATE TABLE Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            created_at TEXT,
            total REAL,
            FOREIGN KEY(user_id) REFERENCES User(id)
        );
        """,

        """
        CREATE TABLE OrderItem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY(order_id) REFERENCES Orders(id),
            FOREIGN KEY(product_id) REFERENCES Product(id)
        );
        """,

        """
        CREATE TABLE ProductReview (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            rating INTEGER,
            comment TEXT,
            FOREIGN KEY(user_id) REFERENCES User(id),
            FOREIGN KEY(product_id) REFERENCES Product(id)
        );
        """,

        """
        CREATE TABLE Offer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            description TEXT,
            discount_percentage REAL,
            valid_until TEXT,
            FOREIGN KEY(product_id) REFERENCES Product(id)
        );
        """
    ]

    data_statements = [
        # Users
        ("INSERT INTO User (name, email, address) VALUES (:name, :email, :address)", [
            {"name": "Alice", "email": "alice@example.com", "address": "123 Apple St"},
            {"name": "Bob", "email": "bob@example.com", "address": "456 Banana Ave"},
        ]),

        # Products
        ("INSERT INTO Product (name, category, price) VALUES (:name, :category, :price)", [
            {"name": "Laptop", "category": "Electronics", "price": 1000.0},
            {"name": "Headphones", "category": "Electronics", "price": 200.0},
            {"name": "Coffee Mug", "category": "Home", "price": 15.0},
        ]),

        # Orders
        ("INSERT INTO Orders (user_id, created_at, total) VALUES (:user_id, :created_at, :total)", [
            {"user_id": 1, "created_at": "2024-06-01", "total": 1215.0},
            {"user_id": 2, "created_at": "2024-06-02", "total": 215.0},
        ]),

        # Order Items
        ("INSERT INTO OrderItem (order_id, product_id, quantity, price) VALUES (:order_id, :product_id, :quantity, :price)", [
            {"order_id": 1, "product_id": 1, "quantity": 1, "price": 1000.0},
            {"order_id": 1, "product_id": 2, "quantity": 1, "price": 200.0},
            {"order_id": 1, "product_id": 3, "quantity": 1, "price": 15.0},
            {"order_id": 2, "product_id": 2, "quantity": 1, "price": 200.0},
            {"order_id": 2, "product_id": 3, "quantity": 1, "price": 15.0},
        ]),

        # Reviews
        ("INSERT INTO ProductReview (user_id, product_id, rating, comment) VALUES (:user_id, :product_id, :rating, :comment)", [
            {"user_id": 1, "product_id": 1, "rating": 5, "comment": "Amazing Laptop!"},
            {"user_id": 2, "product_id": 2, "rating": 4, "comment": "Great sound quality."},
        ]),

        # Offers
        ("INSERT INTO Offer (product_id, description, discount_percentage, valid_until) VALUES (:product_id, :description, :discount_percentage, :valid_until)", [
            {"product_id": 1, "description": "Summer Sale", "discount_percentage": 10.0, "valid_until": "2025-07-01"},
            {"product_id": 3, "description": "Buy 2 get 1 free", "discount_percentage": 33.3, "valid_until": "2025-06-30"},
        ]),
    ]

    with engine.begin() as conn:
        for stmt in schema_statements:
            conn.execute(text(stmt))

        for sql, records in data_statements:
            for record in records:
                conn.execute(text(sql), record)


def get_database_schema():
    inspector = inspect(engine)
    schema = []
    for table_name in inspector.get_table_names():
        table_info = f"Table: {table_name}\n"
        for column in inspector.get_columns(table_name):
            name = column["name"]
            dtype = str(column["type"])
            nullable = "NOT NULL" if not column["nullable"] else "NULLABLE"
            default = f"DEFAULT {column['default']}" if column['default'] is not None else ""
            primary = "Primary Key" if column.get("primary_key") else ""
            constraints = ", ".join(filter(None, [dtype, nullable, default, primary]))
            table_info += f"- {name}: {constraints}\n"

        foreign_keys = inspector.get_foreign_keys(table_name)
        for fk in foreign_keys:
            col = fk['constrained_columns'][0]
            ref_table = fk['referred_table']
            ref_col = fk['referred_columns'][0]
            table_info += f"  ForeignKey: {col} -> {ref_table}.{ref_col}\n"

        schema.append(table_info)
    return "\n".join(schema)


def print_all_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in the database:")
    with engine.connect() as conn:
        for table in tables:
            print(f"\n- {table}")
            result = conn.execute(text(f"SELECT * FROM {table}"))
            rows = result.fetchall()
            columns = result.keys()
            if not rows:
                print("  (No data)")
            else:
                for row in rows:
                    row_dict = dict(zip(columns, row))
                    print("  ", row_dict)


if __name__ == "__main__":
    if not os.path.exists("example.db"):
        print("Dumping data")
        create_ecommerce_db()
        print("Dumping data success")
    else:
        print("Data already present")
    
    print(print_all_tables())
