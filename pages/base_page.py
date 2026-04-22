# pages/base_page.py

class BasePage:
    def __init__(self, page):
        self.page = page

    def wait_for_load(self, timeout: int = 3000):
        # networkidle can hang if app has background requests
        # using domcontentloaded + short timeout is more reliable
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        except Exception:
            pass