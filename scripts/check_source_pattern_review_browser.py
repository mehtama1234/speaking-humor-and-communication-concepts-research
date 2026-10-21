#!/usr/bin/env python3
"""Smoke-test the local source-pattern contextual review browser."""

from __future__ import annotations

import http.server
import functools
import json
import re
import subprocess
import sys
import tempfile
import threading
import zipfile
from pathlib import Path
from urllib.parse import urljoin


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "analysis" / "source-pattern-review-browser-smoke.json"


def validate_static_context() -> dict:
    browser = (ROOT / "site" / "pattern-review.html").read_text(encoding="utf-8")
    wave_browser = (ROOT / "site" / "pattern-review-wave-2.html").read_text(encoding="utf-8")
    queue_specs = (
        ROOT / "analysis" / "ali-siddiq-wave-2-context-review-queue.json",
        ROOT / "analysis" / "dry-bar-comedy-wave-2-starter-context-review-queue.json",
        ROOT / "analysis" / "ted-wave-2-starter-context-review-queue.json",
    )
    wave_items = [
        item
        for path in queue_specs
        for item in json.loads(path.read_text(encoding="utf-8")).get("items", [])
    ]
    packet_paths = (
        "analysis/ali-siddiq-wave-2-context-packets.json",
        "analysis/dry-bar-comedy-wave-2-starter-context-packets.json",
        "analysis/ted-wave-2-starter-context-packets.json",
    )
    packets_by_id = {
        packet_item["item_id"]: packet_item
        for path in packet_paths
        for packet_item in json.loads((ROOT / path).read_text(encoding="utf-8")).get("packets", [])
    }
    expected_refs = sum(len(packets_by_id[item["item_id"]].get("references", [])) for item in wave_items)
    expected_excerpts = sum(
        len(reference.get("bounded_retrieval_excerpts", []))
        for item in wave_items
        for reference in packets_by_id[item["item_id"]].get("references", [])
    )
    expected_wave_ids = {item["item_id"] for item in wave_items}
    all_queue_match = re.search(r'<script id="all-queue-ids" type="application/json">(.*?)</script>', wave_browser, re.DOTALL)
    all_queue_ids = json.loads(all_queue_match.group(1)) if all_queue_match else []
    rendered_wave_ids = {
        match.split(" ", 1)[0]
        for match in re.findall(r'<article class="review-card" data-search="([^"]+)"', wave_browser)
    }
    local_links = re.findall(r'href="([^"]*raw-material/youtube/transcripts/[^"]+)"', browser)
    wave_local_links = re.findall(r'href="([^"]*raw-material/youtube/(?:transcripts|cues)/[^"]+)"', wave_browser)
    expected_ids_present = all(f'data-search="{item["item_id"]} ' in browser for item in wave_items)
    files_present = all(
        (ROOT / "site" / href).resolve().is_file()
        and ROOT in (ROOT / "site" / href).resolve().parents
        for href in local_links
    )
    return {
        "queue_item_count": browser.count('class="review-card"') == 107,
        "all_19_wave_2_items_rendered": len(wave_items) == 19 and expected_ids_present,
        "retrieval_excerpts_rendered": browser.count("<blockquote>") == expected_excerpts,
        "transcript_and_cue_links_rendered": len(local_links) == expected_refs * 2,
        "all_local_transcript_and_cue_targets_exist": files_present,
        "source_video_links_rendered": browser.count(">Open source video</a>") == expected_refs,
        "dedicated_wave_2_card_count": wave_browser.count('class="review-card"') == 19,
        "dedicated_wave_2_exact_ids": rendered_wave_ids == expected_wave_ids,
        "dedicated_page_retains_107_item_denominator": len(all_queue_ids) == 107 and expected_wave_ids.issubset(set(all_queue_ids)),
        "dedicated_page_discloses_88_unreviewed": "other 88 combined-queue items are not displayed" in wave_browser,
        "dedicated_context_links_and_excerpts": len(wave_local_links) == expected_refs * 2 and wave_browser.count("<blockquote>") == expected_excerpts,
        "dedicated_context_targets_exist": all(
            (ROOT / "site" / href).resolve().is_file()
            and ROOT in (ROOT / "site" / href).resolve().parents
            for href in wave_local_links
        ),
    }


def record_browser_unavailable(error: str, static_checks: dict) -> None:
    REPORT.write_text(json.dumps({
        "schema_version": "1.0",
        "report_id": "source-pattern-review-browser-smoke",
        "status": "source_pattern_review_browser_unavailable",
        "queue_item_count": 107,
        "checks": {
            **static_checks,
            "browser_interactions": False,
            "search_filter": False,
            "local_save_reload": False,
            "partial_wave_2_export": False,
            "export_fail_closed": False,
            "complete_json_export": False,
        },
        "error": error,
        "claim_boundary": "Browser interactions were not tested; this is not a passing runtime receipt and it creates no human review, recurrence, learner, listener or effectiveness evidence.",
    }, indent=2) + "\n", encoding="utf-8")


