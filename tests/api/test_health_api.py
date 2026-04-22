import pytest
import allure
from api.endpoints import HEALTH


@allure.title("TC-CART-011 | Health check — service is available")
@allure.description("Verify the API service is available and returns 200 OK with healthy status")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "positive")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.positive
def test_health_check(api_client):
    response = api_client.get(HEALTH)

    print(f"\n[HEALTH] status={response.status_code} | body={response.text}")

    assert response.status_code == 200, (
        f"[APP BUG] Health check failed: expected 200, got {response.status_code} | body: {response.text}"
    )

    data = response.json()

    assert "status" in data, (
        f"[APP BUG] Response missing 'status' field | got: {data}"
    )
    assert data["status"].lower() == "ok", (
        f"[APP BUG] Expected status='ok', got '{data['status']}'"
    )