"""Validate relative README links and the static synthetic scorecard."""
from pathlib import Path
from xml.etree import ElementTree as ET
import re

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]+\")?\)")

def check():
    missing = []
    for file in ROOT.rglob("*.md"):
        for href in LINK.findall(file.read_text(encoding="utf-8")):
            if href.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = href.split("#", 1)[0]
            if not target:
                continue
            path = (file.parent / target).resolve()
            if not path.is_relative_to(ROOT.resolve()) or not path.exists():
                missing.append(f"{file.relative_to(ROOT)} -> {href}")
    path = ROOT / "docs" / "reconciliation-scorecard.svg"
    svg = ET.parse(path).getroot()
    assert svg.tag.endswith("svg")
    content = path.read_text(encoding="utf-8").lower()
    assert "<script" not in content
    assert not re.search(r"<image\b[^>]*https?://", content)
    assert not missing, "Broken local links:\n" + "\n".join(missing)
    print("PASS: Markdown links and illustrative SVG")


if __name__ == "__main__":
    check()
