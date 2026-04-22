import pytest
import allure
from api.endpoints import GET_CART, APPLY_DISCOUNT
from utils.helpers import calculate_discounted_total, add_item_to_cart


def apply_and_get(api_client, cart_id, code):
    """Apply discount and return updated cart state via GET."""
    url = APPLY_DISCOUNT.format(cart_id=cart_id)
    resp = api_client.post(url, payload={"code": code})
    cart = api_client.get(GET_CART.format(cart_id=cart_id)).json()
    return resp, cart


@allure.title("TC-DISC-001 | Apply SAVE10 — verify 10% discount with floor rounding")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "positive")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_apply_save10(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=20.0, quantity=1)

    response, cart_data = apply_and_get(api_client, cart, "SAVE10")
    expected = calculate_discounted_total(20.0, 10)

    print(f"\n[SAVE10] subtotal=20 | expected={expected} | actual={cart_data.get('total')} | discount={cart_data.get('discount')}")

    assert response.status_code == 200, (
        f"[APP BUG] Expected 200, got {response.status_code} | body: {response.text}"
    )
    assert cart_data["total"] == expected, (
        f"[APP BUG] SAVE10: expected total={expected}, got {cart_data['total']}"
    )
    assert cart_data["discountCode"] == "SAVE10", (
        f"[APP BUG] Expected discountCode='SAVE10', got {cart_data.get('discountCode')}"
    )


