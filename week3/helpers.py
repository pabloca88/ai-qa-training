import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://practicesoftwaretesting.com"


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        pg = context.new_page()
        yield pg
        context.close()
        browser.close()
