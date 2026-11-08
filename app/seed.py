from app.database import get_connection, initialize_database


def seed_orders():
    orders = [
        ("ORD1001", "Rahul Sharma", 2499.00, "Shipped", "Ahmedabad, Gujarat"),
        ("ORD1002", "Priya Patel", 1599.00, "Processing", "Mumbai, Maharashtra"),
        ("ORD1003", "Amit Shah", 4999.00, "Delivered", "Surat, Gujarat"),
        ("ORD1004", "Neha Mehta", 899.00, "Cancelled", "Pune, Maharashtra"),
        ("ORD1005", "Karan Desai", 3299.00, "Out for Delivery", "Vadodara, Gujarat"),
    ]

    with get_connection() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO orders
            (id, customer, amount, status, address)
            VALUES (?, ?, ?, ?, ?)
            """,
            orders
        )


if __name__ == "__main__":
    initialize_database()
    seed_orders()
    print("Sample orders inserted successfully.")