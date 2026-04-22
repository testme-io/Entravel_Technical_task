import pytest
import allure
from pages.cart_page import CartPage


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@allure.title("TC-UI-008 | Validation — zero quantity does not add item")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "negative", "regression")
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.regression
def test_validation_zero_quantity(cart_page):
    initial_count = cart_page.get_items_count()

    cart_page.page.fill(cart_page.NAME_INPUT, "Item")
    cart_page.page.fill(cart_page.PRICE_INPUT, "10")
    cart_page.page.fill(cart_page.QUANTITY_INPUT, "0")
    cart_page.page.click(cart_page.ADD_BUTTON)
    cart_page.wait_for_load()

    count_after = cart_page.get_items_count()

    print(f"\n[UI-008] initial={initial_count} | after zero qty submit={count_after}")

    assert count_after == initial_count, (
        f"[APP BUG] Item with quantity=0 was added to cart, count went from {initial_count} to {count_after}"
    )


@allure.title("TC-UI-013 | Clear entire cart via UI — list empty, total is 0")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("ui", "positive", "regression")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.regression
def test_clear_all_items_via_ui(cart_page):
    items = [("Coffee", 10.0, 1), ("Tea", 5.0, 1), ("Juice", 7.0, 1)]
    for name, price, qty in items:
        cart_page.add_item(name=name, price=price, quantity=qty)
        cart_page.page.wait_for_timeout(400)

    count_before = cart_page.get_items_count()
    print(f"\n[UI-013] items before clear={count_before}")

    assert count_before == 3, (
        f"[TEST SETUP FAILED] Expected 3 items before clearing, got {count_before}"
    )

    # remove all items one by one — always click index 0 since list shifts after each removal
    for _ in range(count_before):
        cart_page.remove_item(index=0)
        cart_page.page.wait_for_timeout(400)

    count_after = cart_page.get_items_count()
    total_after = cart_page.get_total()

    print(f"[UI-013] items after clear={count_after} | total={total_after}")

    assert count_after == 0, (
        f"[APP BUG] Expected 0 items after clearing cart, got {count_after}"
    )
    assert "0" in total_after, (
        f"[APP BUG] Expected total to show 0 after clearing, got '{total_after}'"
    )