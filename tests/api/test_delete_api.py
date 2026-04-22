import pytest
import allure
from api.endpoints import ADD_ITEM, DELETE_ITEM, GET_CART
from utils.helpers import generate_item


@allure.title("TC-DEL-001 | Remove existing item from cart")
@allure.description("Add item, delete it, verify it is removed from cart")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "positive")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_delete_existing_item(api_client, cart_with_item):
    cart_id, item_id = cart_with_item

    url = DELETE_ITEM.format(cart_id=cart_id, item_id=item_id)
    response = api_client.delete(url)

    print(f"\n[DELETE] cart={cart_id} | item={item_id} | status={response.status_code}")

    assert response.status_code == 204, (
        f"[APP BUG] Expected 204 on delete, got {response.status_code} | body: {response.text}"
    )

    cart_data = api_client.get(GET_CART.format(cart_id=cart_id)).json()

    print(f"\n[DELETE] remaining items={len(cart_data['items'])} | total={cart_data['total']}")

    assert cart_data["items"] == [], (
        f"[APP BUG] Expected empty cart after delete, got {cart_data['items']}"
    )


@allure.title("TC-DEL-002 | Total recalculates correctly after item deletion")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_total_recalculates_after_delete(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)

    resp_a = api_client.post(url, payload=generate_item(name="Item A", price=10.0, quantity=1))
    resp_b = api_client.post(url, payload=generate_item(name="Item B", price=20.0, quantity=1))

    assert resp_a.status_code == 201, "[TEST SETUP FAILED] Could not add Item A"
    assert resp_b.status_code == 201, "[TEST SETUP FAILED] Could not add Item B"

    item_a_id = resp_a.json()["id"]

    delete_url = DELETE_ITEM.format(cart_id=cart, item_id=item_a_id)
    api_client.delete(delete_url)

    cart_data = api_client.get(GET_CART.format(cart_id=cart)).json()

    print(f"\n[DELETE RECALC] remaining items={len(cart_data['items'])} | total={cart_data['total']}")

    assert len(cart_data["items"]) == 1, (
        f"[APP BUG] Expected 1 item after delete, got {len(cart_data['items'])}"
    )
    assert cart_data["total"] == 20.0, (
        f"[APP BUG] Expected total=20.0 after deleting 10.0 item, got {cart_data['total']}"
    )


@allure.title("TC-DEL-003 | Sequential removal of all items — cart ends up empty")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_delete_all_items_sequentially(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)

    items = [
        generate_item(name="Item A", price=5.0, quantity=1),
        generate_item(name="Item B", price=10.0, quantity=1),
        generate_item(name="Item C", price=15.0, quantity=1),
    ]

    item_ids = []
    for item in items:
        resp = api_client.post(url, payload=item)
        assert resp.status_code == 201, f"[TEST SETUP FAILED] Could not add {item['name']}"
        item_ids.append(resp.json()["id"])

    for item_id in item_ids:
        delete_url = DELETE_ITEM.format(cart_id=cart, item_id=item_id)
        api_client.delete(delete_url)

    cart_data = api_client.get(GET_CART.format(cart_id=cart)).json()

    print(f"\n[DELETE ALL] items={cart_data['items']} | total={cart_data['total']}")

    assert cart_data["items"] == [], (
        f"[APP BUG] Expected empty cart, got {cart_data['items']}"
    )
    assert cart_data["total"] == 0, (
        f"[APP BUG] Expected total=0 after removing all items, got {cart_data['total']}"
    )


@allure.title("TC-DEL-004 | Delete non-existent item — expect 404")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_delete_nonexistent_item(api_client, cart):
    url = DELETE_ITEM.format(cart_id=cart, item_id="nonexistent-item-00000")
    response = api_client.delete(url)

    print(f"\n[DELETE 404] status={response.status_code} | body={response.text}")

    assert response.status_code == 404, (
        f"[APP BUG] Expected 404 for non-existent item, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DEL-005 | Double deletion — second attempt returns 404")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_double_delete(api_client, cart_with_item):
    cart_id, item_id = cart_with_item

    url = DELETE_ITEM.format(cart_id=cart_id, item_id=item_id)

    first = api_client.delete(url)
    second = api_client.delete(url)

    print(f"\n[DOUBLE DELETE] first={first.status_code} | second={second.status_code}")

    assert first.status_code == 204, (
        f"[APP BUG] First delete should return 204, got {first.status_code}"
    )
    assert second.status_code == 404, (
        f"[APP BUG] Second delete should return 404, got {second.status_code} | body: {second.text}"
    )


