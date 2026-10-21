#!/usr/bin/env python3
"""Check adjacent navigation and capture bounded interior/PDF review views."""
from pathlib import Path
import tempfile
import json
import pymupdf as fitz
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = Path(tempfile.mkdtemp(prefix="speaking-interior-review-"))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(java_script_enabled=False)
        page.goto((ROOT / "site/speaking-practice.html").as_uri())
        for prefix, count in (("chapter", 27), ("path", 11)):
            for number in range(1, count + 1):
                expected = [f"#{prefix}-{n:02}" for n in (number - 1, number + 1) if 1 <= n <= count]
                links = page.locator(f"#{prefix}-{number:02} .chapter-navigation a")
                assert links.evaluate_all("els => els.map(el => el.getAttribute('href'))") == expected
        for width in (390, 1280):
            page.set_viewport_size({"width": width, "height": 900})
            for name, selector in (
                ("learning-path", "#path-02 h3"),
                ("approach", "#chapter-16 blockquote"),
                ("end-navigation", "#chapter-16 .chapter-navigation"),
                ("source-index", "#source-index h3"),
            ):
                target = page.locator(selector).first
                target.evaluate("el => el.scrollIntoView({block:'start'})")
                page.screenshot(path=str(output / f"{name}-{width}.png"))
            for origin, target in (("#chapter-16", "#chapter-17"), ("#chapter-17", "#chapter-16"), ("#path-02", "#path-03")):
                link = page.locator(f'{origin} .chapter-navigation a[href="{target}"]')
                link.focus()
                assert link.evaluate("el => el === document.activeElement && getComputedStyle(el).outlineStyle !== 'none'")
                page.keyboard.press("Enter")
                page.wait_for_url("**" + target)
                assert page.locator(target).bounding_box()["y"] < 100
            link = page.locator('#path-03 .back a[href="#learning-paths"]')
            link.focus()
            page.keyboard.press("Enter")
            page.wait_for_url("**#learning-paths")
            assert page.locator("#learning-paths").bounding_box()["y"] < 100
        browser.close()
    document = fitz.open(ROOT / "deliverables/speaking-practice/speaking-practice.pdf")
    needles = ["Without confirmation, we won't send", "not the publication date", "Support owns the reply"]
    pages = {0, len(document) - 1}
    for needle in needles:
        matches = [i for i, page in enumerate(document) if needle in " ".join(page.get_text().split()).replace("’", "'")]
        assert matches, needle
        pages.add(matches[0])
    for index in sorted(pages):
        document[index].get_pixmap(matrix=fitz.Matrix(1, 1)).save(output / f"pdf-page-{index+1}.png")
    print(json.dumps({"output": str(output), "adjacency_sets_checked": 38, "keyboard_widths": [390,1280], "pdf_pages_rendered": [i+1 for i in sorted(pages)]}, indent=2))


if __name__ == "__main__":
    main()