def record_runtime_status(status: str, static_checks: dict, error: str | None = None) -> None:
    REPORT.write_text(json.dumps({
        "schema_version": "1.0",
        "report_id": "source-pattern-review-browser-smoke",
        "status": status,
        "queue_item_count": 107,
        "checks": {**static_checks, "browser_interactions": False, "dedicated_wave_2_partial_export": False},
        "error": error,
        "claim_boundary": "A running or failed smoke test is not a passing browser receipt and creates no human review, recurrence, learner, listener or effectiveness evidence.",
    }, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("source-pattern review browser smoke unavailable: playwright is not installed")
        return 2
    static_checks = validate_static_context()
    failed_static_checks = [name for name, passed in static_checks.items() if not passed]
    if failed_static_checks:
        record_runtime_status("source_pattern_review_static_validation_failed", static_checks, ", ".join(failed_static_checks))
        print("source-pattern review static context validation failed: " + ", ".join(failed_static_checks))
        return 1
    record_runtime_status("source_pattern_review_browser_smoke_running", static_checks)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    port = server.server_address[1]
    try:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            except Exception as exc:
                record_browser_unavailable(str(exc), static_checks)
                print(f"source-pattern review browser runtime unavailable: {exc}")
                return 2
            page = browser.new_page(accept_downloads=True)
            page.goto(f"http://127.0.0.1:{port}/site/pattern-review.html", wait_until="networkidle")
            assert page.locator(".review-card").count() == 107
            for item_id, excerpt_count in (("ali-001", 6), ("drybar-001", 6), ("ted-001", 5)):
                card = page.locator(f'.review-card[data-search^="{item_id}"]')
                assert card.count() == 1
                assert card.locator(".context-reference").count() == 3
                assert card.locator("blockquote").count() == excerpt_count
                transcript_link = card.locator('a[href*="/raw-material/youtube/transcripts/"]').first
                cue_link = card.locator('a[href*="/raw-material/youtube/transcripts/"][href*="/cues/"]').first
                assert page.request.get(urljoin(page.url, transcript_link.get_attribute("href"))).ok
                assert page.request.get(urljoin(page.url, cue_link.get_attribute("href"))).ok
                assert card.locator('a[href*="youtube.com/watch"]').count() == 3
            page.locator("#search").fill("Charisma")
            assert page.locator(".review-card:not([hidden])").count() > 0
            page.locator("#search").fill("wave 2")
            assert page.locator(".review-card:not([hidden])").count() == 19
            page.locator("#search").fill("")
            page.locator("#reviewer-code").fill("synthetic-browser-smoke")
            page.locator("#save").click()
            assert "Draft saved" in page.locator("#export-status").inner_text()
            page.reload(wait_until="networkidle")
            page.wait_for_function("document.getElementById('reviewer-code').value === 'synthetic-browser-smoke'")
            assert page.locator("#reviewer-code").input_value() == "synthetic-browser-smoke"
            page.locator("#independence").check()
            # The export must fail closed when nothing is completed, while
            # allowing the targeted 19-item wave-2 batch to be returned alone.
            page.locator("#export").click()
            assert "at least one item" in page.locator("#export-status").inner_text()
            wave_2_ids = {
                row["review_item_id"]
                for row in json.loads((ROOT / "analysis" / "wave-2-unified-candidate-crosswalk.json").read_text())["rows"]
            }
            assert len(wave_2_ids) == 19
            for item_id in sorted(wave_2_ids):
                card = page.locator(f'.review-card[data-search^="{item_id}"]')
                card.locator(".review-decision").select_option("indeterminate")
                card.locator(".context-inspected").check()
            with page.expect_download() as partial_download:
                page.locator("#export").click()
            partial_path = partial_download.value.path()
            partial = json.loads(partial_path.read_text())
            assert len(partial["records"]) == 19
            assert partial["review_status"] == "partial"
            assert len(partial["unreviewed_item_ids"]) == 88
            assert {record["review_item_id"] for record in partial["records"]} == wave_2_ids
            validation = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_source_pattern_review_export.py"), str(partial_path)], capture_output=True, text=True)
            assert validation.returncode == 0, validation.stdout + validation.stderr
            assert "19/107" in validation.stdout and "wave-2 coverage 19/19" in validation.stdout

            for card in page.locator(".review-card").all():
                if not card.locator(".review-decision").input_value():
                    card.locator(".review-decision").select_option("indeterminate")
                if not card.locator(".context-inspected").is_checked():
                    card.locator(".context-inspected").check()
            with page.expect_download() as complete_download:
                page.locator("#export").click()
            complete_path = complete_download.value.path()
            exported = json.loads(complete_path.read_text())
            assert len(exported["records"]) == 107
            assert exported["review_status"] == "complete"
            assert exported["unreviewed_item_ids"] == []
            assert exported["independence_confirmed"] is True
            assert all(record["context_inspected"] for record in exported["records"])
            validation = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_source_pattern_review_export.py"), str(complete_path)], capture_output=True, text=True)
            assert validation.returncode == 0, validation.stdout + validation.stderr
            assert "107/107" in validation.stdout

            wave_page = browser.new_page(accept_downloads=True)
            wave_page.goto(f"http://127.0.0.1:{port}/site/pattern-review-wave-2.html", wait_until="networkidle")
            assert wave_page.locator(".review-card").count() == 19
            assert wave_page.evaluate("allQueueIds.length") == 107
            assert "88 combined-queue IDs are intentionally not shown" in wave_page.locator(".reviewer-bar").inner_text()
            wave_page.locator("#reviewer-code").fill("synthetic-wave2-review")
            wave_page.locator("#independence").check()
            wave_page.locator("#export").click()
            assert "at least one item" in wave_page.locator("#export-status").inner_text()
            for item_id in sorted(wave_2_ids):
                card = wave_page.locator(f'.review-card[data-search^="{item_id}"]')
                card.locator(".review-decision").select_option("indeterminate")
                card.locator(".context-inspected").check()
            with wave_page.expect_download() as focused_download:
                wave_page.locator("#export").click()
            focused_path = focused_download.value.path()
            focused = json.loads(focused_path.read_text())
            assert len(focused["records"]) == 19
            assert focused["queue_item_count"] == 107 and focused["review_status"] == "partial"
            assert len(focused["unreviewed_item_ids"]) == 88
            assert {record["review_item_id"] for record in focused["records"]} == wave_2_ids
            validation = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_source_pattern_review_export.py"), str(focused_path)], capture_output=True, text=True)
            assert validation.returncode == 0, validation.stdout + validation.stderr
            assert "19/107" in validation.stdout and "wave-2 coverage 19/19" in validation.stdout

            with tempfile.TemporaryDirectory(prefix="wave2-review-pack-smoke-") as temp_dir:
                package_root = Path(temp_dir).resolve()
                pack_path = ROOT / "deliverables" / "wave-2-full-context-reviewer-pack.zip"
                with zipfile.ZipFile(pack_path) as archive:
                    for member in archive.infolist():
                        target = (package_root / member.filename).resolve()
                        assert package_root in target.parents, member.filename
                    archive.extractall(package_root)
                package_handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=package_root)
                package_server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), package_handler)
                package_thread = threading.Thread(target=package_server.serve_forever, daemon=True)
                package_thread.start()
                try:
                    package_page = browser.new_page(accept_downloads=True)
                    package_page.goto(f"http://127.0.0.1:{package_server.server_address[1]}/site/pattern-review-wave-2.html", wait_until="networkidle")
                    assert package_page.locator(".review-card").count() == 19
                    assert package_page.evaluate("allQueueIds.length") == 107
                    context_urls = sorted(set(package_page.locator('a[href*="../raw-material/youtube/"]').evaluate_all("nodes => nodes.map(node => node.href)")))
                    assert len(context_urls) == 86
                    assert all(package_page.request.get(url).ok for url in context_urls)
                    package_page.locator("#reviewer-code").fill("synthetic-portable-wave2-review")
                    package_page.locator("#independence").check()
                    for item_id in sorted(wave_2_ids):
                        card = package_page.locator(f'.review-card[data-search^="{item_id}"]')
                        card.locator(".review-decision").select_option("indeterminate")
                        card.locator(".context-inspected").check()
                    with package_page.expect_download() as package_download:
                        package_page.locator("#export").click()
                    package_export = json.loads(package_download.value.path().read_text())
                    assert len(package_export["records"]) == 19
                    assert package_export["queue_item_count"] == 107
                    assert len(package_export["unreviewed_item_ids"]) == 88
                    package_validation = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_source_pattern_review_export.py"), str(package_download.value.path())], capture_output=True, text=True)
                    assert package_validation.returncode == 0, package_validation.stdout + package_validation.stderr
                    assert "19/107" in package_validation.stdout and "wave-2 coverage 19/19" in package_validation.stdout
                    package_page.close()
                finally:
                    package_server.shutdown()
                    package_server.server_close()
                    package_thread.join(timeout=5)
            browser.close()
    except Exception as exc:
        record_runtime_status("source_pattern_review_browser_smoke_failed", static_checks, str(exc))
        raise
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=5)
    REPORT.write_text(json.dumps({"schema_version": "1.0", "report_id": "source-pattern-review-browser-smoke", "status": "source_pattern_review_browser_smoke_passed", "queue_item_count": 107, "checks": {**static_checks, "wave_2_search_returns_19_items": True, "browser_interactions": True, "search_filter": True, "local_save_reload": True, "partial_wave_2_export": True, "dedicated_wave_2_surface": True, "dedicated_wave_2_partial_export": True, "portable_context_assets_open": True, "portable_wave_2_partial_export": True, "export_fail_closed": True, "complete_json_export": True}, "claim_boundary": "Local runtime smoke test only; it does not create human review, recurrence, learner, listener or effectiveness evidence. Synthetic smoke decisions are discarded and are not human review records."}, indent=2) + "\n", encoding="utf-8")
    print("source-pattern review browser smoke: local and portable 19-card pages; all bundled context links; 19/107 export preserves 88 unreviewed IDs; full 107-card export and validators passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
