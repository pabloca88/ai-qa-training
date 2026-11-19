# Week 3 AI Prompt

## Context

I am automating tests for https://practicesoftwaretesting.com using Playwright with Python
and pytest. The site sells tools. A product detail page has a quantity field
(data-test="quantity") and an Add to Cart button (data-test="add-to-cart").
The cart page shows each item's quantity in an input (data-test="product-quantity")
and a nav badge (data-test="cart-quantity") with the total item count.

## Scenario

Based on this existing test:

```python
def tc08_custom_quantity(page):
    page.goto("https://practicesoftwaretesting.com")
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()
    page.locator('[data-test="product-name"]').first.click()
    qty_field = page.locator('[data-test="quantity"]')
    qty_field.triple_click()
    qty_field.fill("3")
    page.locator('[data-test="add-to-cart"]').click()
    page.locator('[data-test="nav-cart"]').click()
    cart_qty = page.locator('[data-test="product-quantity"]').first
    expect(cart_qty).to_have_value("3")
```

Generate three things:

1. A file data.csv with at least 6 rows. Columns: quantity, expected_cart_value, expect_added.
   Include: quantities 1, 3, 5, 0, -1, and "abc". The last three should have
   expect_added=false because the site rejects or ignores them.

2. A pytest parametrized test test_quantity that reads data.csv with csv.DictReader,
   uses @pytest.mark.parametrize, opens the first Hand Tools product, sets the quantity,
   clicks Add to Cart, and if expect_added is true checks that data-test="product-quantity"
   shows the expected value in the cart; if false checks the item was NOT added
   (cart-quantity badge stays at 0 or the cart page shows no rows).
   Use expect() for page assertions, plain assert for Python values. No time.sleep.

3. A test test_api_product that calls GET https://api.practicesoftwaretesting.com/products?page=1
   with the requests library, asserts status 200, asserts the response has keys
   "data", "total", and "per_page", picks the first product from data[], then
   navigates to that product's page on the site and compares the product name
   shown in data-test="product-name" with the name field from the API response.

## Rules

- pytest -v must list every CSV row as its own test line.
- No time.sleep anywhere.
- Use expect() for Playwright assertions, plain assert for Python/API values.
- Never click the Send button on any form.
- helpers.py provides the browser fixture; import it.
