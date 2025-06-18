# app/debug_scrape.py

import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()
COOKIE = os.getenv("DISCOURSE_COOKIE", "")
URL    = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34/l/latest"

print("Using cookie:", COOKIE)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    if COOKIE:
        page.set_extra_http_headers({"Cookie": COOKIE})
    page.goto(URL, wait_until="networkidle")
    # scroll just in case
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    html = page.content()
    browser.close()

# dump to file
with open("app/data/category_debug.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Wrote category_debug.html. Now inspect it in your browser and note the selector for each topic row.")
