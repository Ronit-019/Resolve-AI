from langchain.tools import tool
from app.database import get_connection


@tool
def get_order_details(order_id: str) -> str:
    """Retrieve order details using the customer's order ID."""

    with get_connection() as conn:
        order = conn.execute(
            """
            SELECT id, customer, amount, status, address
            FROM orders
            WHERE id = ?
            """,
            (order_id,)
        ).fetchone()

    if order is None:
        return f"No order found with ID {order_id}."

    return (
        f"Order ID: {order[0]}\n"
        f"Customer: {order[1]}\n"
        f"Amount: ₹{order[2]:.2f}\n"
        f"Status: {order[3]}\n"
        f"Delivery Address: {order[4]}"
    )