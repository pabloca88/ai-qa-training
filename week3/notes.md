# Week 3 Notes

## How to run

source .venv/bin/activate
cd week3
pytest -v

## Review against prompt.md

| Requirement | Status |
| --- | --- |
| data.csv has at least 6 rows with quantity, expected_cart_value, expect_added | Done (7 rows) |
| Includes 1, 3, 5, 0, -1 and "abc" | Done, plus 100 as an upper boundary |
| 0, -1 and "abc" have expect_added=false | Changed, see below |
| test_quantity reads data.csv with csv.DictReader and uses @pytest.mark.parametrize | Done |
| Opens first Hand Tools product, sets quantity, clicks Add to Cart | Done |
| expect_added=true checks data-test="product-quantity" in the cart | Done |
| expect_added=false checks the item was not added | Done (badge absent and no cart rows), no CSV row uses it today |
| test_api_product: status 200, keys data/total/per_page, first product name matches the page | Done |
| pytest -v lists every CSV row as its own line | Done (test_quantity[chromium-qty=...]) |
| No time.sleep | Done |
| expect() for page checks, assert for Python/API values | Done |
| Never click Send on a form | Done (no forms used) |
| Use the browser fixture from helpers.py | Done |

## Things the prompt assumed that were wrong

1. **The site does not reject invalid quantities.** The prompt says 0, -1 and "abc" should
   not be added. On the real site the quantity field is `type=number` with `min=1` and the
   app clamps the value to 1-99: 0, -1, empty and "abc" become 1, 2.5 becomes 2, and 100
   becomes 99 with the message "You can order at most 99 of this product." The item is
   always added. data.csv uses the real behavior (expected_cart_value=1, expect_added=true)
   so the tests check what the site does instead of failing on a wrong assumption.

2. **`triple_click()` does not exist in Playwright Python.** The tc08 example in the prompt
   (and week2/tests.py) calls `qty_field.triple_click()`, which raises AttributeError.
   The Python API is `click(click_count=3)`.

3. **`fill("abc")` cannot work on a number input.** Playwright raises
   "Cannot type text into input[type=number]". The test types non-numeric values with
   `press_sequentially()`, which is what a real user does.

## Things we hit while running

- Clearing the field with `fill("")` and then typing does not work: the app puts 1 back as
  soon as the field is empty, so typing "1" gives "11". Numbers are set with `fill()`.
- practicesoftwaretesting.com is a shared demo and resets its database. During one reset
  the API returned 500 and then `total: 0` for about a minute, and some page loads took
  over 30 seconds. A full run can fail on timeouts while the site is slow; every test
  passed when re-run.

## Question for the shop owner

Should an invalid quantity (0, negative, letters) be silently changed to 1, or should the
shop show an error and refuse to add it? Today it silently adds 1 item.
