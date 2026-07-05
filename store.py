from typing import Dict, List, Optional

TOTAL_ORDERS = 52

orders: Dict[int, dict] = {}
idempotency_store: Dict[str, dict] = {}

# pre-generate fixed catalog 1..52
for i in range(1, TOTAL_ORDERS + 1):
    orders[i] = {
        "id": i,
        "item": f"order-{i}"
    }


def get_orders_slice(start: int, limit: int):
    items = []
    for i in range(start, min(start + limit, TOTAL_ORDERS + 1)):
        items.append(orders[i])
    return items
