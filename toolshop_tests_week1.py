from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com"


def test_browse_category(page):
    """Test 1: Browse Hand Tools category and verify products."""
    page.goto(BASE_URL)
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()

    title = page.locator('[data-test="page-title"]')
    expect(title).to_contain_text("Hand Tools", ignore_case=True)

    product_names = page.locator('[data-test="product-name"]').all()
    assert len(product_names) > 0, "Expected at least one product in Hand Tools"
    for product in product_names:
        name = product.inner_text().strip()
        assert name != "", f"Expected a non-empty product name, got: '{name}'"
    print("PASS: test_browse_category")


def test_product_details(page):
    """Test 2: Open first product in Hand Tools and verify detail page."""
    page.goto(BASE_URL)
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()

    first_product = page.locator('[data-test="product-name"]').first
    product_name = first_product.inner_text().strip()
    first_product.click()

    detail_name = page.locator('[data-test="product-name"]')
    expect(detail_name).to_contain_text(product_name, ignore_case=True)

    price_text = page.locator('[data-test="unit-price"]').inner_text().strip()
    assert price_text != "", "Expected a price, got empty string"

    add_to_cart = page.locator('[data-test="add-to-cart"]')
    expect(add_to_cart).to_be_visible()
    print("PASS: test_product_details")


def test_add_to_cart(page):
    """Test 3: Add first Hand Tools product to cart and verify cart."""
    page.goto(BASE_URL)
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()

    first_product = page.locator('[data-test="product-name"]').first
    product_name = first_product.inner_text().strip()
    first_product.click()

    price_text = page.locator('[data-test="unit-price"]').inner_text().strip()
    page.locator('[data-test="add-to-cart"]').click()

    cart_count = page.locator('[data-test="cart-quantity"]')
    expect(cart_count).to_have_text("1")

    page.locator('[data-test="nav-cart"]').click()

    cart_item_name = page.locator('[data-test="product-title"]').first.inner_text().strip()
    assert product_name in cart_item_name, \
        f"Expected '{product_name}' in cart, got '{cart_item_name}'"

    cart_qty = page.locator('[data-test="cart-quantity"]').first
    expect(cart_qty).to_have_value("1")

    cart_total = page.locator('[data-test="cart-total"]').inner_text().strip()
    assert price_text in cart_total or price_text.replace("$", "") in cart_total, \
        f"Expected price {price_text} in cart total {cart_total}"
    print("PASS: test_add_to_cart")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        tests = [
            ("test_browse_category", test_browse_category),
            ("test_product_details", test_product_details),
            ("test_add_to_cart", test_add_to_cart),
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
