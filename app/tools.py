from langchain.tools import tool
from app.database import get_connection

@tool
def get_order(order_id: str) -> str:
    """Retrieve order details using the order ID."""

    with get_connection() as conn:
        order = conn.execute(
            """
            SELECT id, customer, email, amount, status, address
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
        f"Email: {order[2]}\n"
        f"Amount: ₹{order[3]:.2f}\n"
        f"Status: {order[4]}\n"
        f"Delivery Address: {order[5]}"
    )

@tool
def search_orders(customer: str) -> str:
    """Search orders using customer name or email."""

    with get_connection() as conn:
        orders = conn.execute(
            """
            SELECT id, customer, email, amount, status
            FROM orders
            WHERE LOWER(customer) LIKE LOWER(?)
               OR LOWER(email) = LOWER(?)
            """,
            (f"%{customer}%", customer)
        ).fetchall()

    if not orders:
        return f"No orders found for customer: {customer}."

    results = [f"Found {len(orders)} order(s):"]

    for order in orders:
        results.append(
            f"{order[0]} | {order[1]} | ₹{order[3]:.2f} | {order[4]}"
        )

    return "\n".join(results)

@tool
def refund(order_id: str, amount: float) -> str:
    """Record an approved partial or full refund for an order."""

    if amount <= 0:
        return "Refund amount must be greater than zero."

    with get_connection() as conn:
        order = conn.execute(
            "SELECT amount FROM orders WHERE id = ?",
            (order_id,)
        ).fetchone()

        if order is None:
            return f"No order found with ID {order_id}."

        total_amount = order[0]

        refunded = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM refunds
            WHERE order_id = ?
            """,
            (order_id,)
        ).fetchone()[0]

        remaining = total_amount - refunded

        if amount > remaining:
            return (
                f"Refund exceeds the remaining refundable amount. "
                f"Remaining: ₹{remaining:.2f}"
            )

        conn.execute(
            """
            INSERT INTO refunds (order_id, amount, status)
            VALUES (?, ?, ?)
            """,
            (order_id, amount, "Recorded")
        )

    return (
        f"Refund recorded successfully.\n"
        f"Order ID: {order_id}\n"
        f"Refund Amount: ₹{amount:.2f}"
    )

@tool
def update_address(order_id: str, address: str) -> str:
    """Update the delivery address for an eligible order."""

    if not address.strip():
        return "Delivery address cannot be empty."

    with get_connection() as conn:
        order = conn.execute(
            "SELECT status FROM orders WHERE id = ?",
            (order_id,)
        ).fetchone()

        if order is None:
            return f"No order found with ID {order_id}."

        if order[0].lower() != "processing":
            return (
                f"Address cannot be updated. "
                f"Current order status: {order[0]}."
            )

        conn.execute(
            "UPDATE orders SET address = ? WHERE id = ?",
            (address, order_id)
        )

    return (
        f"Delivery address updated successfully.\n"
        f"Order ID: {order_id}\n"
        f"New Address: {address}"
    )