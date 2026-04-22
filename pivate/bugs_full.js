const finalBugDataReport = [
    // --- ГРУППА 1: API ВАЛИДАЦИЯ (tests/api/test_items_neg.py) ---
    ["BUG-001", "API accepts item with price=0", "test_items_neg.py", "Send item with price: 0", "Cart exists", "/api/cart/:id/items", "POST", "Status 400 (Bad Request)", "Blocker", "api, negative"],
    ["BUG-002", "Whitespace-only names allowed", "test_items_neg.py", "Send item with name: '   '", "Cart exists", "/api/cart/:id/items", "POST", "Status 400 (Bad Request)", "Critical", "api, negative"],
    ["BUG-003", "Fractional quantity accepted (2.5)", "test_items_neg.py", "Send item with quantity: 2.5", "Cart exists", "/api/cart/:id/items", "POST", "Status 400 (Reject floats)", "Major", "api, negative"],
    ["BUG-004", "Non-JSON payload causes 500/Crash", "test_items_neg_extra_api.py", "Send plain text instead of JSON object", "Cart exists", "/api/cart/:id/items", "POST", "Status 400 (Invalid Format)", "Normal", "api, negative, security"],

    // --- ГРУППА 2: ЛОГИКА РАСЧЕТОВ И СКИДОК ---
    ["BUG-005", "Discount applies to first item only", "test_cart_ui.py", "Add items (10+20), apply SAVE20", "2 items in cart", "/api/cart/:id/discount", "POST", "Total is 24 (30 - 20%)", "Blocker", "ui, regression, positive"],
    ["BUG-006", "No recalculation when new item added", "test_discount_api.py", "Apply HALF, then add item for 20", "Discount active", "/api/cart/:id/items", "POST", "Total is 15 (half of 30)", "Blocker", "api, regression, positive"],
    ["BUG-007", "Math.floor failure (Rounding issues)", "test_discount_api.py", "Apply HALF to subtotal 1.0", "Item 1.0 in cart", "/api/cart/:id/discount", "POST", "Total is 0 (floor of 0.5)", "Critical", "api, negative, boundary"],
    ["BUG-008", "Floating point precision error (0.81)", "test_discount_api.py", "Apply SAVE10 to 0.09", "Item 0.09 in cart", "/api/cart/:id/discount", "POST", "Total is 0 (no floats like 0.81)", "Major", "api, boundary"],
    ["BUG-009", "POST /discount missing cart state", "test_discount_api.py", "Check response body after applying code", "Valid code", "/api/cart/:id/discount", "POST", "Body contains updated total", "Major", "api, positive"],
    ["BUG-010", "Discount code with spaces not trimmed", "test_discount_neg_api.py", "Apply code ' SAVE10 ' with spaces", "Item in cart", "/api/cart/:id/discount", "POST", "Status 200 (Trimmed success)", "Minor", "api, negative"],

    // --- ГРУППА 3: ПОЛЬЗОВАТЕЛЬСКИЙ ИНТЕРФЕЙС (UI) ---
    ["BUG-011", "Persistence: Cart cleared on reload", "test_persistence.py", "Add item and press F5", "Item added", "/", "UI/RELOAD", "Cart remains populated", "Blocker", "ui, persistence"],
    ["BUG-012", "UI: Promo code does not update Total", "test_cart_ui.py", "Enter SAVE10 in UI field", "Item in list", "/", "UI", "Total updates visually", "Critical", "ui, smoke, positive"],
    ["BUG-013", "UI: Last item remains in DOM after removal", "test_cart_extra_ui.py", "Remove the only item in cart", "1 item in list", "/", "UI", "List becomes empty", "Major", "ui, regression"],
    ["BUG-014", "UI: Error message missing for invalid code", "test_cart_ui.py", "Enter 'WRONG' code in UI", "Item in list", "/", "UI", "Error text is displayed", "Minor", "ui, negative"],
    ["BUG-015", "UI: HALF discount button not functional", "test_cart_ui.py", "Click HALF button in UI", "Item in list", "/", "UI", "Total reduced by 50%", "Blocker", "ui, smoke"],

    // --- ГРУППА 4: СИСТЕМНЫЕ И БЕЗОПАСНОСТЬ ---
    ["BUG-016", "SQL/NoSQL Injection in Cart ID", "test_security.py", "Use ' OR '1'='1' as cart ID", "Public endpoint", "/api/cart/:id", "GET", "Status 400/404 (No 500)", "Critical", "api, security, negative"],
    ["BUG-017", "System Crash on JavaScript Dialogs", "test_cart_ui.py", "Trigger alert/dialog during action", "Browser active", "/", "UI", "System remains stable", "Blocker", "ui, stress"],
    ["BUG-018", "API vs UI Total Mismatch (Sync)", "test_cart_ui.py", "Compare UI total with API response", "Cart populated", "/", "UI", "Values are identical", "Critical", "ui, regression"]
];