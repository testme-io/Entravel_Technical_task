import pytest
import allure
from api.endpoints import CREATE_CART, GET_CART, ADD_ITEM
from utils.helpers import generate_item


@allure.title("TC-CART-001 | Create new cart and verify cart ID generation")
@allure.description("Verify that POST /cart returns 201 and a valid cartId")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "positive")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_create_cart(api_client):
    response = api_client.post(CREATE_CART)

    print(f"\n[CART CREATE] status={response.status_code} | body={response.text}")

    assert response.status_code == 201, (
        f"[APP BUG] Expected 201, got {response.status_code} | body: {response.text}"
    )

    data = response.json()

    assert "cartId" in data, (
        f"[APP BUG] Response missing 'cartId' field | got: {data}"
    )
    assert isinstance(data["cartId"], str) and len(data["cartId"]) > 0, (
        f"[APP BUG] cartId is empty or not a string | got: {data['cartId']}"
    )


@allure.title("TC-CART-002 | Cart ID uniqueness — two carts must have different IDs")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
@pytest.mark.happy_path
def test_cart_id_uniqueness(api_client):
    resp_a = api_client.post(CREATE_CART)
    resp_b = api_client.post(CREATE_CART)

    id_a = resp_a.json()["cartId"]
    id_b = resp_b.json()["cartId"]

    print(f"\n[CART UNIQUE] cart_a={id_a} | cart_b={id_b}")

    assert id_a != id_b, (
        f"[APP BUG] Both carts got same ID: {id_a}"
    )


@allure.title("TC-CART-003 | Response body structure on cart creation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_create_cart_response_structure(api_client):
    response = api_client.post(CREATE_CART)
    data = response.json()

    print(f"\n[CART STRUCTURE] body={data}")

    assert "cartId" in data, (
        f"[APP BUG] Missing field 'cartId' in response | got: {data}"
    )
    assert isinstance(data["cartId"], str) and len(data["cartId"]) > 0, (
        f"[APP BUG] cartId is empty or not a string | got: {data['cartId']}"
    )


@allure.title("TC-CART-004 | Get empty cart — items=[] and total=0")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "positive")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_get_empty_cart(api_client, cart):
    url = GET_CART.format(cart_id=cart)
    response = api_client.get(url)
    data = response.json()

    print(f"\n[CART GET EMPTY] cart_id={cart} | body={data}")

    assert response.status_code == 200, (
        f"[APP BUG] Expected 200, got {response.status_code} | body: {response.text}"
    )
    assert "items" in data, (
        f"[APP BUG] Response missing 'items' field | got: {data}"
    )
    assert "total" in data, (
        f"[APP BUG] Response missing 'total' field | got: {data}"
    )
    assert data["items"] == [], (
        f"[APP BUG] Expected empty items list, got {data['items']}"
    )
    assert data["total"] == 0, (
        f"[APP BUG] Expected total=0 for empty cart, got {data['total']}"
    )


@allure.title("TC-CART-005 | Get cart with items — items and total are correct")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
@pytest.mark.happy_path
def test_get_cart_with_items(api_client, cart):
    item = generate_item(name="Coffee", price=10.0, quantity=2)
    add_url = ADD_ITEM.format(cart_id=cart)
    add_resp = api_client.post(add_url, payload=item)

    # if this fails — test setup issue, not app bug
    assert add_resp.status_code == 201, (
        f"[TEST SETUP FAILED] Could not add item | got {add_resp.status_code}: {add_resp.text}"
    )

    url = GET_CART.format(cart_id=cart)
    response = api_client.get(url)
    data = response.json()

    print(f"\n[CART GET] cart_id={cart} | items={data.get('items')} | total={data.get('total')}")

    assert response.status_code == 200, (
        f"[APP BUG] Expected 200, got {response.status_code}"
    )
    assert len(data["items"]) == 1, (
        f"[APP BUG] Expected 1 item, got {len(data['items'])}"
    )
    assert data["total"] == 20.0, (
        f"[APP BUG] Expected total=20.0 (10.0 x 2), got {data['total']}"
    )


@allure.title("TC-CART-006 | Get cart with non-existent ID — expect 404")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "smoke", "negative")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.negative
def test_get_cart_nonexistent_id(api_client):
    url = GET_CART.format(cart_id="nonexistent-cart-id-00000")
    response = api_client.get(url)

    print(f"\n[CART 404] status={response.status_code} | body={response.text}")

    assert response.status_code == 404, (
        f"[APP BUG] Expected 404 for missing cart, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-CART-007 | Get cart with empty ID segment — expect 404 or 405")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_get_cart_empty_id(api_client):
    url = GET_CART.format(cart_id=" ")
    response = api_client.get(url)

    print(f"\n[CART EMPTY ID] status={response.status_code} | body={response.text}")

    assert response.status_code in [404, 405], (
        f"[APP BUG] Expected 404 or 405 for empty ID, got {response.status_code}"
    )


@allure.title("TC-CART-008 | Get cart with numeric ID — expect 404")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_get_cart_numeric_id(api_client):
    url = GET_CART.format(cart_id="12345")
    response = api_client.get(url)

    print(f"\n[CART NUMERIC ID] status={response.status_code} | body={response.text}")

    assert response.status_code == 404, (
        f"[APP BUG] Expected 404 for numeric ID, got {response.status_code}"
    )


@allure.title("TC-CART-010 | Cart data isolation — carts do not share items")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_cart_isolation(api_client):
    cart_a = api_client.post(CREATE_CART).json()["cartId"]
    cart_b = api_client.post(CREATE_CART).json()["cartId"]

    add_url = ADD_ITEM.format(cart_id=cart_a)
    api_client.post(add_url, payload=generate_item(name="Item A", price=5.0, quantity=1))

    url_b = GET_CART.format(cart_id=cart_b)
    data_b = api_client.get(url_b).json()

    print(f"\n[ISOLATION] cart_a={cart_a} | cart_b={cart_b} | cart_b items={data_b.get('items')}")

    assert data_b["items"] == [], (
        f"[APP BUG] Cart B should be empty but got items: {data_b['items']}"
    )
    assert data_b["total"] == 0, (
        f"[APP BUG] Cart B total should be 0, got {data_b['total']}"
    )


@allure.title("TC-CART-013 | Response Content-Type header is application/json")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_response_content_type(api_client):
    response = api_client.post(CREATE_CART)
    content_type = response.headers.get("Content-Type", "")

    print(f"\n[HEADERS] Content-Type={content_type}")

    assert "application/json" in content_type, (
        f"[APP BUG] Expected application/json, got '{content_type}'"
    )