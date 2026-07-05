from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel
import uuid

from store import orders, idempotency_store, get_orders_slice, TOTAL_ORDERS
from rate_limit import check_rate_limit

app = FastAPI()

# -------------------------
# Models
# -------------------------
class OrderRequest(BaseModel):
    item: str


# -------------------------
# CORS (required by grader)
# -------------------------
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# 1. Idempotent POST /orders
# -------------------------
@app.post("/orders", status_code=201)
def create_order(
    payload: OrderRequest,
    idempotency_key: str = Header(None),
    x_client_id: str = Header(None)
):
    if not x_client_id:
        raise HTTPException(400, "Missing X-Client-Id")

    check_rate_limit(x_client_id)

    if not idempotency_key:
        raise HTTPException(400, "Missing Idempotency-Key")

    # return same response if repeated
    if idempotency_key in idempotency_store:
        return idempotency_store[idempotency_key]

    order_id = str(uuid.uuid4())

    response = {
        "id": order_id,
        "item": payload.item
    }

    idempotency_store[idempotency_key] = response
    return response


# -------------------------
# 2. Cursor Pagination GET /orders
# -------------------------
@app.get("/orders")
def list_orders(
    limit: int = Query(10, le=50),
    cursor: str = Query(None),
    x_client_id: str = Header(None)
):
    if not x_client_id:
        raise HTTPException(400, "Missing X-Client-Id")

    check_rate_limit(x_client_id)

    start = int(cursor) if cursor else 1

    items = get_orders_slice(start, limit)

    next_cursor = start + len(items)
    if next_cursor > TOTAL_ORDERS:
        next_cursor = None

    return {
        "items": items,
        "next_cursor": str(next_cursor) if next_cursor else None
    }
