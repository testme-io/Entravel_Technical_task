import pytest
import allure
from api.endpoints import ADD_ITEM, DELETE_ITEM, GET_CART
from utils.helpers import generate_item, add_item_to_cart


@allure.title("TC-CALC-002 | Total for single item with qty > 1")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_total_single_item_qty_multiple(api_client, cart):
    add_item_to_cart(api_client, cart, name="Widget", price=10.0, quantity=3)

    data = api_client.get(GET_CART.format(cart_id=cart)).json()
    expected = 10.0 * 3

    print(f"\n[CALC-002] price=10.0 | qty=3 | expected={expected} | actual={data.get('total')}")

    assert data["total"] == expected, (
        f"[APP BUG] Expected total={expected} (10.0 x 3), got {data['total']}"
    )


@allure.title("TC-CALC-003 | Total for multiple different items")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_total_multiple_items(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)

    api_client.post(url, payload=generate_item(name="Coffee", price=10.0, quantity=2))
    api_client.post(url, payload=generate_item(name="Tea", price=5.0, quantity=3))
    api_client.post(url, payload=generate_item(name="Juice", price=7.0, quantity=1))

    data = api_client.get(GET_CART.format(cart_id=cart)).json()
    expected = (10.0 * 2) + (5.0 * 3) + (7.0 * 1)  # 42.0

    print(f"\n[CALC-003] items=3 | expected_total={expected} | actual={data.get('total')}")

    assert data["total"] == expected, (
        f"[APP BUG] Expected total={expected}, got {data['total']}"
    )


@allure.title("TC-CALC-006 | Total never goes negative after removing all items")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "boundary", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.boundary
@pytest.mark.regression
def test_total_non_negative_after_deletions(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)

    resp_a = api_client.post(url, payload=generate_item(name="Item A", price=15.0, quantity=1))
    resp_b = api_client.post(url, payload=generate_item(name="Item B", price=25.0, quantity=1))

    assert resp_a.status_code == 201, "[TEST SETUP FAILED] Could not add Item A"
    assert resp_b.status_code == 201, "[TEST SETUP FAILED] Could not add Item B"

    for resp in [resp_a, resp_b]:
        item_id = resp.json()["id"]
        api_client.delete(DELETE_ITEM.format(cart_id=cart, item_id=item_id))

    data = api_client.get(GET_CART.format(cart_id=cart)).json()

    print(f"\n[CALC-006] total after removing all items={data.get('total')}")

    assert data["total"] >= 0, (
        f"[APP BUG] Total must never be negative, got {data['total']}"
    )
    assert data["total"] == 0, (
        f"[APP BUG] Expected total=0 after removing all items, got {data['total']}"
    )


@allure.title("TC-CALC-007 | Large price and quantity — no overflow or precision loss")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_total_large_values(api_client, cart):
    add_item_to_cart(api_client, cart, name="Bulk Item", price=999.0, quantity=1000)

    data = api_client.get(GET_CART.format(cart_id=cart)).json()
    expected = 999.0 * 1000  # 999000.0

    print(f"\n[CALC-007] price=999.0 | qty=1000 | expected={expected} | actual={data.get('total')}")

    assert data["total"] == expected, (
        f"[APP BUG] Large value total mismatch: expected={expected}, got {data['total']}"
    )