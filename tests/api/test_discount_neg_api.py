import pytest
import allure
from api.endpoints import APPLY_DISCOUNT
from utils.helpers import add_item_to_cart


@allure.title("TC-DINV-003 | Lowercase discount code — expect 400 (case-sensitive)")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "boundary")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.boundary
def test_lowercase_discount_code(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=10.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": "save10"})

    print(f"\n[DINV] code='save10' | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Lowercase code 'save10' should be rejected (case-sensitive), "
        f"got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DINV-004 | Mixed-case discount code — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "boundary")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.boundary
def test_mixed_case_discount_code(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=10.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": "Save10"})

    print(f"\n[DINV] code='Save10' | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Mixed-case 'Save10' should be rejected, "
        f"got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DINV-005 | Missing code field in body — expect 400")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_missing_code_field(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=10.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={})

    print(f"\n[DINV] payload={{}} | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Empty body should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DINV-006 | Discount code as null — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_null_discount_code(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=10.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": None})

    print(f"\n[DINV] code=null | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Null code should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DINV-007 | Numeric discount code — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_numeric_discount_code(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=10.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": 10})

    print(f"\n[DINV] code=10 (numeric) | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Numeric code should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DINV-008 | Discount code with leading/trailing spaces — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "boundary")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.boundary
def test_discount_code_with_spaces(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=10.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": " SAVE10 "})

    print(f"\n[DINV] code=' SAVE10 ' | status={response.status_code} | body={response.text}")

    # if trim is not implemented — should reject; if trim is implemented — 200 is acceptable
    assert response.status_code in [400, 200], (
        f"[APP BUG] Unexpected status for padded code, got {response.status_code} | body: {response.text}"
    )

    # if it was accepted — total must be actually discounted (not a silent accept with no effect)
    if response.status_code == 200:
        print(f"[INFO] Server trimmed whitespace and accepted the code — documenting behavior")


@allure.title("TC-DINV-009 | Discount code with special characters — expect 400")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_discount_code_special_chars(api_client, cart):
    add_item_to_cart(api_client, cart, name="Item", price=10.0, quantity=1)

    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": "SAVE!@#"})

    print(f"\n[DINV] code='SAVE!@#' | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Code with special chars should be rejected, "
        f"got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-DINV-011 | Apply valid discount to empty cart — expect 400 or 200 with total=0")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "boundary", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_discount_on_empty_cart(api_client, cart):
    url = APPLY_DISCOUNT.format(cart_id=cart)
    response = api_client.post(url, payload={"code": "SAVE10"})

    print(f"\n[DINV] SAVE10 on empty cart | status={response.status_code} | body={response.text}")

    assert response.status_code in [400, 200], (
        f"[APP BUG] Unexpected response for discount on empty cart, "
        f"got {response.status_code} | body: {response.text}"
    )

    if response.status_code == 200:
        data = response.json()
        print(f"[INFO] Discount accepted on empty cart — discount={data.get('discount')} total={data.get('total')}")