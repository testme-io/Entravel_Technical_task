import pytest
import allure
from api.endpoints import ADD_ITEM
from utils.helpers import generate_item


@allure.title("TC-INV-001 | Negative price — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_negative_price(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name="Item", price=-10.0, quantity=1)
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Negative price should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-002 | Zero price boundary — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "boundary", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_zero_price(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name="Item", price=0, quantity=1)
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Zero price should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-003 | Zero quantity — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_zero_quantity(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name="Item", price=10.0, quantity=0)
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Zero quantity should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-004 | Negative quantity — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_negative_quantity(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name="Item", price=10.0, quantity=-3)
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Negative quantity should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-005 | Missing name field — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_missing_name(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"price": 10.0, "quantity": 1}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Missing name should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-006 | Missing price field — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_missing_price(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": "Item", "quantity": 1}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Missing price should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-007 | Missing quantity field — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_missing_quantity(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": "Item", "price": 10.0}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Missing quantity should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-008 | Empty request body — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_empty_body(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Empty body should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-009 | Non-numeric price string — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_string_price(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": "Item", "price": "abc", "quantity": 1}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] String price should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-010 | Non-numeric quantity string — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_string_quantity(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": "Item", "price": 10.0, "quantity": "many"}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] String quantity should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-011 | Fractional quantity — expect 400 (assumed integer only)")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "boundary", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_fractional_quantity(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": "Item", "price": 10.0, "quantity": 2.5}
    response = api_client.post(url, payload=payload)

    # assumed: quantity must be integer — not confirmed by team, document actual behavior
    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[ASSUMED] Fractional quantity rejected — got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-012 | Empty string name — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_empty_name(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": "", "price": 10.0, "quantity": 1}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Empty name should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-013 | Whitespace-only name — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_whitespace_name(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": "   ", "price": 10.0, "quantity": 1}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] payload={payload} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Whitespace-only name should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-017 | Add item to non-existent cart — expect 404")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_add_to_nonexistent_cart(api_client):
    url = ADD_ITEM.format(cart_id="nonexistent-cart-00000")
    payload = generate_item(name="Item", price=10.0, quantity=1)
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] cart=nonexistent | status={response.status_code} | body={response.text}")

    assert response.status_code == 404, (
        f"[APP BUG] Expected 404 for non-existent cart, got {response.status_code} | body: {response.text}"
    )