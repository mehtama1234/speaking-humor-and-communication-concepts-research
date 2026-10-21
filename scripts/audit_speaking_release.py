#!/usr/bin/env python3
"""Audit release scope and artifact identity, not prose quality or source truth."""
from hashlib import sha256
from pathlib import Path
import json
import re
import zipfile
from build_speaking_source_catalog import collect_sources

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    inventory = ROOT / "analysis/transcript-backed-concrete-speaking-approaches.md"
    originals = dict(re.findall(r"^## (\d+)\. (.+)$", inventory.read_text(), re.M))
    chapters = sorted((ROOT / "writeups/speaking-practice").glob("[0-9][0-9]-*.md"))
    paths = sorted((ROOT / "writeups/speaking-curricula").glob("[0-9][0-9]-*.md"))
    assert set(originals) == {str(n) for n in range(1, 28)}
    assert [p.name[:2] for p in chapters] == [f"{n:02}" for n in range(1, 28)]
    assert [p.name[:2] for p in paths] == [f"{n:02}" for n in range(1, 12)]
    expected_curricula = ["starter", "business-communication", "clarity-and-anti-rambling", "confidence-and-composure", "delivery-and-vocal-presence", "interview-and-hard-question", "multilingual-clarity-and-accent-pressure", "presentation-and-formal-speaking", "skeptical-room-and-objection-handling", "social-speaking-and-humor", "storytelling-and-memorability"]
    rows = []
    for p in chapters + paths:
        text = p.read_text()
        is_path = p in paths
        n = int(p.name[:2])
        if is_path:
            original = ROOT / "analysis" / (expected_curricula[n-1] + "-curriculum.md")
            assert original.is_file() and original.name in text, p
            assert len(re.findall(r"^## Session \d+:", text, re.M)) >= 6, p
            original_title = original.read_text().splitlines()[0].lstrip("# ")
        else:
            original = inventory
            original_title = originals[str(n)]
            assert re.search(r"^## (?:The principle|Practice:)", text, re.M), p
            assert "## Practice:" in text and "## Source" in text, p
        assert len(text.split()) > 900, p
        assert re.search(r"invented|fictional|original teaching", text, re.I), p
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" not in target and not target.startswith("#"):
                assert (p.parent / target).resolve().is_file(), (p, target)
        rows.append({"file": str(p.relative_to(ROOT)), "title": text.splitlines()[0][2:], "original": str(original.relative_to(ROOT)), "original_title": original_title, "words": len(text.split()), "sha256": digest(p)})
    current = collect_sources()
    assert current == json.loads((ROOT / "analysis/speaking-source-catalog.json").read_text()), "Stale source catalog"
    out = ROOT / "deliverables/speaking-practice"
    receipt = json.loads((out / "export-check.json").read_text())
    assert receipt["status"] == "portable_first_edition_technical_checks_pass"
    for reader in (ROOT / "site/speaking-practice.html", out / "speaking-practice.html"):
        html = reader.read_text()
        assert "The detailed guide · First edition" in html
        assert "Editorial preview" not in html and "These drafts are not the completed book" not in html
    assert "PORTABLE FIRST EDITION" in (out / "README.txt").read_text()
    for name, expected in receipt["authored_input_hashes"].items():
        assert digest(ROOT / name) == expected, f"Stale export input: {name}"
    for name, expected in receipt["archive_payload_hashes"].items():
        assert digest(out / name) == expected, f"Stale payload: {name}"
    assert digest(out / "speaking-practice.zip") == receipt["archive_sha256"]
    with zipfile.ZipFile(out / "speaking-practice.zip") as archive:
        assert set(archive.namelist()) == set(receipt["archive_payload_hashes"]) | {"manifest.json"}
        assert archive.testzip() is None
        assert json.loads(archive.read("manifest.json")) == receipt["archive_payload_hashes"]
        for name, expected in receipt["archive_payload_hashes"].items():
            assert sha256(archive.read(name)).hexdigest() == expected
    for page in (ROOT / "site/index.html", ROOT / "site/curriculum.html"):
        assert "speaking-practice.html" in page.read_text(), page
    for ext in ("pdf", "zip"):
        assert f"speaking-practice.{ext}" in (ROOT / "site/curriculum.html").read_text()
    assert receipt["chapters"] == 27 and receipt["learning_paths"] == 11
    assert not receipt["pdf_text_outside_page"]
    assert not json.loads((out / "pdf-missing-blocks.json").read_text())
    report = {"status": "technical_scope_and_identity_pass", "limitation": "Does not replace the substantive editorial review, verify source claims independently, or certify accessibility or licensing.", "units": rows, "source_count": current["source_count"], "main_manuscript_words": sum(r["words"] for r in rows), "export_receipt_sha256": digest(out / "export-check.json"), "archive_sha256": receipt["archive_sha256"], "pdf_pages": receipt["pdf_pages"]}
    (ROOT / "analysis/speaking-release-technical-audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"PASS: 27 inventory mappings, 11 curriculum mappings, all manuscript links, {current['source_count']} source identities, export freshness and exact archive payloads; {report['main_manuscript_words']} words")


if __name__ == "__main__":
    main()
