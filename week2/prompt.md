# Week 2 AI Prompt

## Context
- Language: Python
- Library: Playwright sync API
- Site: https://practicesoftwaretesting.com
- I am writing automated tests for a QA training course

## Scenario to automate
Write Python test functions using Playwright (sync API) for the following test cases:

1. **TC01 - Search by button**: Go to the home page, type "hammer" in the search box
   ([data-test="search-query"]), click the search button ([data-test="search-submit"]),
   verify at least one product is shown.

2. **TC05 - Sort high to low**: Go to Hand Tools category, select "Price (High to Low)"
   from the sort dropdown ([data-test="sort"]), verify the first product price is greater
   than or equal to the second product price.

3. **TC08 - Custom quantity**: Open the first product in Hand Tools, clear the quantity
   field ([data-test="quantity"]), type 3, click Add to cart, open the cart and verify
   the quantity shown is 3.

4. **TC12 - Remove from cart**: Add any product to the cart, go to the cart, click the
   remove button, verify the cart shows an empty message.

5. **TC13 - Contact form validation**: Go to the Contact page, click Send without filling
   anything, verify validation errors appear under each empty field.

6. **TC16 - Out of stock**: Find a product that is out of stock and verify the Add to
   cart button is disabled or not present.

## Rules
- Use data-test attributes for all locators
- Use expect() not time.sleep()
- Read prices and names from the page, never hardcode them
- Write TODO comments where you are unsure of a locator or behavior
- One function per test case, named tc01_search_by_button, tc05_sort_high_to_low, etc.
- Each function takes page as its only argument
- Include a main() that runs all tests and prints PASS or FAIL for each
- Never click Send on the contact form when it is filled in
