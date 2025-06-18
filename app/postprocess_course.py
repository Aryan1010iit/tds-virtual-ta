# app/postprocess_course.py

import os, json
from bs4 import BeautifulSoup

INPUT_HTML  = os.path.join("app", "data", "course_content_raw.html")
OUTPUT_JSON = os.path.join("app", "data", "course_content_structured.json")

def parse_course_html():
    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # 1) Headings (h1–h6)
    headings = [
        {"tag": h.name, "text": h.get_text(strip=True)}
        for h in soup.find_all(["h1","h2","h3","h4","h5","h6"])
    ]

    # 2) Paragraphs
    paragraphs = [
        p.get_text(strip=True)
        for p in soup.find_all("p")
        if p.get_text(strip=True)
    ]

    # 3) Lists (ul / ol)
    lists = []
    for ul in soup.find_all(["ul","ol"]):
        items = [li.get_text(strip=True) for li in ul.find_all("li")]
        if items:
            lists.append(items)

    # 4) Tables
    tables = []
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [cell.get_text(strip=True) for cell in tr.find_all(["th","td"])]
            if cells:
                rows.append(cells)
        if rows:
            tables.append(rows)

    # 5) Links
    links = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        # ignore empty anchors
        if text and href:
            links.append({"text": text, "url": href})

    structured = {
        "headings": headings,
        "paragraphs": paragraphs,
        "lists": lists,
        "tables": tables,
        "links": links
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2, ensure_ascii=False)

    print(f"✅ Wrote structured content to {OUTPUT_JSON}")

if __name__ == "__main__":
    parse_course_html()
