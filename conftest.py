import pytest
from playwright.sync_api import sync_playwright
from api.client import APIClient
from api.endpoints import CREATE_CART, ADD_ITEM, APPLY_DISCOUNT
from config.settings import BASE_URL, HEADLESS
from utils.helpers import generate_item


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def cart(api_client):
    response = api_client.post(CREATE_CART)
    assert response.status_code == 201, (
        f"[TEST SETUP FAILED] Could not create cart | got {response.status_code}: {response.text}"
    )
    return response.json()["cartId"]


@pytest.fixture
def cart_with_item(api_client, cart):
    url = ADD_ITEM.format(cart_id=cart)
    payload = generate_item(name="Test Item", price=100.0, quantity=1)
    response = api_client.post(url, payload=payload)

    assert response.status_code == 201, (
        f"[TEST SETUP FAILED] Could not add item | got {response.status_code}: {response.text}"
    )
    item_id = response.json()["id"]
    return cart, item_id


@pytest.fixture
def cart_with_discount(api_client, cart_with_item):
    cart_id, item_id = cart_with_item
    url = APPLY_DISCOUNT.format(cart_id=cart_id)
    response = api_client.post(url, payload={"code": "SAVE10"})

    assert response.status_code == 200, (
        f"[TEST SETUP FAILED] Could not apply discount | got {response.status_code}: {response.text}"
    )
    return cart_id, item_id



@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context(base_url=BASE_URL)
    context.set_default_timeout(10000)
    pg = context.new_page()
    pg.goto("/")
    yield pg
    context.close()