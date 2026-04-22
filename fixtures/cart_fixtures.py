
from pages.base_page import BasePage


class CartPage(BasePage):
    NAME_INPUT       = "#itemName"
    PRICE_INPUT      = "#itemPrice"
    QUANTITY_INPUT   = "#itemQuantity"
    ADD_BUTTON       = "#addItemForm button[type='submit']"
    DISCOUNT_INPUT   = "#discountCode"
    APPLY_BUTTON     = "#applyDiscount"
    SUBTOTAL_DISPLAY = "#subtotal"
    DISCOUNT_DISPLAY = "#discount"
    TOTAL_DISPLAY    = "#total"
    ITEM_LIST        = ".cart-item"
    REMOVE_BUTTON    = ".btn-danger"
    ERROR_MESSAGE    = ".error-message"

    def add_item(self, name: str, price: float, quantity: int):
        self.page.fill(self.NAME_INPUT, name)
        self.page.fill(self.PRICE_INPUT, str(price))
        self.page.fill(self.QUANTITY_INPUT, str(quantity))
        self.page.click(self.ADD_BUTTON)
        self.wait_for_load()

    def remove_item(self, index: int = 0):
        self.page.locator(self.REMOVE_BUTTON).nth(index).click()
        self.wait_for_load()

    def apply_discount(self, code: str):
        self.page.fill(self.DISCOUNT_INPUT, code)
        self.page.click(self.APPLY_BUTTON)
        self.wait_for_load()

    def get_total(self) -> str:
        return self.page.locator(self.TOTAL_DISPLAY).text_content().strip()

    def get_subtotal(self) -> str:
        return self.page.locator(self.SUBTOTAL_DISPLAY).text_content().strip()

    def get_discount(self) -> str:
        return self.page.locator(self.DISCOUNT_DISPLAY).text_content().strip()

    def get_items_count(self) -> int:
        return self.page.locator(self.ITEM_LIST).count()

    def is_error_visible(self) -> bool:
        return self.page.locator(self.ERROR_MESSAGE).is_visible()

    def get_error_message(self) -> str:
        return self.page.locator(self.ERROR_MESSAGE).text_content().strip()