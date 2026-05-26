import json
import pytest
from src.lambdas.notify_order import format_notification, handler


class TestFormatNotification:
    def test_returns_expected_keys(self):
        result = format_notification("ORD-001", "shipped")
        assert result["order_id"] == "ORD-001"
        assert result["status"] == "shipped"
        assert "message" in result

    def test_message_contains_order_id_and_status(self):
        result = format_notification("ORD-999", "delivered")
        assert "ORD-999" in result["message"]
        assert "delivered" in result["message"]


class TestHandler:
    def _event(self, body: dict) -> dict:
        return {"body": json.dumps(body)}

    def test_valid_request_returns_200(self):
        response = handler(self._event({"order_id": "ORD-001", "status": "shipped"}), None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["order_id"] == "ORD-001"

    def test_missing_order_id_returns_400(self):
        response = handler(self._event({"status": "pending"}), None)
        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "error" in body

    def test_default_status_is_unknown(self):
        response = handler(self._event({"order_id": "ORD-002"}), None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["status"] == "unknown"

    def test_body_as_dict_is_accepted(self):
        event = {"body": {"order_id": "ORD-003", "status": "pending"}}
        response = handler(event, None)
        assert response["statusCode"] == 200
