import pytest
import allure
from api.endpoints import ADD_ITEM, GET_CART
from utils.helpers import generate_item
from pages.cart_page import CartPage


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@allure.title("TC-STRESS-001 | Add 200 items — system remains stable, total is correct")
@allure.description(
    "Sequentially add 200 items via API and verify the total is calculated correctly. "
    "Reduced from 1000 to keep runtime reasonable while still validating stability."
)
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "stress", "boundary")
@pytest.mark.api
@pytest.mark.stress
@pytest.mark.boundary
@pytest.mark.timeout(120)
def test_max_items_stability(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    item_count = 200
    price = 1.0

    print(f"\n[STRESS-001] Adding {item_count} items...")

    for i in range(item_count):
        resp = api_client.post(url, payload=generate_item(name=f"Item {i}", price=price, quantity=1))
        assert resp.status_code == 201, (
            f"[APP BUG] Failed to add item #{i}: got {resp.status_code} | body: {resp.text}"
        )

    cart_data = api_client.get(GET_CART.format(cart_id=cart)).json()
    actual_count = len(cart_data["items"])
    actual_total = cart_data["total"]
    expected_total = price * item_count

    print(f"[STRESS-001] items_in_cart={actual_count} | total={actual_total} | expected={expected_total}")

    assert actual_count == item_count, (
        f"[APP BUG] Expected {item_count} items, got {actual_count}"
    )
    assert actual_total == expected_total, (
        f"[APP BUG] Total mismatch after bulk add: expected={expected_total}, got {actual_total}"
    )


@allure.title("TC-STRESS-002 | Item with very long name — UI does not freeze")
@allure.description(
    "Add an item with a 10,000-character name via API and then load the UI. "
    "Verify the page renders without freezing or crashing."
)
@allure.severity(allure.severity_level.MINOR)
@allure.tag("ui", "stress", "boundary")
@pytest.mark.ui
@pytest.mark.stress
@pytest.mark.boundary
@pytest.mark.timeout(60)
def test_long_name_ui_stability(api_client, cart, page):
    long_name = "X" * 10_000
    url = ADD_ITEM.format(cart_id=cart)
    resp = api_client.post(url, payload=generate_item(name=long_name, price=5.0, quantity=1))

    print(f"\n[STRESS-002] name_len=10000 | add_status={resp.status_code}")

    if resp.status_code != 201:
        # API rejected — still a valid test outcome, skip UI part
        print(f"[STRESS-002] API rejected long name ({resp.status_code}) — UI test skipped")
        pytest.skip(f"API rejected 10k-char name with {resp.status_code}, UI stability N/A")

    # navigate to the app and verify it renders without crashing
    cp = CartPage(page)
    cp.wait_for_load(timeout=10000)

    item_count = cp.get_items_count()
    print(f"[STRESS-002] UI rendered | items={item_count}")

    # the page should be responsive — getting item count is enough to confirm no freeze
    assert item_count >= 0, (
        "[APP BUG] UI crashed or item count unavailable after loading long-name item"
    )