import pytest
import allure
from api.endpoints import GET_CART, APPLY_DISCOUNT
from utils.helpers import calculate_discounted_total, add_item_to_cart


def apply_and_get(api_client, cart_id, code):
    url = APPLY_DISCOUNT.format(cart_id=cart_id)
    resp = api_client.post(url, payload={"code": code})
    cart = api_client.get(GET_CART.format(cart_id=cart_id)).json()
    return resp, cart


@allure.title("TC-DCALC-003 | SAVE20 on even subtotal — floor(50 * 0.8) = 40")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_save20_even_subtotal(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=50.0, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "SAVE20")
    expected = calculate_discounted_total(50.0, 20)

    print(f"\n[DCALC-003] subtotal=50 | SAVE20 | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] SAVE20 on 50: expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DCALC-004 | SAVE20 on odd subtotal — floor(25 * 0.8) = 20")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "boundary", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.boundary
@pytest.mark.regression
def test_save20_odd_subtotal_floor(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=25.0, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "SAVE20")
    expected = calculate_discounted_total(25.0, 20)

    print(f"\n[DCALC-004] subtotal=25 | SAVE20 | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] SAVE20 on 25: expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DCALC-005 | HALF on even subtotal — floor(20 * 0.5) = 10")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_half_even_subtotal(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=20.0, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "HALF")
    expected = calculate_discounted_total(20.0, 50)

    print(f"\n[DCALC-005] subtotal=20 | HALF | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] HALF on 20: expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DCALC-007 | HALF on minimum subtotal — floor(1 * 0.5) = 0")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_half_minimum_subtotal(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=1.0, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "HALF")
    expected = calculate_discounted_total(1.0, 50)  # floor(0.5) = 0

    print(f"\n[DCALC-007] subtotal=1 | HALF | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] HALF on 1: expected={expected} (floor(0.5)=0), got {cart_data['total']}"
    )


@allure.title("TC-DCALC-008 | Recalculation when SAVE10 is replaced by SAVE20")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_recalculation_on_code_override(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=100.0, quantity=1)

    disc_url = APPLY_DISCOUNT.format(cart_id=cart)
    api_client.post(disc_url, payload={"code": "SAVE10"})

    _, cart_data = apply_and_get(api_client, cart, "SAVE20")
    expected = calculate_discounted_total(100.0, 20)

    print(f"\n[DCALC-008] subtotal=100 | SAVE10->SAVE20 | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] After override SAVE10->SAVE20: expected={expected}, got {cart_data['total']}"
    )
    assert cart_data.get("discountCode") == "SAVE20", (
        f"[APP BUG] Expected discountCode='SAVE20', got {cart_data.get('discountCode')}"
    )


@allure.title("TC-DCALC-010 | Discount amount integrity — response field matches math")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_discount_amount_integrity(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=100.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    resp = api_client.post(url, payload={"code": "SAVE20"})
    data = resp.json()

    cart_data = api_client.get(GET_CART.format(cart_id=cart)).json()

    subtotal = 100.0
    expected_total = calculate_discounted_total(subtotal, 20)  # 80
    expected_discount = subtotal - expected_total  # 20

    print(
        f"\n[DCALC-010] subtotal={subtotal} | SAVE20 | "
        f"expected_total={expected_total} | expected_discount={expected_discount} | "
        f"actual_total={cart_data.get('total')} | actual_discount={cart_data.get('discount')}"
    )

    assert cart_data["total"] == expected_total, (
        f"[APP BUG] Total mismatch: expected={expected_total}, got {cart_data['total']}"
    )

    # discount field should match the mathematical difference
    actual_discount = cart_data.get("discount")
    assert actual_discount == expected_discount, (
        f"[APP BUG] Discount amount mismatch: expected={expected_discount}, got {actual_discount}"
    )


@allure.title("TC-DISC-006 | Re-apply the same code — total remains unchanged")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_reapply_same_code(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=100.0, quantity=1)

    disc_url = APPLY_DISCOUNT.format(cart_id=cart)
    api_client.post(disc_url, payload={"code": "SAVE10"})

    cart_after_first = api_client.get(GET_CART.format(cart_id=cart)).json()
    total_after_first = cart_after_first["total"]

    api_client.post(disc_url, payload={"code": "SAVE10"})

    cart_after_second = api_client.get(GET_CART.format(cart_id=cart)).json()
    total_after_second = cart_after_second["total"]

    print(
        f"\n[DISC-006] SAVE10 x2 | after_first={total_after_first} | after_second={total_after_second}"
    )

    assert total_after_second == total_after_first, (
        f"[APP BUG] Re-applying same code changed the total: "
        f"first={total_after_first}, second={total_after_second}"
    )


@allure.title("TC-DISC-007 | Discount on single-item cart — correct calculation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_discount_single_item_cart(api_client, cart):
    add_item_to_cart(api_client, cart, name="Solo Item", price=30.0, quantity=1)

    _, cart_data = apply_and_get(api_client, cart, "SAVE20")
    expected = calculate_discounted_total(30.0, 20)

    print(f"\n[DISC-007] single item subtotal=30 | SAVE20 | expected={expected} | actual={cart_data.get('total')}")

    assert cart_data["total"] == expected, (
        f"[APP BUG] SAVE20 on single-item cart: expected={expected}, got {cart_data['total']}"
    )


@allure.title("TC-DISC-008 | Discount on multi-item cart — applied to combined subtotal")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "regression")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
def test_discount_multi_item_cart(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item A", price=10.0, quantity=1)
    add_item_to_cart(api_client, cart, name="Item B", price=15.0, quantity=1)
    add_item_to_cart(api_client, cart, name="Item C", price=25.0, quantity=1)

    subtotal = 50.0
    _, cart_data = apply_and_get(api_client, cart, "SAVE10")
    expected = calculate_discounted_total(subtotal, 10)

    print(
        f"\n[DISC-008] 3 items | subtotal={subtotal} | SAVE10 | "
        f"expected={expected} | actual={cart_data.get('total')}"
    )

    assert cart_data["total"] == expected, (
        f"[APP BUG] SAVE10 on multi-item cart: subtotal={subtotal}, expected={expected}, got {cart_data['total']}"
    )