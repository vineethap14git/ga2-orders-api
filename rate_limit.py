import time
from collections import defaultdict, deque
from fastapi import HTTPException

RATE_LIMIT = 18
WINDOW = 10

client_requests = defaultdict(deque)


def check_rate_limit(client_id: str):
    now = time.time()
    q = client_requests[client_id]

    # remove old requests
    while q and now - q[0] > WINDOW:
        q.popleft()

    if len(q) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": "10"}
        )

    q.append(now)
