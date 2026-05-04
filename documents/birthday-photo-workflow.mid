# Portrait Workflow (Birthday + Certification + Project Teams)

This note explains how portraits are prepared and connected to birthday, certification, new-member, and project slides.

## What was done

- Added dedicated layouts: `layouts/birthday.vue`, `layouts/certification.vue`, `layouts/new-member.vue`, `layouts/project.vue`
- Added styling: `styles/birthday.css`, `styles/certification.css`, `styles/project.css`, ...
- Added blurred fireworks background: `/fireworkbirthday.png`
- Created cropped portraits in:
  - `public/birthdays/`
  - `public/certifications/`
  - `public/new-member/`
  - `public/team/` (project team grid avatars)
- Wired birthday slides (page 3 to 9) to use `layout: birthday` with `avatar: /birthdays/<name>.jpg`
- Wired certification slides (page 12 to 14) to use `layout: certification` with `avatar: /certifications/<name>.jpg`
- Wired project slides (Project Updates section) to use `layout: project` with `team[*].avatar: /team/<name>.jpg`

## Source photos

Input folders:

- `assets/individual_photos/Individual Photos 2026/`
- `assets/individual_photos/Individual Photos 2025/`
- `assets/individual_photos/Individual Photos 2024/`

The crop script scans candidates by matching the person name prefix (for example `Daniel Tran`).

## Crop pipeline

Script:

- `scripts/generate_public_avatars.py`

Behavior:

1. Finds candidate files for each configured person.
2. Prefers the latest year folder first (2026 first, then 2025 fallback).
3. Inside that year, prefers the latest image file index (for example `... 4.jpg` before `... 1.jpg`).
4. Uses face detection on that preferred order and picks the first valid face.
5. Crops to a square portrait with headroom + shoulders.
6. Exports `800x800` JPEG avatars (configurable in the script) with quality/subsampling tuned for size to the proper output folder (`public/birthdays/`, `public/certifications/`, etc.).

Selection rule note:

- If a person has photos in 2026, the script will use 2026 and will not switch to 2025 just because the 2025 face box is larger.
- 2025 is used only when the person has no usable 2026 candidate.
- For rare bad detections, a per-person override can force a specific latest-year source image (currently used for Thao Mai).

## Re-run command

```bash
.venv-face/bin/python3 scripts/generate_public_avatars.py
```

## Birthday avatar mapping

- Daniel Tran -> `/birthdays/daniel-tran.jpg`
- Hien Vuong -> `/birthdays/hien-vuong.jpg`
- Pierrick Libert -> `/birthdays/pierrick-libert.jpg`
- Tuan Nguyen -> `/birthdays/tuan-nguyen.jpg`
- Tai Le -> `/birthdays/tai-le.jpg`
- Phu Ha -> `/birthdays/phu-ha.jpg`
- Thao Mai -> `/birthdays/thao-mai.jpg`

## Certification avatar mapping

- Tuan Nguyen -> `/certifications/tuan-nguyen.jpg`
- Quyen Nguyen -> `/certifications/quyen-nguyen.jpg`
- Manh Pham -> `/certifications/manh-pham.jpg`

## Project team avatar mapping

Generated into `public/team/` via `TEAM_PEOPLE` in `scripts/generate_public_avatars.py`.
Referenced from `slides.md` on `layout: project` entries as `team[*].avatar: /team/<slug>.jpg`.

GEDAT:

- Travis Le -> `/team/travis-le.jpg`
- Sieu Nguyen -> `/team/sieu-nguyen.jpg`
- Anh Truong -> `/team/anh-truong.jpg`
- Hien Vuong -> `/team/hien-vuong.jpg`
- Anh Tran -> `/team/anh-tran.jpg`
- Michael Nguyen -> `/team/michael-nguyen.jpg`
- Thanh Nguyen -> `/team/thanh-nguyen.jpg`
- Nathan Nguyen -> `/team/nathan-nguyen.jpg`

JTL — Cloud Platform:

- Thao Mai -> `/team/thao-mai.jpg`
- Khoi Ngo -> `/team/khoi-ngo.jpg`
- Nghia Nguyen -> `/team/nghia-nguyen.jpg`
- Dat Tran -> `/team/dat-tran.jpg`
- Ngoc Tran -> `/team/ngoc-tran.jpg`
- Hoang Dinh -> `/team/hoang-dinh.jpg`
- Quyen Nguyen -> `/team/quyen-nguyen.jpg`
- Kane Vo -> `/team/kane-vo.jpg`
- Tuan Nguyen -> `/team/tuan-nguyen.jpg`
- Phi Luong -> `/team/phi-luong.jpg`
- Clara-Marie Kückelhaus, Hong Kai Len, Markus Fleischer — client-side, no portrait (initial fallback renders)

JTL — WMS Dashboard:

- Tony Nguyen -> `/team/tony-nguyen.jpg`
- Kiet Huynh -> `/team/kiet-huynh.jpg`
- Hoang Dinh -> `/team/hoang-dinh.jpg`
- Stefan Kull -> `/team/stefan-kull.jpg` (client, photo available)

DAWN × Evolution:

- Nam Ho -> `/team/nam-ho.jpg` (from `Individual Photos 2024`)
- Avery Dao — no source photo yet (initial fallback renders)
- Trung Tran -> `/team/trung-tran.jpg`

MaiVita:

- Phuc Le — no source photo yet (initial fallback renders)
- Linh Pham -> `/team/linh-pham.jpg`
- Thach Huynh -> `/team/thach-huynh.jpg`

CODE LEAP Clockify:

- Pierrick Libert -> `/team/pierrick-libert.jpg`
- Alex Huynh -> `/team/alex-huynh.jpg`
- Trung Tran -> `/team/trung-tran.jpg`
- Thanh Hoang -> `/team/thanh-hoang.jpg`
- Viet Vo -> `/team/viet-vo.jpg`

To add a new person: drop their photo into `assets/individual_photos/Individual Photos 2026/` (or fallback years like 2025/2024) with the filename prefixed by their display name (e.g. `Jane Doe 1.jpg`), add a `("jane-doe", "Jane Doe", [...])` entry to `TEAM_PEOPLE`, then re-run the avatar script.
