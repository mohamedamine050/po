import pytest
from src.jobs.process_orders import calculate_order_total, filter_pending_orders


class TestCalculateOrderTotal:
    def test_single_item(self):
        items = [{"price": 10.0, "quantity": 3}]
        assert calculate_order_total(items) == 30.0

    def test_multiple_items(self):
        items = [{"price": 5.0, "quantity": 2}, {"price": 20.0, "quantity": 1}]
        assert calculate_order_total(items) == 30.0

    def test_empty_list(self):
        assert calculate_order_total([]) == 0.0

    def test_fractional_prices(self):
        items = [{"price": 1.5, "quantity": 4}]
        assert calculate_order_total(items) == pytest.approx(6.0)


class TestFilterPendingOrders:
    def test_returns_only_pending(self):
        orders = [
            {"id": 1, "status": "pending"},
            {"id": 2, "status": "shipped"},
            {"id": 3, "status": "pending"},
        ]
        result = filter_pending_orders(orders)
        assert len(result) == 2
        assert all(o["status"] == "pending" for o in result)

    def test_empty_list(self):
        assert filter_pending_orders([]) == []

    def test_no_pending_orders(self):
        orders = [{"id": 1, "status": "shipped"}, {"id": 2, "status": "delivered"}]
        assert filter_pending_orders(orders) == []

    def test_all_pending(self):
        orders = [{"id": 1, "status": "pending"}, {"id": 2, "status": "pending"}]
        assert filter_pending_orders(orders) == orders
