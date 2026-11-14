#!/usr/bin/env python3
"""Inline an official Unidcom Base64 logo into an editorial HTML file."""

from __future__ import annotations

import argparse
import base64
from pathlib import Path


TOKEN = "{{UNIDCOM_LOGO_DATA_URI}}"
VARIANTS = ("allwhite", "allblack", "color", "white")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replace the Unidcom logo token with an official PNG data URI."
    )
    parser.add_argument("html", type=Path, help="HTML composition containing the logo token")
    parser.add_argument(
        "--variant",
        choices=VARIANTS,
        default="allwhite",
        help="Official logo variant (default: allwhite for dark backgrounds)",
    )
    parser.add_argument("--output", type=Path, help="Output path; defaults to updating the input")
    args = parser.parse_args()

    html_path = args.html.resolve()
    output_path = args.output.resolve() if args.output else html_path
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    logo_path = assets_dir / f"logo-{args.variant}-b64.txt"

    html = html_path.read_text(encoding="utf-8")
    if TOKEN not in html:
        raise SystemExit(f"Logo token not found: {TOKEN}")

    payload = "".join(logo_path.read_text(encoding="utf-8").split())
    try:
        decoded = base64.b64decode(payload, validate=True)
    except ValueError as exc:
        raise SystemExit(f"Invalid Base64 asset: {logo_path}") from exc
    if not decoded.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit(f"Logo asset is not a PNG: {logo_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        html.replace(TOKEN, f"data:image/png;base64,{payload}"), encoding="utf-8"
    )
    print(f"Inlined official Unidcom logo ({args.variant}) into {output_path}")


if __name__ == "__main__":
    main()
