#!/usr/bin/env python3
"""
Extract inline CSS from HTML templates into separate .css files.
Replaces <style>...</style> with <link rel="stylesheet" href="...">.

Usage:
    python scripts/extract_css.py
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
CSS_DIR = ASSETS_DIR / "css"

TEMPLATE_MAP = {
    "card_template_wuxia.html": "wuxia.css",
    "card_template_wuxia_conquest.html": "wuxia_conquest.css",
    "card_template_wuxia_pipeline.html": "wuxia_pipeline.css",
    "card_template_newspaper.html": "newspaper.css",
    "card_template_web.html": "web.css",
    "card_template_catalog.html": "catalog.css",
}


def extract_css(html_content, template_name):
    """Extract CSS content from <style> tag in HTML and clean formatting."""
    pattern = r"<style>\s*\n(.*?)</style>"
    match = re.search(pattern, html_content, re.DOTALL)
    if not match:
        print(f"  [SKIP] {template_name}: no <style> tag found")
        return None, None

    css_content = match.group(1)
    # Remove leading whitespace from each line (inline HTML indentation)
    css_lines = []
    for line in css_content.split("\n"):
        css_lines.append(line.lstrip() if line.strip() else "")
    css_content = "\n".join(css_lines).strip()
    return match.group(0), css_content


def replace_style_with_link(html_content, template_name, css_filename):
    """Replace <style> tag with <link rel='stylesheet'> tag."""
    pattern = r"<style>\s*\n.*?</style>"
    replacement = (
        f'<link rel="stylesheet" href="css/{css_filename}">\n'
        f"  <!-- Inline CSS extracted to assets/css/{css_filename} -->"
    )
    new_content = re.sub(pattern, replacement, html_content, count=1, flags=re.DOTALL)
    return new_content


def main():
    CSS_DIR.mkdir(parents=True, exist_ok=True)

    for template_name, css_filename in TEMPLATE_MAP.items():
        template_path = ASSETS_DIR / template_name
        css_path = CSS_DIR / css_filename

        if not template_path.exists():
            print(f"  [SKIP] {template_name}: file not found")
            continue

        # Read template
        original = template_path.read_text(encoding="utf-8")

        # Extract CSS
        style_tag, css_content = extract_css(original, template_name)
        if css_content is None:
            continue

        # Write CSS file
        css_path.write_text(css_content, encoding="utf-8")
        print(f"  [OK] css/{css_filename} ({len(css_content)} chars)")

        # Replace <style> with <link> in template
        updated = replace_style_with_link(original, template_name, css_filename)
        template_path.write_text(updated, encoding="utf-8")
        print(f"  [OK] {template_name}: <style> replaced with <link>")

    print(f"\nDone. CSS files extracted to {CSS_DIR}")


if __name__ == "__main__":
    main()
