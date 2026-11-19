import csv
from pathlib import Path

import pytest
import requests
from playwright.sync_api import expect

from helpers import BASE_URL, page  # noqa: F401  (page is the browser fixture)

API_URL = "https://api.practicesoftwaretesting.com"
DATA_FILE = Path(__file__).parent / "data.csv"


def load_rows():
    with open(DATA_FILE, newline="") as f:
        return list(csv.DictReader(f))


ROWS = load_rows()


def open_first_hand_tool(page):
    page.goto(BASE_URL)
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()
    page.locator('[data-test="product-name"]').first.click()


@pytest.mark.parametrize("row", ROWS, ids=[f"qty={r['quantity']}" for r in ROWS])
def test_quantity(page, row):
    """Data-driven version of tc08: each CSV row sets a quantity and checks the cart."""
    expect_added = row["expect_added"].strip().lower() == "true"

    open_first_hand_tool(page)
    qty_field = page.locator('[data-test="quantity"]')
    if row["quantity"].lstrip("-").isdigit():
        qty_field.fill(row["quantity"])
    else:
        # fill() raises on letters in a number input, so type them like a user would.
        # Locator has no triple_click(); click_count=3 selects the current value first.
        qty_field.click(click_count=3)
        qty_field.press_sequentially(row["quantity"])
    page.locator('[data-test="add-to-cart"]').click()

    badge = page.locator('[data-test="cart-quantity"]')
    if expect_added:
        expect(badge).to_have_text(row["expected_cart_value"])
        page.locator('[data-test="nav-cart"]').click()
        cart_qty = page.locator('[data-test="product-quantity"]').first
        expect(cart_qty).to_have_value(row["expected_cart_value"])
    else:
        expect(badge).to_have_count(0)
        page.goto(f"{BASE_URL}/checkout")
        expect(page.locator('[data-test="product-quantity"]')).to_have_count(0)


def test_api_product(page):
    """The first product from the API shows the same name on its product page."""
    response = requests.get(f"{API_URL}/products?page=1", timeout=30)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    body = response.json()
    for key in ("data", "total", "per_page"):
        assert key in body, f"Response is missing key '{key}'"
    assert len(body["data"]) > 0, "API returned no products"

    product = body["data"][0]
    page.goto(f"{BASE_URL}/product/{product['id']}")
    expect(page.locator('[data-test="product-name"]')).to_have_text(product["name"])
