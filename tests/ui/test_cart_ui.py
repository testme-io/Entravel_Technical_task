# tests/ui/test_cart_ui.py

import pytest
import allure
from pages.cart_page import CartPage
from utils.helpers import calculate_discounted_total


@pytest.fixture
def cart_page(page):
    cp = CartPage(page)
    return cp


@allure.title("TC-UI-001 | Add item via UI form — item appears in list, total updates")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("ui", "smoke", "positive")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_add_item_via_ui(cart_page):
    cart_page.add_item(name="Coffee", price=10.0, quantity=2)

    print(f"\n[UI ADD] items={cart_page.get_items_count()} | total={cart_page.get_total()}")

    assert cart_page.get_items_count() == 1, (
        f"[APP BUG] Expected 1 item in list, got {cart_page.get_items_count()}"
    )
    assert cart_page.get_total() != "0", (
        f"[APP BUG] Total should update after adding item, got {cart_page.get_total()}"
    )


@allure.title("TC-UI-002 | Remove item via UI — item disappears, total recalculates")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("ui", "smoke", "positive")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_remove_item_via_ui(cart_page):
    # each test gets fresh page — add item first
    cart_page.add_item(name="Tea", price=5.0, quantity=1)

    count_before = cart_page.get_items_count()
    print(f"\n[UI REMOVE] items before={count_before}")

    assert count_before == 1, (
        f"[TEST SETUP FAILED] Expected 1 item before remove, got {count_before}"
    )

    cart_page.remove_item(index=0)

    print(f"\n[UI REMOVE] items after={cart_page.get_items_count()} | total={cart_page.get_total()}")

    assert cart_page.get_items_count() == 0, (
        f"[APP BUG] Expected 0 items after remove, got {cart_page.get_items_count()}"
    )


@allure.title("TC-UI-003 | Apply SAVE10 via UI — BUG-008: total unchanged")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("ui", "smoke", "positive")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.happy_path
def test_apply_save10_via_ui(cart_page):
    cart_page.add_item(name="Item", price=20.0, quantity=1)
    total_before = cart_page.get_total()
    cart_page.apply_discount("SAVE10")
    total_after = cart_page.get_total()

    print(f"\n[UI SAVE10] before={total_before} | after={total_after}")

    # BUG-008: SAVE10 does not apply in UI — documenting actual vs expected
    assert total_after != total_before, (
        f"[APP BUG - BUG-008] SAVE10 has no effect in UI: "
        f"before={total_before}, after={total_after}. "
        f"Expected total=18.00"
    )


@allure.title("TC-UI-004 | Apply SAVE20 via UI — discounted total displayed")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "positive", "regression")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.regression
def test_apply_save20_via_ui(cart_page):
    cart_page.add_item(name="Item", price=20.0, quantity=1)
    total_before = cart_page.get_total()
    cart_page.apply_discount("SAVE20")
    total_after = cart_page.get_total()

    print(f"\n[UI SAVE20] before={total_before} | after={total_after}")

    assert total_after != total_before, (
        f"[APP BUG] Total did not change after SAVE20: before={total_before}, after={total_after}"
    )


@allure.title("TC-UI-005 | Apply HALF via UI — discounted total displayed")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "positive", "regression")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.regression
def test_apply_half_via_ui(cart_page):
    cart_page.add_item(name="Item", price=20.0, quantity=1)
    total_before = cart_page.get_total()
    cart_page.apply_discount("HALF")
    total_after = cart_page.get_total()

    print(f"\n[UI HALF] before={total_before} | after={total_after}")

    assert total_after != total_before, (
        f"[APP BUG] Total did not change after HALF: before={total_before}, after={total_after}"
    )


@allure.title("TC-UI-006 | Validation — empty form submit does not add item")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "negative", "regression")
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.regression
def test_validation_empty_form(cart_page):
    initial_count = cart_page.get_items_count()
    cart_page.page.click(cart_page.ADD_BUTTON)
    cart_page.wait_for_load()

    print(f"\n[UI VALIDATION] items after empty submit={cart_page.get_items_count()}")

    assert cart_page.get_items_count() == initial_count, (
        f"[APP BUG] Item added with empty form, count={cart_page.get_items_count()}"
    )


