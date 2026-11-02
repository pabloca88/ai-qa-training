from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com"


def tc01_search_by_button(page):
    """TC01 - Search by clicking the search button returns results."""
    page.goto(BASE_URL)
    page.locator('[data-test="search-query"]').fill("hammer")
    page.locator('[data-test="search-submit"]').click()
    # TODO: verify the exact locator for the product list container
    products = page.locator('[data-test="product-name"]')
    expect(products.first).to_be_visible()
    count = products.count()
    assert count > 0, f"Expected products for 'hammer', got {count}"
    print("PASS: tc01_search_by_button")


def tc05_sort_high_to_low(page):
    """TC05 - Sort by price high to low shows most expensive product first."""
    page.goto(BASE_URL)
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()
    # TODO: check the exact option value for price high to low in the dropdown
    page.locator('[data-test="sort"]').select_option(label="Price (High to Low)")
    page.wait_for_load_state("networkidle")
    prices = page.locator('[data-test="product-price"]').all()
    assert len(prices) >= 2, "Expected at least 2 products to compare prices"
    first_price = float(prices[0].inner_text().replace("$", "").strip())
    second_price = float(prices[1].inner_text().replace("$", "").strip())
    assert first_price >= second_price, \
        f"Expected first price {first_price} >= second price {second_price}"
    print("PASS: tc05_sort_high_to_low")


def tc08_custom_quantity(page):
    """TC08 - Typing a custom quantity adds that quantity to the cart."""
    page.goto(BASE_URL)
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()
    page.locator('[data-test="product-name"]').first.click()
    qty_field = page.locator('[data-test="quantity"]')
    qty_field.triple_click()
    qty_field.fill("3")
    page.locator('[data-test="add-to-cart"]').click()
    page.locator('[data-test="nav-cart"]').click()
    # TODO: verify the exact locator for quantity in cart rows
    cart_qty = page.locator('[data-test="cart-quantity"]').first
    expect(cart_qty).to_have_value("3")
    print("PASS: tc08_custom_quantity")


def tc12_remove_from_cart(page):
    """TC12 - Removing the only item shows an empty cart message."""
    page.goto(BASE_URL)
    page.locator('[data-test="product-name"]').first.click()
    page.locator('[data-test="add-to-cart"]').click()
    page.locator('[data-test="nav-cart"]').click()
    # TODO: verify the remove button locator
    page.locator('[data-test="delete-product"]').first.click()
    empty_msg = page.locator('[data-test="cart-empty-message"]')
    # TODO: verify the exact text of the empty cart message
    expect(empty_msg).to_be_visible()
    print("PASS: tc12_remove_from_cart")


def tc13_contact_form_validation(page):
    """TC13 - Submitting empty contact form shows validation errors."""
    page.goto(f"{BASE_URL}/contact")
    # TODO: verify the exact locator for the Send button
    page.locator('[data-test="contact-submit"]').click()
    errors = page.locator('.invalid-feedback')
    expect(errors.first).to_be_visible()
    count = errors.count()
    assert count >= 1, f"Expected validation errors, got {count}"
    print("PASS: tc13_contact_form_validation")


def tc16_out_of_stock(page):
    """TC16 - Out of stock product cannot be added to cart."""
    page.goto(BASE_URL)
    # TODO: find an actual out-of-stock product - this searches for one
    page.locator('[data-test="search-query"]').fill("Thor")
    page.locator('[data-test="search-submit"]').click()
    page.locator('[data-test="product-name"]').first.click()
    add_btn = page.locator('[data-test="add-to-cart"]')
    is_disabled = add_btn.is_disabled() if add_btn.count() > 0 else True
    assert is_disabled, "Expected Add to cart to be disabled for out-of-stock product"
    print("PASS: tc16_out_of_stock")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()

        tests = [
            ("tc01_search_by_button", tc01_search_by_button),
            ("tc05_sort_high_to_low", tc05_sort_high_to_low),
            ("tc08_custom_quantity", tc08_custom_quantity),
            ("tc12_remove_from_cart", tc12_remove_from_cart),
            ("tc13_contact_form_validation", tc13_contact_form_validation),
            ("tc16_out_of_stock", tc16_out_of_stock),
        ]

        results = []
        for name, test_fn in tests:
            try:
                test_fn(page)
                results.append((name, "PASS"))
            except Exception as e:
                print(f"FAIL: {name} -- {e}")
                results.append((name, "FAIL"))

        browser.close()

        print("\n--- Results ---")
        any_failed = False
        for name, result in results:
            print(f"{result}: {name}")
            if result == "FAIL":
                any_failed = True
        if any_failed:
            exit(1)


if __name__ == "__main__":
    main()
