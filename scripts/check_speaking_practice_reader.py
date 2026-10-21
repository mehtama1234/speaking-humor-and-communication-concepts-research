#!/usr/bin/env python3
"""Check reader links, content coverage and no-JS responsive navigation."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from playwright.sync_api import sync_playwright
from build_speaking_source_catalog import collect_sources

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "site" / "speaking-practice.html"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "href" in attrs:
            self.hrefs.append(attrs["href"])


def main():
    catalog = collect_sources()
    parser = Links()
    parser.feed(PAGE.read_text())
    assert len(parser.ids) == len(set(parser.ids)), "Duplicate IDs"
    for href in parser.hrefs:
        parts = urlsplit(href)
        if parts.scheme or parts.netloc:
            continue
        if parts.path:
            assert (PAGE.parent / unquote(parts.path)).is_file(), href
        elif parts.fragment:
            assert unquote(parts.fragment) in parser.ids, href
    approaches = sorted((ROOT / "writeups" / "speaking-practice").glob("[0-9][0-9]-*.md"))
    curricula = sorted((ROOT / "writeups" / "speaking-curricula").glob("[0-9][0-9]-*.md"))
    sources = approaches + curricula
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(java_script_enabled=False)
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        for width in (320, 390, 768, 1280):
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(PAGE.as_uri(), wait_until="load")
            assert page.locator("article").count() == len(sources)
            assert page.locator("article.approach").count() == len(approaches)
            assert page.locator("article.learning-path").count() == len(curricula)
            assert page.locator("#learning-paths li").count() == len(curricula)
            assert f"{len(curricula)} of 11 learning paths" in page.locator(".status").inner_text()
            assert page.locator("h1").count() == 1
            assert page.locator("#source-index li").count() == catalog["source_count"]
            assert page.locator("#using-the-guide h2").count() == 1
            assert page.locator("#source-notes h2").count() == 1
            for source in catalog["sources"]:
                entry = page.locator("#source-" + source["video_id"])
                assert entry.locator("h3 a").get_attribute("href") == source["url"]
            assert page.locator("article h3").count() >= len(sources) * 5
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), width
            for source in sources:
                title = source.read_text().splitlines()[0][2:]
                assert page.get_by_role("heading", name=title, exact=True).count() == 1
            page.keyboard.press("Tab")
            assert page.locator(".skip").evaluate("el => el === document.activeElement")
            assert page.locator(".skip").bounding_box()["y"] >= 0
            page.keyboard.press("Enter")
            page.wait_for_url("**#main", timeout=10000)
            assert page.locator("#main").evaluate("el => el === document.activeElement")
            for source in approaches:
                target = "#" + "chapter-" + source.stem.split("-", 1)[0]
                page.locator(f'#contents a[href="{target}"]').click()
                page.wait_for_url("**" + target, timeout=10000)
                assert page.locator(target).bounding_box()["y"] < 100
            assert page.locator("article .chapter-navigation").count() == len(sources)
            page.locator('#contents a[href="#chapter-09"]').click()
            assert page.url.endswith("#chapter-09")
            assert page.locator("#chapter-09").bounding_box()["y"] < 100
            for curriculum in curricula:
                path_id = "path-" + curriculum.stem.split("-", 1)[0]
                page.locator(f'#learning-paths a[href="#{path_id}"]').click()
                assert page.url.endswith("#" + path_id)
                assert page.locator("#" + path_id).bounding_box()["y"] < 100
                cross_link = page.locator(f'#{path_id} a[href^="#chapter-"]').first
                target = cross_link.get_attribute("href")
                cross_link.click()
                assert page.url.endswith(target)
                assert page.locator(target).bounding_box()["y"] < 100
            source_link = page.locator('#chapter-01 a[href^="#source-"]').first
            source_target = source_link.get_attribute("href")
            source_link.click()
            assert page.url.endswith(source_target)
            assert page.locator(source_target).bounding_box()["y"] < 100
        assert not errors, errors
        # Text enlargement is distinct from a narrow viewport: enlarge rem/em
        # text to 200% and check all rendered text containers for clipping.
        page.set_viewport_size({"width": 320, "height": 900})
        page.goto(PAGE.as_uri())
        page.evaluate("document.documentElement.style.fontSize = '200%'")
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "200% text overflow"
        assert page.locator("article, .contents-panel, .book-matter").evaluate_all(
            "els => els.every(el => el.scrollWidth <= el.clientWidth + 1)"
        ), "200% container clipping"
        page.locator('#contents a[href="#chapter-16"]').click()
        page.screenshot(path="/tmp/speaking-practice-reader-large-text.png")
        page.goto(PAGE.as_uri())
        page.set_viewport_size({"width": 1280, "height": 900})
        page.screenshot(path="/tmp/speaking-practice-reader-desktop.png")
        page.set_viewport_size({"width": 390, "height": 900})
        page.screenshot(path="/tmp/speaking-practice-reader-mobile.png")
        browser.close()
    print(f"PASS: {len(approaches)} chapters, {len(curricula)} learning paths, {len(parser.hrefs)} links, unique IDs, four widths, every chapter destination, no-JS reading, cross-navigation, keyboard skip focus and 200% text")


if __name__ == "__main__":
    main()
