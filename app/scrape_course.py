# app/scrape_course.py

from playwright.sync_api import sync_playwright
import os

OUT_HTML = os.path.join("app", "data", "course_content_raw.html")
OUT_TEXT = os.path.join("app", "data", "course_content_raw.txt")

def scrape_course_content_raw(term="2025-01"):
    url = f"https://tds.s-anand.net/#/{term}/"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        html = page.content()
        text = page.evaluate("document.body.innerText")
        browser.close()

    # write HTML
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    # write plain text
    with open(OUT_TEXT, "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Saved raw HTML & text")

if __name__ == "__main__":
    scrape_course_content_raw()
