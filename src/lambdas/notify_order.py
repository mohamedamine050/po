import json


def format_notification(order_id: str, status: str) -> dict:
    return {"order_id": order_id, "status": status, "message": f"Order {order_id} is now {status}."}


def handler(event: dict, context) -> dict:
    body = event.get("body")
    if isinstance(body, str):
        body = json.loads(body)

    order_id = body.get("order_id")
    status = body.get("status", "unknown")

    if not order_id:
        return {"statusCode": 400, "body": json.dumps({"error": "order_id is required"})}

    notification = format_notification(order_id, status)
    return {"statusCode": 200, "body": json.dumps(notification)}
