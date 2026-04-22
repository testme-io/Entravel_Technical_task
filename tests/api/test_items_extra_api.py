import pytest
import allure
from api.endpoints import ADD_ITEM, GET_CART
from utils.helpers import generate_item


@allure.title("TC-ADD-006 | Long item name boundary — 256 chars")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_add_item_long_name(api_client, cart):
    long_name = "A" * 256
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name=long_name, price=5.0, quantity=1)
    response = api_client.post(url, payload=payload)

    print(f"\n[BOUNDARY] name_len={len(long_name)} | status={response.status_code} | body={response.text[:100]}")

    # system may accept or reject — documenting actual behavior
    assert response.status_code in [201, 400], (
        f"[APP BUG] Unexpected status for 256-char name, got {response.status_code}"
    )


@allure.title("TC-ADD-007 | Unicode and emoji in item name")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_add_item_unicode_emoji_name(api_client, cart):
    name = "Кофе ☕ Latté 日本語"
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name=name, price=5.0, quantity=1)
    response = api_client.post(url, payload=payload)

    print(f"\n[UNICODE] name='{name}' | status={response.status_code} | body={response.text}")

    assert response.status_code == 201, (
        f"[APP BUG] Unicode/emoji name should be accepted, got {response.status_code} | body: {response.text}"
    )

    data = response.json()
    assert data.get("name") == name, (
        f"[APP BUG] Name was altered: expected='{name}', got='{data.get('name')}'"
    )


@allure.title("TC-ADD-009 | Duplicate item — second add creates separate entry or merges qty")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_add_duplicate_item(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name="Coffee", price=10.0, quantity=1)

    api_client.post(url, payload=payload)
    api_client.post(url, payload=payload)

    data = api_client.get(GET_CART.format(cart_id=cart)).json()
    items = data["items"]

    print(f"\n[DUPLICATE] items_count={len(items)} | total={data.get('total')}")

    # both behaviors are acceptable: two separate entries or one merged
    assert len(items) in [1, 2], (
        f"[APP BUG] Expected 1 (merged) or 2 (separate) items after duplicate add, got {len(items)}"
    )
    assert data["total"] == 20.0, (
        f"[APP BUG] Expected total=20.0 after two identical items, got {data['total']}"
    )


@allure.title("TC-ADD-012 | High-precision float price — 3+ decimal places")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_add_item_high_precision_price(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name="Precise Item", price=9.999, quantity=1)
    response = api_client.post(url, payload=payload)

    print(f"\n[PRECISION] price=9.999 | status={response.status_code} | body={response.text}")

    # may accept and round, or reject — documenting actual behavior
    assert response.status_code in [201, 400], (
        f"[APP BUG] Unexpected status for 3-decimal price, got {response.status_code}"
    )

    if response.status_code == 201:
        data = api_client.get(GET_CART.format(cart_id=cart)).json()
        print(f"[PRECISION] total in cart={data.get('total')} (may be rounded)")