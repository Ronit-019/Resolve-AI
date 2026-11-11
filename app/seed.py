from app.database import get_connection, initialize_database


def seed_orders():
    orders = [
        ("ORD1001", "Rahul Sharma", "rahul@gmail.com", 2499.00, "Shipped", "Ahmedabad, Gujarat"),
        ("ORD1002", "Priya Patel", "priya@gmail.com", 1599.00, "Processing", "Mumbai, Maharashtra"),
        ("ORD1003", "Amit Shah", "amit@gmail.com", 4999.00, "Delivered", "Surat, Gujarat"),
        ("ORD1004", "Neha Mehta", "neha@gmail.com", 899.00, "Cancelled", "Pune, Maharashtra"),
        ("ORD1005", "Karan Desai", "karan@gmail.com", 3299.00, "Out for Delivery", "Vadodara, Gujarat"),
    ]

    with get_connection() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO orders
            (id, customer, email, amount, status, address)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            orders
        )

def update_order_emails():
    emails = [
        ("rahul@gmail.com", "ORD1001"),
        ("priya@gmail.com", "ORD1002"),
        ("amit@gmail.com", "ORD1003"),
        ("neha@gmail.com", "ORD1004"),
        ("karan@gmail.com", "ORD1005"),
    ]

    with get_connection() as conn:
        conn.executemany(
            """
            UPDATE orders
            SET email = ?
            WHERE id = ?
            """,
            emails
        )


if __name__ == "__main__":
    initialize_database()
    seed_orders()
    update_order_emails()
    print("Sample orders inserted successfully.")