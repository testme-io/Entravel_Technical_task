const testData = [
    ["TC-CALC-002", "Total for single item with qty > 1", "test_calc_api.py", "Add one item with quantity 3 and verify total is price * 3", "Service is running", "/api/cart/:id/items", "POST", "total equals price * quantity", "Critical", "api, positive, regression"],
    ["TC-CALC-003", "Total for multiple different items", "test_calc_api.py", "Add multiple different items and verify the subtotal", "Service is running", "/api/cart/:id/items", "POST", "total equals sum of all items", "Critical", "api, positive, regression"],
    ["TC-CALC-006", "Total calculation after item removal", "test_calc_api.py", "Add items then remove all of them and check total", "Items added to cart", "/api/cart/:id/items/:id", "DELETE", "total returns to 0 and is never negative", "Major", "api, positive, regression"],
    ["TC-CALC-007", "Large price and quantity — no precision loss", "test_calc_api.py", "Add items with very large prices/quantities", "Service is running", "/api/cart/:id/items", "POST", "Total is calculated correctly without float errors", "Normal", "api, boundary, regression"],


    ["TC-CART-001", "Create new cart and verify cart ID generation", "test_cart_api.py", "Verify that POST /cart returns 201 and a valid cartId", "API service is up and running", "/api/cart", "POST", "201 Created and cartId is present", "Blocker", "api, smoke, positive"],
    ["TC-CART-003", "Response body structure on creation", "test_cart_api.py", "Check if response contains items and total fields", "Service is running", "/api/cart", "POST", "Fields id, items, and total are present in response", "Critical", "api, positive, regression"],
    ["TC-CART-004", "Get empty cart details", "test_cart_api.py", "Fetch details of a newly created cart", "Cart is created", "/api/cart/:cartId", "GET", "items is empty list, total is 0", "Blocker", "api, smoke, positive"],
    ["TC-CART-007", "Get cart with empty ID segment", "test_cart_api.py", "Send GET to /api/cart/ without ID", "Service is running", "/api/cart/", "GET", "404 Not Found or 405 Method Not Allowed", "Normal", "api, negative, regression"],
    ["TC-CART-008", "Get cart with numeric-only ID", "test_cart_api.py", "Send GET with numeric ID (e.g., 123)", "Service is running", "/api/cart/123", "GET", "404 Not Found", "Minor", "api, negative, boundary"],
    ["TC-CART-009", "Get cart with special characters in ID", "test_cart_api.py", "Send GET with special chars (abc!@#)", "Service is running", "/api/cart/abc!@#", "GET", "400 or 404", "Minor", "api, negative, boundary"],
    ["TC-CART-010", "Cart data isolation", "test_cart_api.py", "Verify carts do not share items", "Two carts created", "/api/cart/:id", "GET", "Items added to Cart A do not appear in Cart B", "Critical", "api, positive, regression"],
    ["TC-CART-012", "POST /cart with extra body fields", "test_cart_api.py", "Send redundant fields in JSON body", "Service is running", "/api/cart", "POST", "201 Created, extra fields are ignored", "Minor", "api, boundary, regression"],
    ["TC-CART-013", "Response Content-Type header", "test_cart_api.py", "Verify response header is application/json", "Service is running", "/api/cart", "POST", "Content-Type header present and correct", "Major", "api, positive, regression"],



    ["TC-CART-009", "Get cart with special characters in ID", "test_cart_extra_api.py", "Send GET request with ID containing !@#", "Service is running", "/api/cart/:id", "GET", "400 Bad Request or 404 Not Found", "Minor", "api, negative, boundary"],
    ["TC-CART-012", "POST /cart with extra body fields", "test_cart_extra_api.py", "Send JSON with redundant fields (foo: bar)", "Service is running", "/api/cart", "POST", "201 Created, extra fields are ignored", "Minor", "api, boundary, regression"],



    ["TC-DEL-001", "Remove existing item from cart", "test_delete_api.py", "Add an item and then delete it using its ID", "Cart with one item exists", "/api/cart/:id/items/:itemId", "DELETE", "204 No Content, item removed from list", "Blocker", "api, smoke, positive"],
    ["TC-DEL-002", "Delete item with non-existent ID", "test_delete_api.py", "Attempt to delete an item using a random UUID", "Cart exists", "/api/cart/:id/items/:itemId", "DELETE", "404 Not Found", "Major", "api, negative, regression"],
    ["TC-DEL-003", "Delete item from non-existent cart", "test_delete_api.py", "Attempt to delete an item from a cart that doesn't exist", "Service is running", "/api/cart/:id/items/:itemId", "DELETE", "404 Not Found", "Major", "api, negative, regression"],
    ["TC-CALC-004", "Total updates correctly after item removal", "test_delete_api.py", "Add two items, delete one, verify total is updated", "Cart with two items exists", "/api/cart/:id/items/:itemId", "DELETE", "Total reflects remaining items, never negative", "Critical", "api, positive, regression"]



    ["TC-DISC-001", "Apply SAVE10 — verify 10% discount", "test_discount_api.py", "Apply SAVE10 code and check total with floor rounding", "Cart has items", "/api/cart/:id/discount", "POST", "200 OK, total = subtotal * 0.9 (rounded down)", "Blocker", "api, smoke, positive"],
    ["TC-DISC-002", "Apply HALF — verify 50% discount", "test_discount_api.py", "Apply HALF code and check total", "Cart has items", "/api/cart/:id/discount", "POST", "200 OK, total = subtotal * 0.5 (rounded down)", "Critical", "api, positive, regression"],
    ["TC-DISC-004", "Apply discount in lowercase", "test_discount_api.py", "Try applying 'save10' instead of 'SAVE10'", "Cart has items", "/api/cart/:id/discount", "POST", "200 OK, discount applied regardless of case", "Minor", "api, positive, usability"],
    ["TC-DISC-005", "Apply invalid discount code", "test_discount_api.py", "Try applying a non-existent code 'BOGUS'", "Cart has items", "/api/cart/:id/discount", "POST", "400 Bad Request or 422", "Major", "api, negative, regression"],
    ["TC-DISC-009", "Apply discount to empty cart", "test_discount_api.py", "Try applying a code before adding any items", "Cart is empty", "/api/cart/:id/discount", "POST", "400 Bad Request or 200 (but total remains 0)", "Normal", "api, negative, regression"],
    ["TC-DISC-010", "Discount recalculates after adding new item", "test_discount_api.py", "Apply discount, then add more items to cart", "Discount already applied", "/api/cart/:id/items", "POST", "Total is automatically updated including the discount", "Critical", "api, positive, regression"]



    ["TC-DCALC-003", "SAVE20 on even subtotal", "test_discount_calc.py", "Verify 20% discount on 50.0", "Cart subtotal is 50", "/api/cart/:id/discount", "POST", "total is 40", "Critical", "api, positive, regression"],
    ["TC-DCALC-004", "SAVE20 on odd subtotal (Rounding)", "test_discount_calc.py", "Verify 20% discount on 35.0 (expected 28)", "Cart subtotal is 35", "/api/cart/:id/discount", "POST", "total is 28 (floor(28.0))", "Major", "api, positive, bug-015"],
    ["TC-DCALC-005", "HALF on even subtotal", "test_discount_calc.py", "Verify 50% discount on 100.0", "Cart subtotal is 100", "/api/cart/:id/discount", "POST", "total is 50", "Critical", "api, positive, regression"],
    ["TC-DCALC-006", "HALF on odd subtotal (Rounding)", "test_discount_calc.py", "Verify 50% discount on 15.0 (expected 7)", "Cart subtotal is 15", "/api/cart/:id/discount", "POST", "total is 7 (floor(7.5))", "Major", "api, positive, bug-015"],
    ["TC-DISC-007", "Discount on single-item cart", "test_discount_calc.py", "Verify SAVE20 on a single item of 30.0", "One item in cart", "/api/cart/:id/discount", "POST", "total is 24", "Critical", "api, positive, regression"],
    ["TC-DISC-008", "Discount on multi-item cart", "test_discount_calc.py", "Verify discount applies to sum of 10+15+25", "Three items in cart", "/api/cart/:id/discount", "POST", "total is 40 (50 - 20%)", "Blocker", "api, positive, bug-004"]



    ["TC-DINV-003", "Apply discount code in lowercase", "test_discount_neg_api.py", "Try 'save10' instead of 'SAVE10'", "Cart has items", "/api/cart/:id/discount", "POST", "400 Bad Request (case-sensitive)", "Minor", "api, negative, boundary"],
    ["TC-DINV-004", "Apply discount code with spaces", "test_discount_neg_api.py", "Try ' SAVE10 ' (with spaces)", "Cart has items", "/api/cart/:id/discount", "POST", "200 OK (if trimmed) or 400", "Minor", "api, negative, bug-010"],
    ["TC-DINV-011", "Apply discount to empty cart", "test_discount_neg_api.py", "Apply code before adding items", "Empty cart", "/api/cart/:id/discount", "POST", "400 Bad Request", "Normal", "api, negative, bug-011"],
    ["TC-DINV-008", "Apply code with special characters", "test_discount_neg_api.py", "Try 'SAVE!@#'", "Cart has items", "/api/cart/:id/discount", "POST", "400 Bad Request", "Major", "api, negative, regression"]



    ["TC-CART-011", "API Health Check", "test_health_api.py", "Verify the API service returns 200 OK and status 'ok'", "Service is deployed", "/health", "GET", "200 OK with {'status': 'ok'}", "Blocker", "api, smoke, positive"]


    ["TC-ADD-001", "Add single item to cart", "test_items_api.py", "Add a valid item (name, price, quantity)", "Cart exists", "/api/cart/:id/items", "POST", "201 Created, item added with correct data", "Blocker", "api, smoke, positive"],
    ["TC-ADD-002", "Add multiple identical items", "test_items_api.py", "Add the same item multiple times and verify list length", "Cart exists", "/api/cart/:id/items", "POST", "201 Created, each addition is a new entry", "Major", "api, positive, regression"],
    ["TC-CALC-001", "Subtotal calculation for single item", "test_items_api.py", "Verify total equals price * quantity for one item", "Item price 10.0, qty 1", "/api/cart/:id", "GET", "total is 10.0", "Critical", "api, positive, regression"],
    ["TC-CALC-005", "Total for empty cart is 0", "test_items_api.py", "Check total value when no items are present", "Empty cart", "/api/cart/:id", "GET", "total is 0", "Critical", "api, positive, regression"]


    ["TC-ADD-006", "Long item name boundary (256 chars)", "test_items_extra_api.py", "Add item with 256 'A' characters in name", "Cart exists", "/api/cart/:id/items", "POST", "201 Created or 400 (system handles length)", "Passed", "Minor"],
    ["TC-ADD-007", "Unicode and emoji in item name", "test_items_extra_api.py", "Add item with name '☕ Coffee 🍩'", "Cart exists", "/api/cart/:id/items", "POST", "201 Created, name stored correctly", "Passed", "Normal"],
    ["TC-ADD-008", "Duplicate item addition", "test_items_extra_api.py", "Add the exact same item twice", "Cart exists", "/api/cart/:id/items", "POST", "total is 20.0 (10.0 * 2)", "Passed", "Major"],
    ["TC-ADD-012", "High-precision float price", "test_items_extra_api.py", "Add item with price 9.999", "Cart exists", "/api/cart/:id/items", "POST", "201 Created, total is handled", "Passed", "Minor"]



    ["TC-INV-002", "Add item with zero price", "test_items_neg.py", "Try to add item with price: 0", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Failed", "Blocker"],
    ["TC-INV-011", "Add item with fractional quantity", "test_items_neg.py", "Try to add quantity: 2.5", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Failed", "Major"],
    ["TC-INV-013", "Add item with whitespace-only name", "test_items_neg.py", "Try name: '   '", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Failed", "Normal"],
    ["TC-INV-001", "Add item with negative price", "test_items_neg.py", "Try price: -10.0", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Passed", "Critical"]


    ["TC-INV-002", "Add item with zero price", "test_items_neg.py", "Verify that price 0.0 is rejected with 400 error", "Valid cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Blocker", "api, negative, bug-001"],
    ["TC-INV-011", "Add item with fractional quantity", "test_items_neg.py", "Verify that quantity 2.5 is rejected (should be integer)", "Valid cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Major", "api, negative, bug-003"],
    ["TC-INV-013", "Add item with whitespace-only name", "test_items_neg.py", "Verify that name '   ' is rejected with 400 error", "Valid cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Normal", "api, negative, bug-002"]


    ["TC-INV-014", "Add item with null price", "test_items_neg_extra_api.py", "Send 'price': null in JSON payload", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Passed", "Normal"],
    ["TC-INV-015", "Add item with null quantity", "test_items_neg_extra_api.py", "Send 'quantity': null in JSON payload", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Passed", "Normal"],
    ["TC-INV-016", "Add item with null name", "test_items_neg_extra_api.py", "Send 'name': null in JSON payload", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Passed", "Normal"],
    ["TC-INV-018", "Price as extremely large number", "test_items_neg_extra_api.py", "Try price: 9,999,999,999", "Cart exists", "/api/cart/:id/items", "POST", "201 Created or 400 (Handled)", "Passed", "Minor"],
    ["TC-INV-019", "Quantity as extremely large number", "test_items_neg_extra_api.py", "Try quantity: 9,999,999", "Cart exists", "/api/cart/:id/items", "POST", "201 Created or 400 (Handled)", "Passed", "Minor"],
    ["TC-INV-020", "Non-JSON payload (Content-Type mismatch)", "test_items_neg_extra_api.py", "Send plain text instead of JSON object", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request or 415", "Passed", "Normal"]



    ["TC-PERS-001", "Data persists after page reload", "test_persistence.py", "Add item via UI, reload page, verify item remains", "UI state active", "/", "UI/RELOAD", "Item count and total are unchanged", "Failed", "Blocker (BUG-017)"],
    ["TC-PERS-002", "Multi-tab synchronization check", "test_persistence.py", "Add item in Tab A, check Tab B for consistency", "Two tabs open", "/", "UI/TAB", "Verify if cart is shared or isolated", "Passed", "Normal (Isolated behavior confirmed)"]


    ["TC-SEC-001", "XSS injection in item name", "test_security.py", "Try <script>alert(1)</script> as item name", "Cart exists", "/api/cart/:id/items", "POST", "201 Created (Stored as literal text)", "Passed", "Critical"],


    ["TC-SEC-002.1", "SQL Injection in cart ID", "test_security.py", "Try payload: ' OR '1'='1", "API client", "/api/cart/:id", "GET", "400/404, No internal info leak", "Passed", "Critical"],
    ["TC-SEC-002.2", "SQL DROP TABLE in cart ID", "test_security.py", "Try payload: 1; DROP TABLE carts--", "API client", "/api/cart/:id", "GET", "400/404, No internal info leak", "Passed", "Critical"],
    ["TC-SEC-002.3", "NoSQL Injection in cart ID", "test_security.py", "Try payload: {\"$gt\": \"\"}", "API client", "/api/cart/:id", "GET", "400/404, No internal info leak", "Passed", "Critical"],
    ["TC-SEC-002.4", "Path Traversal in cart ID", "test_security.py", "Try payload: ../../../etc/passwd", "API client", "/api/cart/:id", "GET", "400/404, No internal info leak", "Passed", "Critical"]


    ["TC-STRESS-001", "Add 200 items stability check", "test_stress.py", "Sequentially add 200 items via API and verify total calculation", "API available", "/api/cart/:id/items", "POST", "200 items added, total is 200.0", "Passed", "stress, api, stability"],
    ["TC-STRESS-002", "10k characters name UI stability", "test_stress.py", "Add item with 10,000-char name and load UI page", "API accepted long name", "/", "UI_LOAD", "Page renders without freezing or crashing", "Passed", "stress, ui, boundary"]


    ["TC-UI-001", "Add item via UI form", "test_cart_ui.py", "Fill Name, Price, Qty and click Add", "Main page open", "/", "UI", "Item listed, total updates", "Passed", "Blocker, smoke"],
    ["TC-UI-002", "Remove item via UI", "test_cart_ui.py", "Click Remove on existing item", "Item in cart", "/", "UI", "Item disappears, total resets", "Passed", "Blocker, smoke"],
    ["TC-UI-012", "Add 3 items via UI", "test_cart_ui.py", "Sequentially add 3 different items", "Main page open", "/", "UI", "Count: 3, Total is correct sum", "Passed", "Critical"],
    ["TC-UI-009", "UI total matches expected calculation", "test_cart_ui.py", "Add item (10x2), verify total is 20", "Main page open", "/", "UI", "Total display matches calculation", "Passed", "Critical"],


    ["TC-UI-003", "Apply SAVE10 via UI (BUG-008)", "test_cart_ui.py", "Apply SAVE10 to 20.00 total", "Item added", "/", "UI", "Total becomes 18.00", "Failed", "Blocker (BUG-008)"],
    ["TC-UI-004", "Apply SAVE20 via UI", "test_cart_ui.py", "Apply SAVE20 to 20.00 total", "Item added", "/", "UI", "Total becomes 16.00", "Passed", "Critical"],
    ["TC-UI-005", "Apply HALF via UI", "test_cart_ui.py", "Apply HALF to 20.00 total", "Item added", "/", "UI", "Total becomes 10.00", "Passed", "Critical"],
    ["TC-UI-014", "Discount applies to subtotal (BUG-004 Check)", "test_cart_ui.py", "Add 10.0 and 20.0, apply SAVE20", "2 items added", "/", "UI", "Total becomes 24.00", "Failed", "Critical (BUG-004)"],
    ["TC-UI-010", "HALF discount display check", "test_cart_ui.py", "Verify UI reflects HALF discount", "Item added", "/", "UI", "Discounted total visible", "Passed", "Critical"],


    ["TC-UI-006", "Empty form validation", "test_cart_ui.py", "Click Add button without filling fields", "Main page open", "/", "UI", "No item added to list", "Passed", "Critical"],
    ["TC-UI-007", "Negative price validation in UI", "test_cart_ui.py", "Try to add item with price -5", "Main page open", "/", "UI", "Item is not added", "Passed", "Critical"],
    ["TC-UI-011", "Invalid discount code UI feedback", "test_cart_ui.py", "Enter 'FAKECODE' in discount field", "Item added", "/", "UI", "Error message visible or total unchanged", "Passed", "Normal"]


    ["TC-UI-008", "Validation — zero quantity does not add item", "test_cart_extra_ui.py", "Try to add item with quantity=0", "Main page open", "/", "UI", "Item is not added", "Passed", "Critical, negative"],
    ["TC-UI-013", "Clear entire cart via UI", "test_cart_extra_ui.py", "Add 3 items and remove them one by one", "3 items in cart", "/", "UI", "Count: 0, Total: 0", "Passed", "Normal, regression"]


];