#!/usr/bin/env python3
"""
Recursively optimize raster files under public/ (JPEG, PNG, WebP).

- Downscales if the long edge exceeds --max-edge (keeps aspect ratio, LANCZOS).
- Re-encodes for smaller on-disk size.
- Skips animated images and other frames.
- Replaces a file only when the output is smaller, or the image was downscaled
  (rare: resize then replace even if a single recompress is slightly larger).

Usage:
  .venv-face/bin/python3 scripts/optimize_raster_images.py
  .venv-face/bin/python3 scripts/optimize_raster_images.py --dry-run
  npm run optimize:public
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = 200_000_000

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PUBLIC = ROOT / "public"
RASTER_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def is_animated(im: Image.Image) -> bool:
    return getattr(im, "n_frames", 1) > 1


def long_edge(w: int, h: int) -> int:
    return max(w, h)


def downscale_if_needed(im: Image.Image, max_edge: int) -> tuple[Image.Image, bool]:
    w, h = im.size
    if long_edge(w, h) <= max_edge:
        return im, False
    s = max_edge / float(long_edge(w, h))
    nw = max(1, int(round(w * s)))
    nh = max(1, int(round(h * s)))
    return im.resize((nw, nh), Image.LANCZOS), True


def write_jpeg(
    im: Image.Image, path: Path, quality: int, subsampling: int
) -> None:
    if im.mode == "P" and "transparency" not in im.info:
        work = im.convert("RGB")
    elif im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        r = im.convert("RGBA")
        bg = Image.new("RGB", r.size, (255, 255, 255))
        work = Image.alpha_composite(bg.convert("RGBA"), r).convert("RGB")
    else:
        work = im.convert("RGB")
    work.save(
        path,
        format="JPEG",
        quality=quality,
        optimize=True,
        progressive=True,
        subsampling=subsampling,
    )


def write_png(im: Image.Image, path: Path) -> None:
    w = im
    if w.mode == "P" and "transparency" in w.info:
        w = w.convert("RGBA")
    elif w.mode == "P":
        w = w.convert("RGB")
    if w.mode not in ("RGB", "RGBA", "L", "LA"):
        w = w.convert("RGBA" if w.mode in ("CMYK",) else "RGB")
    w.save(path, format="PNG", optimize=True, compress_level=9)


def write_webp(
    im: Image.Image, path: Path, quality: int, method: int
) -> None:
    w = im
    if w.mode == "P" and "transparency" in w.info:
        w = w.convert("RGBA")
    elif w.mode == "P":
        w = w.convert("RGB")
    if w.mode not in ("RGB", "RGBA", "L", "P"):
        w = w.convert("RGB")
    w.save(
        path,
        format="WEBP",
        quality=quality,
        method=method,
    )


def process_one(
    path: Path,
    max_edge: int,
    jpeg_quality: int,
    jpeg_subsampling: int,
    webp_quality: int,
    webp_method: int,
    dry_run: bool,
) -> tuple[int, int, str]:
    before = path.stat().st_size
    ext = path.suffix.lower()
    try:
        with Image.open(path) as src:
            src = ImageOps.exif_transpose(src)
            if is_animated(src):
                return before, before, "skip:animated"
            im = src.copy()
    except (OSError, ValueError) as e:
        return before, before, f"err:read:{e!s}"[:200]

    im, resized = downscale_if_needed(im, max_edge)
    if dry_run:
        return before, 0, "dry"

    suffix = {".jpeg": ".jpg"}.get(ext, ext)
    _fd, tmp = tempfile.mkstemp(
        suffix=suffix, prefix=path.stem + "._opt_", dir=path.parent
    )
    os.close(_fd)
    tmp_path = Path(tmp)
    try:
        if ext in (".jpg", ".jpeg"):
            write_jpeg(
                im, tmp_path, quality=jpeg_quality, subsampling=jpeg_subsampling
            )
        elif ext == ".png":
            write_png(im, tmp_path)
        elif ext == ".webp":
            write_webp(
                im, tmp_path, quality=webp_quality, method=webp_method
            )
        else:
            tmp_path.unlink(missing_ok=True)
            return before, before, "skip:ext"

        after = tmp_path.stat().st_size
        if (after < before) or resized:
            os.replace(tmp_path, path)
            return before, after, "ok"
        tmp_path.unlink(missing_ok=True)
        return before, before, "skip:not-smaller"
    except OSError:
        tmp_path.unlink(missing_ok=True)
        return before, before, "err:write"


def iter_raster_files(base: Path) -> list[Path]:
    out: list[Path] = []
    for p in base.rglob("*"):
        if p.is_file() and p.suffix.lower() in RASTER_EXT:
            out.append(p)
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--public-dir", type=Path, default=DEFAULT_PUBLIC, help="Root (default: ./public)"
    )
    ap.add_argument(
        "--max-edge",
        type=int,
        default=2560,
        help="Max long side in px before downscale (default: 2560)",
    )
    ap.add_argument("--jpeg-quality", type=int, default=82)
    ap.add_argument("--jpeg-subsampling", type=int, default=2, choices=(0, 1, 2))
    ap.add_argument("--webp-quality", type=int, default=80)
    ap.add_argument("--webp-method", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    base = args.public_dir.resolve()
    if not base.is_dir():
        print(f"Not a directory: {base}", file=sys.stderr)
        return 1

    files = iter_raster_files(base)
    size_before = sum(p.stat().st_size for p in files) if files else 0
    n_ok = n_skip = n_err = 0

    for path in files:
        rel = path.relative_to(base)
        b, a, status = process_one(
            path,
            max_edge=args.max_edge,
            jpeg_quality=args.jpeg_quality,
            jpeg_subsampling=args.jpeg_subsampling,
            webp_quality=args.webp_quality,
            webp_method=args.webp_method,
            dry_run=args.dry_run,
        )
        if status == "ok":
            n_ok += 1
            print(
                f"[ok]  {rel}  {b} -> {a} bytes ({100.0 * a / b if b else 0:.0f}%)"
            )
        elif status == "dry":
            n_skip += 1
            print(f"[dry] {rel}  {b} bytes")
        elif status.startswith("skip:"):
            n_skip += 1
            print(f"[{status}] {rel}  {b} bytes")
        else:
            n_err += 1
            print(f"[{status}] {rel}", file=sys.stderr)

    size_after = sum(p.stat().st_size for p in files) if (files and not args.dry_run) else size_before
    if not args.dry_run and files and size_before:
        print(
            f"\nBefore: {size_before/1024/1024:.1f} MiB  |  After: {size_after/1024/1024:.1f} MiB  |  "
            f"saved: {(size_before - size_after)/1024/1024:.1f} MiB"
        )
    elif args.dry_run:
        print(f"\nDry run: {len(files)} rasters, ~{size_before/1024/1024:.1f} MiB total (unchanged)")

    print(
        f"Rasters: {len(files)}, updated: {n_ok}, skipped: {n_skip}, errors: {n_err}"
    )
    return 0 if n_err == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
