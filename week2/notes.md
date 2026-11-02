# Week 2 Notes

## Questions for the shop owner

1. Requirement 1.3 mentions a "small clear button next to the search box" - there is an X
   icon that appears after typing. Is that the clear button, or is there a separate one?
2. Requirement 5.1 says no message has been decided for out-of-stock products. Which
   products are currently out of stock so we can test against them without hardcoding names?
3. Requirement 3.2 says the cart icon count should update when changing quantity in the
   cart - does it update live or only after clicking an Update button?

## Three things the AI got wrong

1. **Wrong locator for cart quantity in tc08**: The assistant used
   `[data-test="cart-quantity"]` for the quantity input inside the cart, but that locator
   is the cart icon badge on the nav bar, not the editable quantity field inside the cart
   rows. The correct locator is `[data-test="product-quantity"]`.

2. **Hardcoded product name for out-of-stock in tc16**: The assistant searched for "Thor"
   to find an out-of-stock product. If the store data changes, that product might come
   back in stock or disappear. The right approach is to look for the out-of-stock
   indicator on the product list page instead of assuming a specific name.

3. **Used wait_for_load_state("networkidle") in tc05**: The assistant added a networkidle
   wait after selecting the sort dropdown. This is unreliable in Playwright and can time
   out or pass too early. The correct pattern is to use expect() on the first product
   after sorting so the check itself acts as the wait.

## One thing the AI got right

The AI correctly identified that prices in the cart include a dollar sign while prices on
the product page do not, and used .replace("$", "") to handle the comparison. This matched
the hint in the assignment and saved debugging time.
