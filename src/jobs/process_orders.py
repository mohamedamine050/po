def calculate_order_total(items: list[dict]) -> float:
    """items: list of {"price": float, "quantity": int}"""
    return sum(item["price"] * item["quantity"] for item in items)


def filter_pending_orders(orders: list[dict]) -> list[dict]:
    """Return only orders with status == 'pending'."""
    return [o for o in orders if o.get("status") == "pending"]
