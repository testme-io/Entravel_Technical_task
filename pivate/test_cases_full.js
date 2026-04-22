const finalNormalizedTestData = [
    // === 1. CART MANAGEMENT (API) ===
    ["TC-CART-001", "Create new cart", "test_cart_api.py", "POST /cart and verify cartId generation", "Service is running", "/api/cart", "POST", "201 Created and cartId is present", "Blocker", "api, smoke, positive"],
    ["TC-CART-002", "Response body structure", "test_cart_api.py", "Check if response contains items and total fields", "Service is running", "/api/cart", "POST", "Fields id, items, and total are present", "Critical", "api, positive, regression"],
    ["TC-CART-003", "Get empty cart details", "test_cart_api.py", "Fetch details of a newly created cart", "Cart is created", "/api/cart/:id", "GET", "items is empty list, total is 0", "Blocker", "api, smoke, positive"],
    ["TC-CART-004", "Cart data isolation", "test_cart_api.py", "Verify carts do not share items", "Two carts created", "/api/cart/:id", "GET", "Items in Cart A do not appear in Cart B", "Critical", "api, positive, regression"],
    ["TC-CART-005", "Get cart with numeric ID", "test_cart_api.py", "Send GET with numeric ID (e.g., 123)", "Service is running", "/api/cart/123", "GET", "404 Not Found", "Minor", "api, negative, boundary"],
    ["TC-CART-006", "POST /cart with extra fields", "test_cart_api.py", "Send redundant fields in JSON body", "Service is running", "/api/cart", "POST", "201 Created, extra fields are ignored", "Minor", "api, boundary, regression"],
    ["TC-CART-007", "Response Content-Type header", "test_cart_api.py", "Verify response header is application/json", "Service is running", "/api/cart", "POST", "Content-Type is application/json", "Major", "api, positive"],

    // === 2. ITEMS & INVENTORY (API) ===
    ["TC-INV-001", "Add single valid item", "test_items_api.py", "Add item (name, price, quantity)", "Cart exists", "/api/cart/:id/items", "POST", "201 Created, data is correct", "Blocker", "api, smoke, positive"],
    ["TC-INV-002", "Add item with price=0", "test_items_neg.py", "Try to add item with price: 0", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request (BUG-001)", "Blocker", "api, negative"],
    ["TC-INV-003", "Add item with negative price", "test_items_neg.py", "Try to add item with price: -10.0", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Critical", "api, negative"],
    ["TC-INV-004", "Add item with fractional quantity", "test_items_neg.py", "Try to add quantity: 2.5", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request (BUG-003)", "Major", "api, negative"],
    ["TC-INV-005", "Add item with whitespace name", "test_items_neg.py", "Try name: '   '", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request (BUG-002)", "Normal", "api, negative"],
    ["TC-INV-006", "Add item with null fields", "test_items_neg_extra_api.py", "Send null for name/price/qty", "Cart exists", "/api/cart/:id/items", "POST", "400 Bad Request", "Normal", "api, negative"],
    ["TC-INV-007", "Unicode and emoji in name", "test_items_extra_api.py", "Add item with name '☕ Coffee'", "Cart exists", "/api/cart/:id/items", "POST", "201 Created, name stored correctly", "Normal", "api, positive"],
    ["TC-INV-008", "Remove item from cart", "test_delete_api.py", "Add item then delete via its ID", "Item exists", "/api/cart/:id/items/:itemId", "DELETE", "204 No Content, item removed", "Blocker", "api, smoke, positive"],

    // === 3. CALCULATIONS & DISCOUNTS (API) ===
    ["TC-DISC-001", "Apply SAVE10 discount", "test_discount_api.py", "Apply SAVE10 and check floor rounding", "Cart has items", "/api/cart/:id/discount", "POST", "200 OK, total = subtotal * 0.9 (floor)", "Blocker", "api, smoke, positive, boundary"],
    ["TC-DISC-002", "Apply HALF discount", "test_discount_api.py", "Apply HALF and check floor rounding", "Cart has items", "/api/cart/:id/discount", "POST", "200 OK, total = subtotal * 0.5 (floor)", "Critical", "api, positive, boundary"],
    ["TC-DISC-003", "Discount persistence", "test_discount_api.py", "Apply discount, then add more items", "Discount active", "/api/cart/:id/items", "POST", "Total updates including discount", "Critical", "api, regression, positive"],
    ["TC-DISC-004", "Apply code with spaces", "test_discount_neg_api.py", "Try ' SAVE10 ' (with spaces)", "Item in cart", "/api/cart/:id/discount", "POST", "200 OK (Trimmed)", "Minor", "api, negative"],
    ["TC-DISC-005", "Discount on empty cart", "test_discount_neg_api.py", "Apply code before adding items", "Empty cart", "/api/cart/:id/discount", "POST", "400 Bad Request", "Normal", "api, negative"],

    // === 4. USER INTERFACE (UI) ===
    ["TC-UI-001", "Add item via UI", "test_cart_ui.py", "Fill form and click Add", "Page open", "/", "UI", "Item listed, total updates", "Blocker", "ui, smoke, positive"],
    ["TC-UI-002", "Remove item via UI", "test_cart_ui.py", "Click Remove button", "Item in cart", "/", "UI", "Item disappears, total resets", "Blocker", "ui, smoke, positive"],
    ["TC-UI-003", "Apply SAVE10 via UI", "test_cart_ui.py", "Enter SAVE10 in field", "Item in cart", "/", "UI", "Total updates (BUG-012)", "Critical", "ui, smoke, positive"],
    ["TC-UI-004", "UI/API Sync check", "test_cart_ui.py", "Compare UI total with API value", "Items in cart", "/", "UI", "Values match exactly", "Critical", "ui, regression"],
    ["TC-UI-005", "Data persistence (F5)", "test_persistence.py", "Add item and reload page", "Item added", "/", "UI", "Cart is not empty (BUG-011)", "Blocker", "ui, persistence"],
    ["TC-UI-006", "Empty form validation", "test_cart_ui.py", "Click Add with empty fields", "Page open", "/", "UI", "No item added", "Critical", "ui, negative"],
    ["TC-UI-007", "Clear cart check", "test_cart_extra_ui.py", "Remove 3 items one by one", "3 items in cart", "/", "UI", "List is empty, Total is 0", "Normal", "ui, regression"],

    // === 5. SYSTEM & SECURITY ===
    ["TC-SEC-001", "SQL Injection in Cart ID", "test_security.py", "Try payload: ' OR '1'='1", "API client", "/api/cart/:id", "GET", "400/404, No leak", "Critical", "api, security, negative"],
    ["TC-SEC-002", "XSS in item name", "test_security.py", "Name: <script>alert(1)</script>", "Cart exists", "/api/cart/:id/items", "POST", "Stored as literal text", "Critical", "api, security, negative"],
    ["TC-STRESS-001", "Add 200 items", "test_stress.py", "Sequentially add 200 items", "API available", "/api/cart/:id/items", "POST", "System remains stable", "Normal", "api, stress, boundary"],
    ["TC-STRESS-002", "Long name UI stability", "test_stress.py", "Item with 10k-char name", "API accepted", "/", "UI", "Page renders without crash", "Normal", "ui, stress, boundary"]
];