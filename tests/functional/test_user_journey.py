"""Functional (Selenium) tests exercising the app through a real browser."""

import pytest

selenium = pytest.importorskip("selenium")
from selenium import webdriver  # noqa: E402
from selenium.webdriver.chrome.options import Options  # noqa: E402
from selenium.webdriver.common.by import By  # noqa: E402

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture
def browser():
    """Headless Chrome instance, closed after the test."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


@pytest.mark.functional
class TestUserJourney:
    """A handful of browser-driven end-to-end scenarios."""

    def test_login_and_see_welcome_page(self, browser):
        """A valid email logs in and shows the welcome page with the club name."""
        browser.get(BASE_URL)
        browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
        browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

        assert "Welcome" in browser.page_source
        assert "john@simplylift.co" in browser.page_source

    def test_points_board_is_accessible_without_login(self, browser):
        """The points board is reachable directly, no login required."""
        browser.get(f"{BASE_URL}/points-board")

        assert "Club Points Board" in browser.page_source
        assert "Simply Lift" in browser.page_source
        assert "Iron Temple" in browser.page_source
