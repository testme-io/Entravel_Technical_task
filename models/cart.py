from dataclasses import dataclass


@dataclass
class CartItem:
    name: str
    price: float
    quantity: int


@dataclass
class DiscountPayload:
    code: str


# -- Test data --
VALID_ITEM       = CartItem(name="Test Product", price=10.00, quantity=2)
ITEM_ODD_PRICE   = CartItem(name="Odd Price Item", price=15.00, quantity=1)
ITEM_HALF_ODD    = CartItem(name="Half Odd Item", price=7.00, quantity=1)
ITEM_FLOAT_PRICE = CartItem(name="Float Price Item", price=9.99, quantity=1)

DISCOUNT_SAVE10  = DiscountPayload(code="SAVE10")
DISCOUNT_SAVE20  = DiscountPayload(code="SAVE20")
DISCOUNT_HALF    = DiscountPayload(code="HALF")
DISCOUNT_INVALID = DiscountPayload(code="FAKECODE")