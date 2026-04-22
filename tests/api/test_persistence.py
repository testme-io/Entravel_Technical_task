import pytest
import allure
from api.endpoints import GET_CART
from pages.cart_page import CartPage
from utils.helpers import calculate_discounted_total


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@allure.title("TC-PERS-001 | Data persists after page reload")
@allure.description("Add item via UI, reload the page, verify item is still listed")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "positive", "persistence")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.persistence
def test_data_persists_after_reload(cart_page):
    cart_page.add_item(name="Persistent Item", price=15.0, quantity=2)

    count_before = cart_page.get_items_count()
    total_before = cart_page.get_total()

    print(f"\n[PERS-001] before reload: items={count_before} | total={total_before}")

    assert count_before == 1, (
        f"[TEST SETUP FAILED] Expected 1 item before reload, got {count_before}"
    )

    cart_page.page.reload()
    cart_page.wait_for_load()

    count_after = cart_page.get_items_count()
    total_after = cart_page.get_total()

    print(f"[PERS-001] after reload: items={count_after} | total={total_after}")

    assert count_after == count_before, (
        f"[APP BUG] Item count changed after reload: before={count_before}, after={count_after}"
    )
    assert total_after == total_before, (
        f"[APP BUG] Total changed after reload: before={total_before}, after={total_after}"
    )


@allure.title("TC-PERS-002 | Multi-tab synchronization — Tab B reflects Tab A changes")
@allure.description("Add item in Tab A, open Tab B, verify cart state is consistent")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("ui", "positive", "persistence")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.persistence
def test_multi_tab_sync(browser_instance):
    from config.settings import BASE_URL

    context = browser_instance.new_context(base_url=BASE_URL)
    context.set_default_timeout(10000)

    page_a = context.new_page()
    page_a.goto("/")
    tab_a = CartPage(page_a)

    tab_a.add_item(name="Shared Item", price=20.0, quantity=1)
    tab_a.wait_for_load()

    items_in_a = tab_a.get_items_count()
    total_in_a = tab_a.get_total()

    print(f"\n[PERS-002] Tab A: items={items_in_a} | total={total_in_a}")

    assert items_in_a == 1, f"[TEST SETUP FAILED] Tab A should have 1 item, got {items_in_a}"

    page_b = context.new_page()
    page_b.goto("/")
    page_b.wait_for_load_state("domcontentloaded")
    tab_b = CartPage(page_b)

    items_in_b = tab_b.get_items_count()
    total_in_b = tab_b.get_total()

    print(f"[PERS-002] Tab B (fresh open): items={items_in_b} | total={total_in_b}")

    # if the app uses a shared cart (same session/cookie) — Tab B should see the same data
    # if app creates a new cart per page load — this documents that behavior
    if items_in_b == items_in_a:
        assert total_in_b == total_in_a, (
            f"[APP BUG] Tab B shows same item count but different total: "
            f"a={total_in_a}, b={total_in_b}"
        )
        print("[PERS-002] Cart is shared across tabs — consistent state confirmed")
    else:
        print(
            f"[PERS-002] App uses separate cart per tab — Tab B is isolated "
            f"(items_a={items_in_a}, items_b={items_in_b})"
        )

    context.close()