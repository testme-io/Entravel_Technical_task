import math
from api.endpoints import ADD_ITEM


def calculate_discounted_total(subtotal: float, percent: float) -> float:
    # Team confirmed: always floor, never round
    return math.floor(subtotal * (1 - percent / 100))


def generate_item(name: str = "Item", price: float = 10.0, quantity: int = 1) -> dict:
    """Returns a simple dict for item payload"""
    return {"name": name, "price": price, "quantity": quantity}


def add_item_to_cart(api_client, cart_id: str, **kwargs):
    """Helper to quickly fill cart for other tests"""
    url = ADD_ITEM.format(cart_id=cart_id)
    payload = generate_item(**kwargs)
    resp = api_client.post(url, payload=payload)

    assert resp.status_code == 201, f"Setup failed: {resp.text}"
    return resp.json().get("id")