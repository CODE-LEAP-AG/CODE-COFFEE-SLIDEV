# Code Coffee — Slidev deck

Monthly **Code Coffee** all-hands deck for **CODE LEAP AG**, built with [Slidev](https://sli.dev). One Markdown file (`slides.md`) drives the presentation; custom Vue **layouts** and shared **styles** match the house template (yellow accent, typography, footers). How the folders fit together and how to edit the deck (including using AI): [documents/](documents/).

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| **Node.js** 18+ | 20 LTS is fine. Check with `node -v`. |
| **npm** 9+ | Bundled with Node; check with `npm -v`. |
| **Python** 3.10+ | Needed for optional helper scripts and for `npm run optimize:public`. Check with `python3 --version`. |

You only need Python if you will run scripts under [`scripts/`](scripts/) or `npm run optimize:public`. Slidev itself is Node-only.

## Quick start

```bash
git clone <repository-url> CODE-COFFEE-Slidev
cd CODE-COFFEE-Slidev
npm install
npm run dev
```

- The dev server (default: <http://localhost:3030>) opens in the browser. Editing `slides.md` or theme files **hot-reloads** the deck.
- Use the **[Slidev](https://sli.dev)** UI for presenter mode, dark mode, recording, and export.

## Python environment (optional)

Create **`.venv-face`** at the repo root (this name matches [`package.json`](package.json) `optimize:public`, which calls `.venv-face/bin/python3`). Install dependencies used by the scripts below:

```bash
cd CODE-COFFEE-Slidev
python3 -m venv .venv-face
source .venv-face/bin/activate   # Windows: .venv-face\Scripts\activate
python3 -m pip install --upgrade pip
python3 -m pip install pymupdf opencv-python Pillow
```

**Details and per-script commands:** [documents/python-scripts.md](documents/python-scripts.md). **Orientation:** [documents/repository-layout.md](documents/repository-layout.md) (directory map), [documents/editing-workflow.md](documents/editing-workflow.md) (monthly workflow). Related: [documents/birthday-photo-workflow.md](documents/birthday-photo-workflow.md), [documents/pdf-export-shrinking.md](documents/pdf-export-shrinking.md).

## First edit

1. Open `slides.md`.
2. Adjust the **root frontmatter** (for example `date:` or `title:` / deck name).
3. Save — the browser should refresh with your change.

## Project layout

| Path | Role |
|------|------|
| `slides.md` | **Source of truth** — one `---` block per slide; frontmatter sets `layout`, copy, and props. |
| `layouts/*.vue` | Custom slide layouts (cover, section, person, event, project, etc.). |
| `styles/*.css` | Global tokens, per-layout CSS, markdown bullets. `style.css` imports them. |
| `public/` | **Served files** — static assets at the site root. Slides reference them **from `/`**: e.g. `image: /projects/foo.jpg` → `public/projects/foo.jpg`. |
| `assets/` | **Prep and bundled art** — source photos (`individual_photos/`, etc.), working files, **and** small images **imported** in Vue (e.g. `assets/cert-logos/*.png`). Slide image URLs normally target `public/` after prep or scripts. |
| `documents/*.md` | Internal notes: [repository layout](documents/repository-layout.md), [editing workflow](documents/editing-workflow.md), [Python helper scripts](documents/python-scripts.md), [portrait workflow](documents/birthday-photo-workflow.md), [PDF shrinking](documents/pdf-export-shrinking.md). |
| `scripts/` | Optional Python helpers (see [Python scripts](#python-scripts)). |

## Layouts (frontmatter `layout:`)

| Layout | Typical use |
|--------|-------------|
| `cover` | Title / date / brand |
| `section` | Chapter divider with icon |
| `birthday` | Birthday slide |
| `person` | One person, headline, role, avatar |
| `new-member` | New joiner “Come say hi” |
| `certification` | Exam pass + logo |
| `event` | Title + image + bullet body |
| `people` | Grid of people / team events |
| `project` | Project update: bullets + team grid |
| `end` | Closing slide |

## Editing a monthly deck

1. **Prepare what will display** — Gather images, certification art, etc.; run [`scripts/`](scripts/) or copy final files into **`public/...`** so slide paths resolve (see [documents/editing-workflow.md](documents/editing-workflow.md)). Optional: stage or hold source material under **`assets/`**.
2. **Duplicate or branch** from the previous month’s `slides.md` if you want history; otherwise edit in place.
3. Update the **root frontmatter** in `slides.md` (`date:`, `info:`, `title` / `name` as you prefer).
4. For each slide: set `layout`, then props the layout expects (see the matching `layouts/<name>.vue` `defineProps` and the examples already in `slides.md`). If no layout fits, add one under `layouts/` (see workflow doc).
5. **Images**  
   - Reference files under `public/...` with a **leading `/`**: e.g. `avatar: /team/jane-doe.jpg` → `public/team/jane-doe.jpg`.  
   - Raster files under `public/` are **gitignored** to keep the repository small; add them locally or pull from your team’s asset store. Re-run the deck after copying files.
6. **Page numbers** — `pageNumber` in frontmatter is set manually so reordering slides doesn’t auto-shift numbers; remove it if you rely on Slidev’s built-in slide index instead.

When using **AI** to edit `slides.md`, supply **verified** names, dates, and file paths; treat the output as a draft and **review in the browser** — see [documents/editing-workflow.md](documents/editing-workflow.md).

> **Note:** `title:` in frontmatter is reserved by Slidev for the **browser / meta title**. Use `heading:` (or each layout’s prop name) for on-slide titles.

## Export & static build

```bash
npm run export            # PDF (output path in the terminal; often a .pdf in the project root)
npm run build             # static site in dist/
npm run optimize:public   # recompress / downscale rasters under public/ (requires .venv-face; see below)
```

For export options (format, size), see the [Slidev export docs](https://sli.dev/guide/exporting).

After `npm run export`, you can run lossless PDF cleanup with **`python3 scripts/shrink_pdf.py`** (install **PyMuPDF** first — already included in the [Python environment](#python-environment-optional) `pip install` line). See [documents/pdf-export-shrinking.md](documents/pdf-export-shrinking.md).

## Python scripts

Slidev and most npm commands are **Node-only**. These pieces use **Python**:

| What | Role |
|------|------|
| **`npm run optimize:public`** | Runs `.venv-face/bin/python3 scripts/optimize_raster_images.py` to walk `public/` and recompress JPEG, PNG, and WebP (see [`package.json`](package.json)). |
| **`scripts/shrink_pdf.py`** | Post-process an exported PDF for smaller file size (PyMuPDF). |
| **`scripts/generate_public_avatars.py`** | Face crop and export square avatars under `public/` (OpenCV + Pillow). |

Full command lines and flags are in [documents/python-scripts.md](documents/python-scripts.md).

## Media and git

Large **photos and binary images** are listed in `.gitignore` (under `public/`, most of `assets/`, and `code-coffee-contents-and-elements/graphics/`). The repo is meant to track **slides, layouts, and styles**; **clone the repo, then** restore media from your internal folder or the monthly content pack. **If slide paths point at `public/…` but images still do not show**, the files are often not in git on purpose — add them locally so the paths exist on disk.

Small **certification logos** under `assets/cert-logos/*.png` stay tracked so certification slides keep working in a fresh clone.

## License

Internal template for **CODE LEAP AG**; keep usage within company policy.