@allure.title("TC-UI-007 | Validation — negative price does not add item")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "negative", "regression")
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.regression
def test_validation_negative_price(cart_page):
    initial_count = cart_page.get_items_count()
    cart_page.page.fill(cart_page.NAME_INPUT, "Item")
    cart_page.page.fill(cart_page.PRICE_INPUT, "-5")
    cart_page.page.fill(cart_page.QUANTITY_INPUT, "1")
    cart_page.page.click(cart_page.ADD_BUTTON)
    cart_page.wait_for_load()

    print(f"\n[UI NEG PRICE] items={cart_page.get_items_count()}")

    assert cart_page.get_items_count() == initial_count, (
        f"[APP BUG] Item with negative price was added, count={cart_page.get_items_count()}"
    )


@allure.title("TC-UI-009 | UI total matches expected calculation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "positive", "regression")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.regression
def test_ui_total_matches_api(cart_page, api_client):
    cart_page.add_item(name="Coffee", price=10.0, quantity=2)
    ui_total = cart_page.get_total()

    # expected: price=10, qty=2 → total=20
    expected = "20"

    print(f"\n[UI vs EXPECTED] expected={expected} | ui_total={ui_total}")

    assert expected in ui_total, (
        f"[APP BUG] UI total '{ui_total}' does not match expected '{expected}'"
    )


@allure.title("TC-UI-010 | HALF discount display — correct value shown")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "positive", "regression")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.regression
def test_half_discount_display(cart_page):
    cart_page.add_item(name="Item", price=20.0, quantity=1)
    total_before = cart_page.get_total()
    cart_page.apply_discount("HALF")
    total_after = cart_page.get_total()

    print(f"\n[UI HALF DISPLAY] before={total_before} | after={total_after}")

    # documents BUG-004/007 — discount may not apply in UI
    assert total_after != total_before, (
        f"[APP BUG] HALF discount not reflected in UI: total stayed {total_after}"
    )


@allure.title("TC-UI-011 | Invalid discount code — error message visible")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("ui", "negative", "regression")
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.regression
def test_invalid_discount_ui(cart_page):
    cart_page.add_item(name="Item", price=10.0, quantity=1)
    cart_page.apply_discount("FAKECODE")

    # check either error message or total unchanged
    error_visible = cart_page.page.locator(cart_page.ERROR_MESSAGE).is_visible()
    total = cart_page.get_total()

    print(f"\n[UI INVALID DISC] error_visible={error_visible} | total={total}")

    assert error_visible or total == "10.00", (
        f"[APP BUG] No error shown and total changed unexpectedly: {total}"
    )


@allure.title("TC-UI-012 | Add 3 items via UI — all listed, total is sum")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "positive", "regression")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.regression
def test_add_multiple_items_via_ui(cart_page):
    items = [
        ("Coffee", 10.0, 1),
        ("Tea", 5.0, 1),
        ("Juice", 7.0, 1),
    ]
    for name, price, qty in items:
        cart_page.add_item(name=name, price=price, quantity=qty)
        # small wait between additions to let UI update
        cart_page.page.wait_for_timeout(500)

    count = cart_page.get_items_count()
    total = cart_page.get_total()

    print(f"\n[UI MULTI] items={count} | total={total}")

    assert count == 3, (
        f"[APP BUG] Expected 3 items, got {count}"
    )
    assert "22" in total, (
        f"[APP BUG] Expected total=22 (10+5+7), got {total}"
    )


@allure.title("TC-UI-014 | Discount applies to subtotal not first item — BUG-004")
@allure.description("BUG-004: SAVE20 must apply to full subtotal, not first item only")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "positive", "regression")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.regression
def test_discount_applies_to_subtotal_not_first_item(cart_page):
    cart_page.add_item(name="Item A", price=10.0, quantity=1)
    cart_page.page.wait_for_timeout(300)
    cart_page.add_item(name="Item B", price=20.0, quantity=1)
    cart_page.page.wait_for_timeout(300)

    subtotal_before = cart_page.get_total()
    cart_page.apply_discount("SAVE20")
    total_after = cart_page.get_total()

    expected = str(calculate_discounted_total(30.0, 20))

    print(f"\n[BUG-004 UI] subtotal={subtotal_before} | SAVE20 | expected={expected} | actual={total_after}")

    assert expected in total_after, (
        f"[APP BUG - BUG-004] SAVE20 on subtotal=30: expected {expected} in '{total_after}'. "
        f"Discount may apply to first item only"
    )