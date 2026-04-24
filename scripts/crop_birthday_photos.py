#!/usr/bin/env python3
"""
Detect the best portrait among configured people groups (birthday + certification),
crop tightly around the face (with headroom + shoulders), and export consistent
1000x1000 JPEG avatars to public subfolders.

Usage:
    .venv-face/bin/python3 scripts/crop_birthday_photos.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import cv2
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PHOTOS_ROOT = ROOT / "assets" / "individual_photos"
OUTPUT_SIZE = 1000

# (slug, display_name, [candidate_folder_names_relative_to_PHOTOS_ROOT_or_direct_paths])
# Birthday/certification entries list directories to scan for files beginning
# with the person's name. New-member entries can pass direct file paths.
BIRTHDAY_PEOPLE = [
    ("daniel-tran", "Daniel Tran", ["Individual Photos 2026", "Individual Photos 2025"]),
    ("hien-vuong", "Hien Vuong", ["Individual Photos 2026"]),
    ("pierrick-libert", "Pierrick Libert", ["Individual Photos 2026", "Individual Photos 2025"]),
    ("tuan-nguyen", "Tuan Nguyen", ["Individual Photos 2026"]),
    ("tai-le", "Tai Le", ["Individual Photos 2026"]),
    ("phu-ha", "Phu Ha", ["Individual Photos 2025"]),
    ("thao-mai", "Thao Mai", ["Individual Photos 2026", "Individual Photos 2025"]),
]

CERTIFICATION_PEOPLE = [
    ("tuan-nguyen", "Tuan Nguyen", ["Individual Photos 2026", "Individual Photos 2025"]),
    ("quyen-nguyen", "Quyen Nguyen", ["Individual Photos 2026", "Individual Photos 2025"]),
    ("manh-pham", "Manh Pham", ["Individual Photos 2026", "Individual Photos 2025"]),
]

NEW_MEMBER_PEOPLE = [
    ("nghia-doan", "Nghia Doan", ["assets/new-member/nghia.png"]),
    ("tam-nguyen", "Tam Nguyen", ["assets/new-member/tam.png"]),
]

# Portraits used on the `project` layout's team grid. Folder order controls the
# "prefer latest year" selection policy (2026 first, then 2025 fallback).
TEAM_PEOPLE = [
    # GEDAT
    ("travis-le", "Travis Le", ["Individual Photos 2026"]),
    ("sieu-nguyen", "Sieu Nguyen", ["Individual Photos 2025"]),
    ("anh-truong", "Anh Truong", ["Individual Photos 2026"]),
    ("hien-vuong", "Hien Vuong", ["Individual Photos 2026"]),
    ("anh-tran", "Anh Tran", ["Individual Photos 2025"]),
    ("michael-nguyen", "Michael Nguyen", ["Individual Photos 2026"]),
    ("thanh-nguyen", "Thanh Nguyen", ["Individual Photos 2025"]),
    ("nathan-nguyen", "Nathan Nguyen", ["Individual Photos 2026"]),
    # JTL — Cloud Platform
    ("thao-mai", "Thao Mai", ["Individual Photos 2026", "Individual Photos 2025"]),
    ("khoi-ngo", "Khoi Ngo", ["Individual Photos 2025"]),
    ("nghia-nguyen", "Nghia Nguyen", ["Individual Photos 2025"]),
    ("dat-tran", "Dat Tran", ["Individual Photos 2026"]),
    ("ngoc-tran", "Ngoc Tran", ["Individual Photos 2026"]),
    ("hoang-dinh", "Hoang Dinh", ["Individual Photos 2025"]),
    ("quyen-nguyen", "Quyen Nguyen", ["Individual Photos 2025"]),
    ("kane-vo", "Kane Vo", ["Individual Photos 2025"]),
    ("tuan-nguyen", "Tuan Nguyen", ["Individual Photos 2026"]),
    ("phi-luong", "Phi Luong", ["Individual Photos 2026"]),
    # JTL — WMS Dashboard
    ("tony-nguyen", "Tony Nguyen", ["Individual Photos 2026"]),
    ("kiet-huynh", "Kiet Huynh", ["Individual Photos 2026"]),
    ("stefan-kull", "Stefan Kull", ["Individual Photos 2026"]),
    # DAWN × Evolution
    ("trung-tran", "Trung Tran", ["Individual Photos 2026"]),
    # MaiVita
    ("linh-pham", "Linh Pham", ["Individual Photos 2025"]),
    ("thach-huynh", "Thach Huynh", ["Individual Photos 2025"]),
    # CODE LEAP Clockify
    ("pierrick-libert", "Pierrick Libert", ["Individual Photos 2026", "Individual Photos 2025"]),
    ("alex-huynh", "Alex Huynh", ["Individual Photos 2025"]),
    ("thanh-hoang", "Thanh Hoang", ["Individual Photos 2025"]),
    ("viet-vo", "Viet Vo", ["Individual Photos 2026"]),
]

# Optional one-off overrides when automatic face detection selects a bad frame.
# Key is display name; value is an exact preferred filename.
PREFERRED_FILE_OVERRIDE = {
    "Thao Mai": "Thao Mai 3.jpg",
}

CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
CASCADE_ALT = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
)


def find_candidates(display_name: str, folders: list[str]) -> list[Path]:
    matches: list[Path] = []
    prefix = display_name.lower()
    for idx, folder in enumerate(folders):
        given = Path(folder)
        if given.is_absolute():
            target = given
        else:
            target = ROOT / given
            if not target.exists():
                target = PHOTOS_ROOT / folder

        if target.is_file():
            if target.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                matches.append(target)
            continue

        if not target.is_dir():
            continue

        for p in target.iterdir():
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
                continue
            if p.name.lower().startswith(prefix):
                matches.append(p)

    # Prefer deterministic order based on configured folder/path order.
    folder_order = {str(Path(f).name): i for i, f in enumerate(folders)}
    matches.sort(key=lambda p: (folder_order.get(p.parent.name, 999), p.name.lower()))
    return matches


def extract_trailing_index(path: Path) -> int:
    """
    Return trailing numeric suffix from filename stem, e.g.:
    "Daniel Tran 4.jpg" -> 4, "Tai Le 1_.jpg" -> 1, no suffix -> 0
    """
    m = re.search(r"(\d+)(?:\D*)$", path.stem)
    return int(m.group(1)) if m else 0


def sort_by_latest_image(candidates: list[Path]) -> list[Path]:
    """Sort newest-looking image first (higher trailing index first)."""
    return sorted(
        candidates,
        key=lambda p: (-extract_trailing_index(p), p.name.lower()),
    )


def detect_best_face(image_path: Path):
    """Return (x, y, w, h) of the largest high-confidence face, or None."""
    data = cv2.imread(str(image_path))
    if data is None:
        return None, None
    gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    all_faces = []
    for cascade in (CASCADE, CASCADE_ALT):
        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(120, 120),
        )
        for (x, y, w, h) in faces:
            all_faces.append((int(x), int(y), int(w), int(h)))

    if not all_faces:
        return None, data

    # Choose the biggest face (assume that's the subject).
    x, y, w, h = max(all_faces, key=lambda f: f[2] * f[3])
    return (x, y, w, h), data


def crop_portrait(img_bgr, face):
    """Expand the face box into a square portrait crop with headroom + shoulders."""
    img_h, img_w = img_bgr.shape[:2]
    x, y, w, h = face
    cx = x + w / 2
    # Shift vertical center a bit above the face center so we keep more shoulders.
    cy = y + h / 2 + h * 0.35

    # Target crop side ~= 3.0x face height — covers hair to mid-chest.
    side = int(h * 3.0)

    # Clamp so the square stays inside the image.
    side = min(side, img_w, img_h)

    half = side / 2
    x0 = int(max(0, min(img_w - side, cx - half)))
    y0 = int(max(0, min(img_h - side, cy - half)))
    x1 = x0 + side
    y1 = y0 + side

    return img_bgr[y0:y1, x0:x1]


def pick_best_candidate(display_name: str, candidates: list[Path]):
    best = None  # (score, path, face, img_bgr)
    for path in candidates:
        face, img = detect_best_face(path)
        if face is None or img is None:
            continue
        score = face[2] * face[3]
        if best is None or score > best[0]:
            best = (score, path, face, img)
    return best


def pick_preferred_candidate(display_name: str, folders: list[str], all_candidates: list[Path]):
    """
    Selection policy:
    1) Prefer latest year folder order as listed in `folders` (e.g. 2026 before 2025).
    2) Inside that folder, prefer latest image index (e.g. `... 4.jpg` over `... 1.jpg`).
    3) Use first file in that order where a face is detected.
    4) If no face in that folder, fall back to centered crop of latest image there.
    5) Only then continue to the next (older) folder.
    """
    grouped: dict[str, list[Path]] = {folder: [] for folder in folders}
    for p in all_candidates:
        for folder in folders:
            folder_path = Path(folder)
            if folder_path.is_file():
                if p.resolve() == folder_path.resolve():
                    grouped[folder].append(p)
            else:
                if p.parent.name == folder_path.name:
                    grouped[folder].append(p)

    preferred_filename = PREFERRED_FILE_OVERRIDE.get(display_name)

    for folder in folders:
        candidates = sort_by_latest_image(grouped.get(folder, []))
        if not candidates:
            continue

        # Optional explicit source-image override (used for problematic cases).
        if preferred_filename:
            override_path = next(
                (p for p in candidates if p.name == preferred_filename),
                None,
            )
            if override_path is not None:
                face, img = detect_best_face(override_path)
                if img is not None:
                    if face is not None:
                        return override_path, face, img, False
                    return override_path, None, img, True

        # Prefer latest image in this year where face detection succeeds.
        for path in candidates:
            face, img = detect_best_face(path)
            if face is not None and img is not None:
                return path, face, img, False

        # No face in this year: still prefer latest image as a fallback crop.
        src = candidates[0]
        img = cv2.imread(str(src))
        if img is not None:
            return src, None, img, True

    return None


def run_set(out_dir: Path, people: list[tuple[str, str, list[str]]]) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    problems: list[str] = []

    for slug, display_name, folders in people:
        candidates = find_candidates(display_name, folders)
        if not candidates:
            problems.append(f"{display_name}: no candidate photos found for {out_dir.name}")
            continue

        preferred = pick_preferred_candidate(display_name, folders, candidates)
        if preferred is None:
            problems.append(f"{display_name}: no readable photos across {len(candidates)} candidates for {out_dir.name}")
            continue

        chosen_path, face, img, used_fallback = preferred
        if used_fallback or face is None:
            problems.append(
                f"{display_name}: no face detected in preferred year folder, used centered fallback ({chosen_path.parent.name}/{chosen_path.name}) for {out_dir.name}"
            )
            h, w = img.shape[:2]
            side = min(h, w)
            x0 = (w - side) // 2
            y0 = max(0, (h - side) // 3)
            y1 = min(h, y0 + side)
            x1 = x0 + side
            cropped = img[y0:y1, x0:x1]
        else:
            cropped = crop_portrait(img, face)

        # cv2 -> PIL for clean resize + JPEG save
        cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(cropped_rgb)
        pil = pil.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.LANCZOS)

        out_path = out_dir / f"{slug}.jpg"
        pil.save(out_path, format="JPEG", quality=88, optimize=True, progressive=True)
        print(f"[ok] {display_name:18s} <- {chosen_path.name}  -> {out_path.relative_to(ROOT)}")

    return problems


def main() -> int:
    all_problems: list[str] = []
    all_problems.extend(run_set(ROOT / "public" / "birthdays", BIRTHDAY_PEOPLE))
    all_problems.extend(run_set(ROOT / "public" / "certifications", CERTIFICATION_PEOPLE))
    all_problems.extend(run_set(ROOT / "public" / "new-member", NEW_MEMBER_PEOPLE))
    all_problems.extend(run_set(ROOT / "public" / "team", TEAM_PEOPLE))

    if all_problems:
        print("\nIssues:")
        for p in all_problems:
            print(f" - {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
