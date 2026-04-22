const bugData = [
    ["BUG-001", "API accepts item with price=0", "Blocker", "TC-INV-002", "Blocker", "OPEN", "curl -X POST /items -d '{\"price\":0}'"],
    ["BUG-002", "Whitespace-only names allowed", "Critical", "TC-INV-013", "Critical", "OPEN", "curl -X POST /items -d '{\"name\":\"   \"}'"],
    ["BUG-003", "Fractional quantity accepted", "Major", "TC-INV-011", "Major", "OPEN", "curl -X POST /items -d '{\"quantity\":2.5}'"],
    ["BUG-004", "Discount applies to first item only (Subtotal logic)", "Blocker", "TC-DCALC-009, TC-DCALC-048", "Blocker", "OPEN", "Add items for $10 and $20, apply SAVE10. Total is 29 instead of 27"],
    ["BUG-005", "POST /discount does not return updated cart state", "Major", "TC-DISC-009", "Major", "OPEN", "curl -X POST /cart/123/discount -d '{\"code\":\"SAVE10\"}'"],
    ["BUG-006", "Discount totals not rounded down (Floor fail)", "Critical", "TC-DCALC-002, TC-DCALC-011, TC-DCALC-012", "Critical", "OPEN", "Prices like 19.99 with discount show decimals instead of floored integer"],
    ["BUG-007", "No discount recalculation when new item added", "Blocker", "TC-DISC-010", "Blocker", "OPEN", "Apply discount first, then add new item. Total ignores existing discount"],
    ["BUG-008", "UI: Total unchanged after applying valid promo code", "Critical", "TC-UI-014", "Blocker", "OPEN", "Enter 'SAVE20' in UI. Subtotal stays 30.00 instead of 24.00"],
    ["BUG-015", "Math.floor failure: $1.00 with 50% discount results in $0.5 instead of $0.0", "Major", "TC-DCALC-007", "Medium", "OPEN", "Apply 'HALF' code to $1.00 item. Expected: 0.0, Actual: 0.5"],
    ["BUG-016", "Floating point precision error: total shows 0.81 for $0.9 price", "Major", "TC-DCALC-011", "Medium", "OPEN", "Apply 'SAVE10' to $0.9 item. Observe raw float result"],
    ["BUG-017", "Incorrect subtotal rounding: 19.99 with 10% discount results in 17.99 instead of 17.0", "Critical", "TC-DCALC-012", "High", "OPEN", "Apply 'SAVE10' to 19.99. Expected floor result (17.0) is ignored"],
    ["BUG-018", "UI: Error message not displayed for invalid promo code", "Minor", "TC-UI-011", "Low", "OPEN", "Enter 'WRONG' code in UI. No error message appears"],
    ["BUG-019", "UI: Last item remains in DOM after removal", "Major", "TC-UI-013", "Medium", "OPEN", "Add one item and click 'Remove'. Item count stays 1"],
    ["BUG-020", "Security: System returns 500 Error on SQL-like payloads in ID", "Critical", "TC-SEC-002", "High", "OPEN", "Use ' OR '1'='1' in Cart ID. Check for server crash"],
    ["BUG-021", "Persistence: Cart is cleared after page reload (F5)", "Critical", "TC-PERS-001", "High", "OPEN", "Add item to cart and refresh the page. Cart returns to empty state"]
];