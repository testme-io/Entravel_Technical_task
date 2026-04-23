# 🛒 EnTravel Cart Functionality: QA Assessment & Reporting

Strategic quality overview of the shopping cart module. This project demonstrates a risk-oriented approach to API & UI testing, ensuring business logic stability and data integrity.

[🌐 **ACCESS LIVE DASHBOARD**](https://testme-io.github.io/Entravel_Technical_task/)

---

### 📊 Executive Summary
- **Test Coverage:** 32 Scenarios (Core API, UI/UX, Edge Cases, Security).
- **Defect Discovery:** 18 Bugs (6 Blocker/Critical).
- **Current Release Status:** ⛔ **BLOCKED**
  *The release is halted due to critical vulnerabilities in the discount engine and potential data loss during session reloads.*

---

### 💡 Engineering Highlights
* **Automated CI/CD Pipeline:** Fully integrated with GitHub Actions. Every push triggers a fresh test run with instant Allure Report generation.
* **Dynamic Quality Gate:** Real-time alert system. The dashboard automatically flags the release status based on defect severity.
* **Traceability:** Seamless navigation between discovered bugs and their corresponding test specifications.
* **Clean Data Visualization:** Technical details (Reproduction Steps, API Payloads) are tucked away to keep the focus on high-level metrics, accessible via **"Select Columns"**.
* **Tech Stack:** Pytest, Playwright, Allure. Custom frontend (JS/jQuery, DataTables) for the executive dashboard.

---

### 🧠 Strategic Assumptions (Risk Mitigation)
To ensure testing consistency, the following logic was applied:
1.  **Financial Integrity:** All prices must be positive; zero-price transactions are blocked as high-risk.
2.  **Customer-First Math:** All discounts use `floor` rounding to prevent overcharging.
3.  **Session Continuity:** Assumption that cart state must persist across reloads (currently failing, see BUG-011).
4.  **Security Baseline:** Mandatory input sanitization for all cart-related endpoints.

---
*QA Engineer: Mykhailo Novozhenov*