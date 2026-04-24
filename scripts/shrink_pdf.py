#!/usr/bin/env python3
"""
Post-process a Slidev PDF to reduce file size.

Default: lossless cleanup (keeps icons, vector art, and fonts intact).

Avoid --lossy for decks exported with Playwright/Chrome: it uses PyMuPDF's
rewrite_images() and can strip or break repeated graphics, masks, and icons.
"""
from __future__ import annotations

import argparse
import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError as e:
    print("Install PyMuPDF:  python3 -m pip install pymupdf", file=sys.stderr)
    raise SystemExit(1) from e


def lossless_shrink(
    src: str,
    out: str,
) -> int:
    doc = fitz.open(src)
    try:
        doc.save(
            out,
            garbage=4,
            deflate=True,
            clean=True,
            use_objstms=1,
        )
    finally:
        doc.close()
    return os.path.getsize(out)


def lossy_shrink(
    src: str,
    out: str,
    quality: int,
) -> int:
    doc = fitz.open(src)
    try:
        doc.rewrite_images(quality=quality)
        doc.save(
            out,
            garbage=4,
            deflate=True,
            clean=True,
            use_objstms=1,
        )
    finally:
        doc.close()
    return os.path.getsize(out)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "source",
        nargs="?",
        default="slides-export.pdf",
        help="Input PDF (default: slides-export.pdf)",
    )
    p.add_argument(
        "-o",
        "--out",
        default="slides-export.compressed.pdf",
        help="Output PDF (default: slides-export.compressed.pdf)",
    )
    p.add_argument(
        "--lossy",
        action="store_true",
        help="Recompress embedded images (can break icons/vectors in Slidev PDFs — not recommended)",
    )
    p.add_argument(
        "--quality",
        type=int,
        default=80,
        metavar="0-100",
        help="JPEG quality for --lossy (default: 80)",
    )
    args = p.parse_args()
    if not os.path.isfile(args.source):
        print(f"Not found: {args.source}", file=sys.stderr)
        raise SystemExit(1)

    before = os.path.getsize(args.source)
    if args.lossy:
        print(
            "Warning: --lossy may break icons, patterns, and form graphics in Chrome/Slidev PDFs. "
            "Use the default (lossless) to preserve them.\n",
            file=sys.stderr,
        )
        after = lossy_shrink(args.source, args.out, max(0, min(100, args.quality)))
    else:
        after = lossless_shrink(args.source, args.out)

    print(
        f"Wrote {args.out}  —  "
        f"{before / 1024 / 1024:.1f} MiB → {after / 1024 / 1024:.1f} MiB  "
        f"({100 * after / before:.1f}%)"
    )


if __name__ == "__main__":
    main()
