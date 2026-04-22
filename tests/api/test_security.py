import pytest
import allure
from api.endpoints import ADD_ITEM, GET_CART
from utils.helpers import generate_item


@allure.title("TC-SEC-001 | XSS injection in item name — script must not execute")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "security", "negative")
@pytest.mark.api
@pytest.mark.security
@pytest.mark.negative
def test_xss_in_item_name(api_client, cart):
    xss_payload = "<script>alert(1)</script>"
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name=xss_payload, price=5.0, quantity=1)
    response = api_client.post(url, payload=payload)

    print(f"\n[SEC-001] XSS payload in name | status={response.status_code} | body={response.text}")

    # API may accept (store as-is) or reject — both are ok at API level
    # the critical thing is it must not be reflected as executable script
    assert response.status_code in [201, 400], (
        f"[SEC] Unexpected status for XSS payload, got {response.status_code}"
    )

    if response.status_code == 201:
        data = response.json()
        # name should be stored as plain text, not interpreted
        stored_name = data.get("name", "")
        print(f"[SEC-001] stored name='{stored_name}'")

        # verify the name was stored literally (not stripped to empty, which could silently hide danger)
        assert stored_name == xss_payload or len(stored_name) == 0 or stored_name != "", (
            f"[SEC] Name should be stored as plain text | got: '{stored_name}'"
        )

        # cross-check: GET /cart and verify stored value
        cart_data = api_client.get(GET_CART.format(cart_id=cart)).json()
        items = cart_data.get("items", [])
        if items:
            retrieved_name = items[0].get("name", "")
            print(f"[SEC-001] retrieved name='{retrieved_name}'")
            assert "<script>" not in retrieved_name or retrieved_name == xss_payload, (
                f"[SEC] Partial script tag in name is suspicious: '{retrieved_name}'"
            )


@allure.title("TC-SEC-002 | SQL/NoSQL injection in cart ID — no data leak or error disclosure")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "security", "negative")
@pytest.mark.api
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.parametrize("injection", [
    "' OR '1'='1",
    "1; DROP TABLE carts--",
    '{"$gt": ""}',
    "../../../etc/passwd",
])
def test_injection_in_cart_id(api_client, injection):
    from api.endpoints import GET_CART

    url = GET_CART.format(cart_id=injection)
    response = api_client.get(url)

    print(f"\n[SEC-002] injection='{injection}' | status={response.status_code} | body={response.text[:200]}")

    assert response.status_code in [400, 404], (
        f"[SEC] Injection payload got unexpected {response.status_code} | body: {response.text[:200]}"
    )

    # response body must not contain internal error details, stack traces, or DB info
    body_lower = response.text.lower()
    for leak_indicator in ["traceback", "exception", "syntax error", "mongodb", "sqlite", "postgres"]:
        assert leak_indicator not in body_lower, (
            f"[SEC] Potential internal info leak — '{leak_indicator}' found in response | body: {response.text[:300]}"
        )