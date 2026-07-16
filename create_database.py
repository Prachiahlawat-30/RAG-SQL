import sqlite3
import os

# Remove old database if exists
if os.path.exists("amazon.db"):
    os.remove("amazon.db")

conn = sqlite3.connect("amazon.db")
cursor = conn.cursor()

# ---------------- CUSTOMERS ----------------
cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    city TEXT,
    join_date TEXT
)
""")

# ---------------- PRODUCTS ----------------
cursor.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT
)
""")

# ---------------- ORDERS ----------------
cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
)
""")

# ---------------- ORDER ITEMS ----------------
cursor.execute("""
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY(order_id)
    REFERENCES orders(order_id),
    FOREIGN KEY(product_id)
    REFERENCES products(product_id)
)
""")

# CUSTOMERS
customers = [
    ("Amit Sharma", "amit@gmail.com", "Delhi", "2025-01-10"),
    ("Priya Verma", "priya@gmail.com", "Mumbai", "2025-01-15"),
    ("Rahul Singh", "rahul@gmail.com", "Bangalore", "2025-02-01"),
    ("Sneha Gupta", "sneha@gmail.com", "Pune", "2025-02-10"),
    ("Arjun Mehta", "arjun@gmail.com", "Chennai", "2025-03-05"),
    ("Neha Kapoor", "neha@gmail.com", "Hyderabad", "2025-03-12"),
    ("Vikas Yadav", "vikas@gmail.com", "Noida", "2025-04-01"),
    ("Anjali Jain", "anjali@gmail.com", "Jaipur", "2025-04-15"),
    ("Rohan Das", "rohan@gmail.com", "Kolkata", "2025-05-01"),
    ("Pooja Mishra", "pooja@gmail.com", "Lucknow", "2025-05-20")
]

cursor.executemany(
    "INSERT INTO customers(name,email,city,join_date) VALUES(?,?,?,?)",
    customers
)

# PRODUCTS
products = [
    ("Laptop",65000,"Electronics"),
    ("Smartphone",30000,"Electronics"),
    ("Headphones",2500,"Accessories"),
    ("Keyboard",1500,"Accessories"),
    ("Mouse",800,"Accessories"),
    ("Monitor",12000,"Electronics"),
    ("Smart Watch",5000,"Wearables"),
    ("Power Bank",1800,"Accessories"),
    ("Tablet",25000,"Electronics"),
    ("Printer",9000,"Office")
]

cursor.executemany(
    "INSERT INTO products(name,price,category) VALUES(?,?,?)",
    products
)

# ORDERS
orders = [
    (1,"2025-06-01",67500),
    (2,"2025-06-02",30000),
    (3,"2025-06-03",14500),
    (4,"2025-06-04",5800),
    (5,"2025-06-05",25000),
    (6,"2025-06-06",66800),
    (7,"2025-06-07",9000),
    (8,"2025-06-08",12000),
    (9,"2025-06-09",33000),
    (10,"2025-06-10",4300)
]

cursor.executemany(
    "INSERT INTO orders(customer_id,order_date,total_amount) VALUES(?,?,?)",
    orders
)

# ORDER ITEMS
order_items = [
    (1,1,1,65000),
    (1,4,1,1500),
    (2,2,1,30000),
    (3,6,1,12000),
    (3,5,2,800),
    (4,7,1,5000),
    (4,5,1,800),
    (5,9,1,25000),
    (6,1,1,65000),
    (6,8,1,1800),
    (7,10,1,9000),
    (8,6,1,12000),
    (9,2,1,30000),
    (9,3,1,2500),
    (10,3,1,2500),
    (10,8,1,1800)
]

cursor.executemany("""
INSERT INTO order_items
(order_id,product_id,quantity,price)
VALUES(?,?,?,?)
""", order_items)

conn.commit()
conn.close()

print("Database Created Successfully!")