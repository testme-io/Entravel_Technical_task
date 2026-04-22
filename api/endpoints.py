from config.settings import BASE_URL

HEALTH          = f"{BASE_URL}/health"
CREATE_CART     = f"{BASE_URL}/cart"
GET_CART        = f"{BASE_URL}/cart/{{cart_id}}"
ADD_ITEM        = f"{BASE_URL}/cart/{{cart_id}}/items"
DELETE_ITEM     = f"{BASE_URL}/cart/{{cart_id}}/items/{{item_id}}"
APPLY_DISCOUNT  = f"{BASE_URL}/cart/{{cart_id}}/discount"