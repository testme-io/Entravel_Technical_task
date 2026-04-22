import pytest
import allure
from api.endpoints import CREATE_CART, GET_CART


@allure.title("TC-CART-009 | Get cart with special characters in ID — expect 400 or 404")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "negative", "boundary", "regression")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_get_cart_special_chars_id(api_client):
    url = GET_CART.format(cart_id="abc!@#")
    response = api_client.get(url)

    print(f"\n[CART SPECIAL ID] status={response.status_code} | body={response.text}")

    assert response.status_code in [400, 404], (
        f"[APP BUG] Expected 400 or 404 for special chars in ID, got {response.status_code}"
    )


@allure.title("TC-CART-012 | POST /cart with extra body fields — should be ignored or rejected")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "boundary", "regression")
@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.regression
def test_create_cart_extra_fields(api_client):
    response = api_client.post(CREATE_CART, payload={"foo": "bar", "extra": 123})

    print(f"\n[CART EXTRA FIELDS] status={response.status_code} | body={response.text}")

    # extra fields should either be silently ignored (201) or rejected (400)
    assert response.status_code in [201, 400], (
        f"[APP BUG] Unexpected response with extra body fields, got {response.status_code}"
    )

    if response.status_code == 201:
        data = response.json()
        assert "cartId" in data, (
            f"[APP BUG] cartId missing in response even though extra fields were accepted | got: {data}"
        )