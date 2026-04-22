import pytest
import allure
from api.endpoints import ADD_ITEM
from utils.helpers import generate_item


@allure.title("TC-INV-014 | Price as null — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_null_price(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": "Item", "price": None, "quantity": 1}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] price=null | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Null price should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-015 | Quantity as null — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_null_quantity(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": "Item", "price": 10.0, "quantity": None}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] quantity=null | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Null quantity should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-016 | Name as null — expect 400")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_null_name(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = {"name": None, "price": 10.0, "quantity": 1}
    response = api_client.post(url, payload=payload)

    print(f"\n[NEG] name=null | status={response.status_code} | body={response.text}")

    assert response.status_code == 400, (
        f"[APP BUG] Null name should be rejected, got {response.status_code} | body: {response.text}"
    )


@allure.title("TC-INV-018 | Extremely large price — system stability check")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_extremely_large_price(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name="Expensive", price=9_999_999_999.99, quantity=1)
    response = api_client.post(url, payload=payload)

    print(f"\n[BOUNDARY] price=9_999_999_999.99 | status={response.status_code} | body={response.text}")

    assert response.status_code in [201, 400], (
        f"[APP BUG] Unexpected status for huge price, got {response.status_code}"
    )


@allure.title("TC-INV-019 | Extremely large quantity — system stability check")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_extremely_large_quantity(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name="Bulk", price=1.0, quantity=9_999_999)
    response = api_client.post(url, payload=payload)

    print(f"\n[BOUNDARY] quantity=9_999_999 | status={response.status_code} | body={response.text}")

    assert response.status_code in [201, 400], (
        f"[APP BUG] Unexpected status for huge quantity, got {response.status_code}"
    )


@allure.title("TC-INV-020 | Non-JSON payload — expect 400 or 415")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "negative", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_non_json_payload(api_client, cart):
    import requests
    from config.settings import BASE_URL
    from api.endpoints import ADD_ITEM

    url = BASE_URL + ADD_ITEM.format(cart_id=cart)
    response = requests.post(
        url,
        data="this is plain text, not json",
        headers={"Content-Type": "text/plain"}
    )

    print(f"\n[NEG] non-json payload | status={response.status_code} | body={response.text}")

    assert response.status_code in [400, 415], (
        f"[APP BUG] Non-JSON payload should be rejected with 400 or 415, "
        f"got {response.status_code} | body: {response.text}"
    )