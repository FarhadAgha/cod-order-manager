import sqlite3

DB_NAME = "orders.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            product TEXT NOT NULL,
            price REAL NOT NULL,
            notes TEXT,
            status TEXT DEFAULT 'Pending',
            ai_message TEXT,
            risk_level TEXT,
            risk_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_order(customer_name, phone, address, product, price, notes):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (customer_name, phone, address, product, price, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_name, phone, address, product, price, notes))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def get_all_orders():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_order_by_id_and_phone(order_id, phone):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM orders WHERE id = ? AND phone = ?",
        (order_id, phone)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_status(order_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

def save_ai_message(order_id, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET ai_message = ? WHERE id = ?", (message, order_id))
    conn.commit()
    conn.close()

def save_risk_assessment(order_id, risk_level, risk_reason):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET risk_level = ?, risk_reason = ? WHERE id = ?",
        (risk_level, risk_reason, order_id)
    )
    conn.commit()
    conn.close()

def delete_order(order_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()