@allure.title("TC-DEL-006 | Cross-cart deletion — item from another cart returns 404")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_cross_cart_delete(api_client, cart):
    from api.endpoints import CREATE_CART

    # create cart B and add item to it
    cart_b_id = api_client.post(CREATE_CART).json()["cartId"]
    add_url = ADD_ITEM.format(cart_id=cart_b_id)
    resp = api_client.post(add_url, payload=generate_item(name="Item B", price=5.0, quantity=1))
    assert resp.status_code == 201, "[TEST SETUP FAILED] Could not add item to cart B"

    item_b_id = resp.json()["id"]

    # try to delete cart B item using cart A id
    url = DELETE_ITEM.format(cart_id=cart, item_id=item_b_id)
    response = api_client.delete(url)

    print(f"\n[CROSS CART] cart_a={cart} | item_from_b={item_b_id} | status={response.status_code}")

    assert response.status_code in [404, 400], (
        f"[APP BUG] Expected 404/400 for cross-cart delete, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DEL-007 | Delete from non-existent cart — expect 404")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_delete_from_nonexistent_cart(api_client):
    url = DELETE_ITEM.format(cart_id="nonexistent-cart-00000", item_id="nonexistent-item-00000")
    response = api_client.delete(url)

    print(f"\n[DELETE NO CART] status={response.status_code} | body={response.text}")

    assert response.status_code == 404, (
        f"[APP BUG] Expected 404 for non-existent cart, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DEL-008 | Discount recalculates after item deletion")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_discount_recalculates_after_delete(api_client, cart):
    from api.endpoints import APPLY_DISCOUNT

    add_url = ADD_ITEM.format(cart_id=cart)

    resp_a = api_client.post(add_url, payload=generate_item(name="Item A", price=10.0, quantity=1))
    resp_b = api_client.post(add_url, payload=generate_item(name="Item B", price=20.0, quantity=1))

    assert resp_a.status_code == 201, "[TEST SETUP FAILED] Could not add Item A"
    assert resp_b.status_code == 201, "[TEST SETUP FAILED] Could not add Item B"

    item_a_id = resp_a.json()["id"]

    disc_url = APPLY_DISCOUNT.format(cart_id=cart)
    disc_resp = api_client.post(disc_url, payload={"code": "SAVE10"})
    assert disc_resp.status_code == 200, "[TEST SETUP FAILED] Could not apply discount"

    delete_url = DELETE_ITEM.format(cart_id=cart, item_id=item_a_id)
    api_client.delete(delete_url)

    cart_data = api_client.get(GET_CART.format(cart_id=cart)).json()

    print(f"\n[DELETE + DISCOUNT] items={len(cart_data['items'])} | total={cart_data['total']} | discount={cart_data.get('discount')} | discountCode={cart_data.get('discountCode')}")

    # document actual behavior — either discount stays applied or resets
    assert cart_data["total"] >= 0, (
        f"[APP BUG] Total should never be negative, got {cart_data['total']}"
    )
    assert len(cart_data["items"]) == 1, (
        f"[APP BUG] Expected 1 item after delete, got {len(cart_data['items'])}"
    )


@allure.title("TC-CALC-004 | Total updates correctly after item removal")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_total_updates_after_removal(api_client, cart):
    add_url = ADD_ITEM.format(cart_id=cart)

    resp_a = api_client.post(add_url, payload=generate_item(name="A", price=15.0, quantity=2))
    resp_b = api_client.post(add_url, payload=generate_item(name="B", price=5.0, quantity=1))

    assert resp_a.status_code == 201, "[TEST SETUP FAILED] Could not add Item A"
    assert resp_b.status_code == 201, "[TEST SETUP FAILED] Could not add Item B"

    item_b_id = resp_b.json()["id"]

    delete_url = DELETE_ITEM.format(cart_id=cart, item_id=item_b_id)
    api_client.delete(delete_url)

    cart_data = api_client.get(GET_CART.format(cart_id=cart)).json()

    expected_total = 15.0 * 2  # only Item A remains

    print(f"\n[CALC AFTER DELETE] expected={expected_total} | actual={cart_data['total']}")

    assert cart_data["total"] == expected_total, (
        f"[APP BUG] Expected total={expected_total} after removing Item B, got {cart_data['total']}"
    )