@allure.title("TC-DISC-002 | Apply SAVE20 — verify 20% discount with floor rounding")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "positive")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_apply_save20(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=20.0, quantity=1)

    response, cart_data = apply_and_get(api_client, cart, "SAVE20")
    expected = calculate_discounted_total(20.0, 20)

    print(f"\n[SAVE20] subtotal=20 | expected={expected} | actual={cart_data.get('total')} | discount={cart_data.get('discount')}")

    assert response.status_code == 200, (
        f"[APP BUG] Expected 200, got {response.status_code} | body: {response.text}"
    )
    assert cart_data["total"] == expected, (
        f"[APP BUG] SAVE20: expected total={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DISC-003 | Apply HALF — verify 50% discount with floor rounding")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "positive")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_apply_half(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=20.0, quantity=1)

    response, cart_data = apply_and_get(api_client, cart, "HALF")
    expected = calculate_discounted_total(20.0, 50)

    print(f"\n[HALF] subtotal=20 | expected={expected} | actual={cart_data.get('total')} | discount={cart_data.get('discount')}")

    assert response.status_code == 200, (
        f"[APP BUG] Expected 200, got {response.status_code} | body: {response.text}"
    )
    assert cart_data["total"] == expected, (
        f"[APP BUG] HALF: expected total={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DISC-004 | Override SAVE10 with SAVE20 — only last code applies")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_override_discount_save10_to_save20(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=20.0, quantity=1)

    disc_url = APPLY_DISCOUNT.format(cart_id=cart)
    api_client.post(disc_url, payload={"code": "SAVE10"})
    response, cart_data = apply_and_get(api_client, cart, "SAVE20")

    expected = calculate_discounted_total(20.0, 20)

    print(f"\n[OVERRIDE] SAVE10->SAVE20 | expected={expected} | actual={cart_data.get('total')} | code={cart_data.get('discountCode')}")

    assert cart_data["discountCode"] == "SAVE20", (
        f"[APP BUG] Expected discountCode='SAVE20' after override, got {cart_data.get('discountCode')}"
    )
    assert cart_data["total"] == expected, (
        f"[APP BUG] After SAVE10->SAVE20: expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DISC-005 | Override SAVE20 with HALF — only last code applies")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_override_discount_save20_to_half(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=20.0, quantity=1)

    disc_url = APPLY_DISCOUNT.format(cart_id=cart)
    api_client.post(disc_url, payload={"code": "SAVE20"})
    response, cart_data = apply_and_get(api_client, cart, "HALF")

    expected = calculate_discounted_total(20.0, 50)

    print(f"\n[OVERRIDE] SAVE20->HALF | expected={expected} | actual={cart_data.get('total')} | code={cart_data.get('discountCode')}")

    assert cart_data["discountCode"] == "HALF", (
        f"[APP BUG] Expected discountCode='HALF' after override, got {cart_data.get('discountCode')}"
    )
    assert cart_data["total"] == expected, (
        f"[APP BUG] After SAVE20->HALF: expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DISC-009 | POST /discount response structure")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_discount_response_structure(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=20.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": "SAVE10"})
    data = response.json()

    print(f"\n[DISC STRUCTURE] POST response={data}")

    # POST /discount returns minimal response — this is BUG-005
    # full cart state is only available via GET /cart
    assert response.status_code == 200, (
        f"[APP BUG] Expected 200, got {response.status_code}"
    )
    assert "discount" in data, (
        f"[APP BUG] Missing 'discount' field in POST /discount response | got: {data}"
    )


@allure.title("TC-DCALC-001 | SAVE10 on even subtotal — floor(100 * 0.9) = 90")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_save10_even_subtotal(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=100.0, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "SAVE10")
    expected = calculate_discounted_total(100.0, 10)

    print(f"\n[DCALC] subtotal=100 | SAVE10 | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] SAVE10 on 100: expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DCALC-002 | SAVE10 on odd subtotal — floor(15 * 0.9) = 13 not 14")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "boundary", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.boundary
@pytest.mark.regression
def test_save10_odd_subtotal_floor(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=15.0, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "SAVE10")
    expected = calculate_discounted_total(15.0, 10)

    print(f"\n[FLOOR] subtotal=15 | SAVE10 | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] Floor rounding failed: subtotal=15, SAVE10, expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DCALC-006 | HALF on odd subtotal — floor(7 * 0.5) = 3 not 4")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "boundary", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.boundary
@pytest.mark.regression
def test_half_odd_subtotal_floor(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=7.0, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "HALF")
    expected = calculate_discounted_total(7.0, 50)

    print(f"\n[FLOOR] subtotal=7 | HALF | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] Floor rounding failed: subtotal=7, HALF, expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DCALC-009 | Discount applies to full subtotal not first item only")
@allure.description("BUG-004: discount may apply only to first item in cart")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_discount_applies_to_full_subtotal(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item A", price=10.0, quantity=1)
    add_item_to_cart(api_client, cart, name="Item B", price=20.0, quantity=1)

    subtotal = 30.0
    _, cart_data = apply_and_get(api_client, cart, "SAVE10")
    expected = calculate_discounted_total(subtotal, 10)

    print(f"\n[BUG-004] subtotal={subtotal} | SAVE10 | expected={expected} | actual={cart_data.get('total')} | discount={cart_data.get('discount')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG - BUG-004] Discount applies to first item only: "
        f"subtotal={subtotal}, expected={expected}, got {cart_data['total']}. "
        f"discount={cart_data.get('discount')} instead of {subtotal - expected}"
    )


@allure.title("TC-DCALC-011 | Floor on micro subtotal — SAVE10 on 0.09")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_floor_micro_subtotal(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=0.09, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "SAVE10")
    expected = calculate_discounted_total(0.09, 10)

    print(f"\n[MICRO] subtotal=0.09 | SAVE10 | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] Micro subtotal floor: expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DCALC-012 | Floor at cent boundary — SAVE10 on 19.99")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_floor_cent_boundary(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=19.99, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "SAVE10")
    expected = calculate_discounted_total(19.99, 10)

    print(f"\n[CENT] subtotal=19.99 | SAVE10 | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] Cent boundary floor: expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DINV-001 | Invalid discount code — expect 400 or 404")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "smoke", "negative")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.negative
def test_invalid_discount_code(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=10.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": "FAKECODE"})

    print(f"\n[DINV] code=FAKECODE | status={response.status_code} | body={response.text}")

    assert response.status_code in [400, 404], (
        f"[APP BUG] Expected 400/404 for invalid code, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DINV-002 | Empty discount code — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_empty_discount_code(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=10.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": ""})

    print(f"\n[DINV] code='' | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Expected 400 for empty code, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DINV-010 | Apply discount to non-existent cart — expect 404")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_discount_nonexistent_cart(api_client):
    url = APPLY_DISCOUNT.format(cart_id="nonexistent-cart-00000")
    response = api_client.post(url, payload={"code": "SAVE10"})

    print(f"\n[DINV] cart=nonexistent | status={response.status_code} | body={response.text}")

    assert response.status_code == 404, (
        f"[APP BUG] Expected 404 for non-existent cart, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DISC-010 | Discount recalculates after adding new item")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_discount_recalculates_after_add(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item A", price=10.0, quantity=1)

    disc_url = APPLY_DISCOUNT.format(cart_id=cart)
    api_client.post(disc_url, payload={"code": "HALF"})

    add_item_to_cart(api_client, cart, name="Item B", price=20.0, quantity=1)

    cart_data = api_client.get(GET_CART.format(cart_id=cart)).json()
    expected = calculate_discounted_total(30.0, 50)

    print(f"\n[DISC RECALC] subtotal=30 | HALF | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] Discount not recalculated after add: expected={expected}, got {cart_data['total']}"
    )