import pytest
import allure
from api.endpoints import ADD_ITEM, GET_CART
from utils.helpers import generate_item


@allure.title("TC-ADD-001 | Add single item to cart")
@allure.description("Add one valid item and verify it appears in cart")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "positive")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_add_single_item(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    item = generate_item(name="Coffee", price=10.0, quantity=1)
    response = api_client.post(url, payload=item)

    print(f"\n[ADD ITEM] status={response.status_code} | body={response.text}")

    assert response.status_code == 201, (
        f"[APP BUG] Expected 201, got {response.status_code} | body: {response.text}"
    )

    data = response.json()
    assert data["name"] == "Coffee", (
        f"[APP BUG] Expected name='Coffee', got '{data.get('name')}'"
    )
    assert data["price"] == 10.0, (
        f"[APP BUG] Expected price=10.0, got {data.get('price')}"
    )
    assert data["quantity"] == 1, (
        f"[APP BUG] Expected quantity=1, got {data.get('quantity')}"
    )


@allure.title("TC-ADD-002 | Add multiple unique items — total is sum of all")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
@pytest.mark.happy_path
def test_add_multiple_items(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)

    items = [
        generate_item(name="Coffee", price=10.0, quantity=2),
        generate_item(name="Tea", price=5.0, quantity=3),
        generate_item(name="Juice", price=7.0, quantity=1),
    ]
    for item in items:
        api_client.post(url, payload=item)

    cart_url = GET_CART.format(cart_id=cart)
    response = api_client.get(cart_url)
    data = response.json()

    expected_total = (10.0 * 2) + (5.0 * 3) + (7.0 * 1)  # 42.0

    print(f"\n[MULTI ITEMS] items={len(data['items'])} | expected_total={expected_total} | actual_total={data.get('total')}")

    assert len(data["items"]) == 3, (
        f"[APP BUG] Expected 3 items, got {len(data['items'])}"
    )
    assert data["total"] == expected_total, (
        f"[APP BUG] Expected total={expected_total}, got {data['total']}"
    )


@allure.title("TC-ADD-003 | Add item with quantity > 1 — total is price x qty")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
@pytest.mark.happy_path
def test_add_item_with_quantity(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    item = generate_item(name="Water", price=3.0, quantity=5)
    api_client.post(url, payload=item)

    cart_url = GET_CART.format(cart_id=cart)
    data = api_client.get(cart_url).json()

    expected_total = 3.0 * 5

    print(f"\n[QTY > 1] price=3.0 | qty=5 | expected={expected_total} | actual={data.get('total')}")

    assert data["total"] == expected_total, (
        f"[APP BUG] Expected total={expected_total} (3.0 x 5), got {data['total']}"
    )


@allure.title("TC-ADD-004 | Minimum quantity boundary — quantity=1")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "positive", "boundary", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.boundary
@pytest.mark.regression
def test_add_item_min_quantity(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    item = generate_item(name="Snack", price=2.0, quantity=1)
    response = api_client.post(url, payload=item)

    print(f"\n[MIN QTY] status={response.status_code} | body={response.text}")

    assert response.status_code == 201, (
        f"[APP BUG] quantity=1 should be valid, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-ADD-005 | Minimum price boundary — price=1")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "positive", "boundary", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.boundary
@pytest.mark.regression
def test_add_item_min_price(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    item = generate_item(name="Candy", price=1.0, quantity=1)
    response = api_client.post(url, payload=item)

    print(f"\n[MIN PRICE] status={response.status_code} | body={response.text}")

    assert response.status_code == 201, (
        f"[APP BUG] price=1 should be valid, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-ADD-008 | Valid float price — price=9.99")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_add_item_float_price(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    item = generate_item(name="Latte", price=9.99, quantity=1)
    response = api_client.post(url, payload=item)

    print(f"\n[FLOAT PRICE] status={response.status_code} | body={response.text}")

    assert response.status_code == 201, (
        f"[APP BUG] Float price 9.99 should be valid, got {response.status_code} | body: {response.text}"
    )

    cart_url = GET_CART.format(cart_id=cart)
    data = api_client.get(cart_url).json()

    print(f"\n[FLOAT PRICE] total={data.get('total')}")

    assert data["total"] == 9.99, (
        f"[APP BUG] Expected total=9.99, got {data['total']}"
    )


@allure.title("TC-ADD-010 | Item response structure contains all required fields")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_add_item_response_structure(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    item = generate_item(name="Burger", price=8.0, quantity=2)
    response = api_client.post(url, payload=item)
    data = response.json()

    print(f"\n[ITEM STRUCTURE] body={data}")

    for field in ["id", "name", "price", "quantity"]:
        assert field in data, (
            f"[APP BUG] Missing field '{field}' in item response | got: {data}"
        )

    assert isinstance(data["id"], str) and len(data["id"]) > 0, (
        f"[APP BUG] item id is empty or not a string | got: {data['id']}"
    )


@allure.title("TC-CALC-001 | Total for single item qty=1")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_total_single_item_qty_one(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    api_client.post(url, payload=generate_item(name="Item", price=10.0, quantity=1))

    data = api_client.get(GET_CART.format(cart_id=cart)).json()

    print(f"\n[CALC] price=10.0 | qty=1 | total={data.get('total')}")

    assert data["total"] == 10.0, (
        f"[APP BUG] Expected total=10.0, got {data['total']}"
    )


@allure.title("TC-CALC-005 | Total for empty cart is 0")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_total_empty_cart(api_client, cart):
    data = api_client.get(GET_CART.format(cart_id=cart)).json()

    print(f"\n[CALC EMPTY] total={data.get('total')}")

    assert data["total"] == 0, (
        f"[APP BUG] Expected total=0 for empty cart, got {data['total']}"
    )


@allure.title("TC-CALC-008 | Total updates immediately after adding item")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_total_updates_immediately(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    api_client.post(url, payload=generate_item(name="Item", price=15.0, quantity=1))

    data = api_client.get(GET_CART.format(cart_id=cart)).json()

    print(f"\n[IMMEDIATE UPDATE] total={data.get('total')}")

    assert data["total"] == 15.0, (
        f"[APP BUG] Total not updated after adding item | got {data['total']}"
    )