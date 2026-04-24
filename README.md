# Code Coffee — Slidev deck

Weekly **Code Coffee** all-hands deck for **CODE LEAP AG**, built with [Slidev](https://sli.dev). One Markdown file (`slides.md`) drives the whole presentation; custom Vue **layouts** and shared **styles** match the house template (yellow accent, typography, footers).

## Prerequisites

- **Node.js** 18+ (20 LTS is fine)
- **npm** 9+ (comes with Node)

## Quick start

```bash
cd CODE-COFFEE-Slidev
npm install
npm run dev
```

- Dev server (default: <http://localhost:3030>) opens in the browser; editing `slides.md` or theme files **hot-reloads** the deck.
- Use the **[Slidev](https://sli.dev)** UI: present mode, dark mode, recording, and export are built in.

## Project layout

| Path | Role |
|------|------|
| `slides.md` | **Source of truth** — one `---` block per slide; frontmatter sets `layout`, copy, and props. |
| `layouts/*.vue` | Custom slide layouts (cover, section, person, event, project, etc.). |
| `styles/*.css` | Global tokens, per-layout CSS, markdown bullets. `style.css` imports them. |
| `public/` | **Static files** served at the site root. Paths in slides are **from `/`**: e.g. `image: /projects/foo.jpg` → file `public/projects/foo.jpg`. |
| `assets/` | Assets **imported** in Vue (e.g. `assets/cert-logos/*.png` for certification slides). |
| `code-coffee-contents-and-elements/content/` | Optional narrative copy / outlines (e.g. weekly summary Markdown). |
| `code-coffee-contents-and-elements/graphics/` | **Not tracked in git** (see below) — local mirror of exported graphics. |

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

## Editing a weekly deck

1. **Duplicate or branch** from the last week’s `slides.md` if you want history; otherwise edit in place.
2. Update the **root frontmatter** in `slides.md` (`date:`, `info:`, `title` / `name` as you prefer).
3. For each slide: set `layout`, then props the layout expects (see the matching `layouts/<name>.vue` `defineProps` and the examples already in `slides.md`).
4. **Images**  
   - Put files under `public/...` and reference them with a **leading `/`**: e.g. `avatar: /team/jane-doe.jpg` → `public/team/jane-doe.jpg`.  
   - Raster files under `public/` are **gitignored** to keep the repository small; add them locally or pull from your team’s asset store. Re-run the deck after copying files.
5. **Page numbers** — `pageNumber` in frontmatter is set manually so reordering slides doesn’t auto-shift numbers; remove it if you rely on Slidev’s built-in slide index instead.

> **Note:** `title:` in frontmatter is reserved by Slidev for the **browser / meta title**. Use `heading:` (or each layout’s prop name) for on-slide titles.

## Export & static build

```bash
npm run export    # PDF (output path shown in the terminal; often a .pdf in the project root)
npm run build     # static site in dist/
```

For export options (format, size), see the [Slidev export docs](https://sli.dev/guide/exporting).

## Media & git

Large **photos and binary images** are listed in `.gitignore` (under `public/`, most of `assets/`, and `code-coffee-contents-and-elements/graphics/`). The repo is meant to track **slides, layouts, and styles**; **clone the repo, then** restore media from your internal folder or the weekly content pack.

Small **certification logos** under `assets/cert-logos/*.png` stay tracked so certification slides keep working in a fresh clone.

## Troubleshooting

**`EMFILE: too many open files` (macOS, dev server)** — raise the file limit, then start Slidev:

```bash
ulimit -n 65536
npm run dev
```

**Missing images after clone** — paths must match `public/…` and filenames must exist on disk; ignored files are not in git by design.

## License

Internal template for **CODE LEAP AG**; keep usage within company policy.
