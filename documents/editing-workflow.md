# Editing workflow (Code Coffee deck)

End-to-end order: **prepare what the slides will show** (files on disk), **then** wire it up in **`slides.md`**. Commands and script flags live in [README.md](../README.md) and the linked `.md` notes.

## 1. Prepare assets (before changing `slides.md`)

You need anything that must **appear on slides** — birthdays, certifications, team photos, event images, logos, etc. — to exist where the deck can load them.

| Step | What to do |
|------|------------|
| **Collect** | Source images and collateral (company drives, `assets/individual_photos/`, exports, certification badges, …). |
| **Process or copy** | Run [scripts/](../scripts/) when the house pipeline applies (e.g. face crop → squares under `public/birthdays/`, `public/team/` — see [birthday-photo-workflow.md](birthday-photo-workflow.md)), **or** compress with `npm run optimize:public` ([python-scripts.md](python-scripts.md)), **or** simply **copy** finished files into the right folder under **`public/`**. |
| **Verify paths** | Slides only resolve URLs that map to real files under **`public/`** (paths in YAML start with `/`). Prep folders under **`assets/`** are not automatically visible to slide props until you export or copy into `public/` (except layouts that **import** small bundles from `assets/` — see [repository-layout.md](repository-layout.md)). |

Do **not** skip this and ask an AI to “fix” missing images only in Markdown — if the file is not in `public/`, the slide will still break in the browser.

## 2. Edit `slides.md` (structure and copy)

After assets exist:

1. Set the deck **root frontmatter** (`date:`, `info:`, cover fields).
2. For each slide: choose **`layout:`** and fill the props that layout expects — mirror working examples in `slides.md` and [README.md — Layouts](../README.md#layouts-frontmatter-layout). Remember: **`title:`** is the browser/meta title; on-slide titles use **`heading:`** or the layout’s props ([README](../README.md#editing-a-monthly-deck)).
3. Reference images with **leading-`/` paths** that match **`public/`** (e.g. `avatar: /birthdays/alice.jpg` → `public/birthdays/alice.jpg`).

### Using AI on `slides.md`

- **Ground the model in facts** — Paste or attach the real names, dates, exam titles, image paths, and bullet copy **you** have verified (HR, calendar, asset filenames). Ask the AI to apply *that* list to the deck, not to invent details.
- **Prompt in one place** — Prefer: “Given this verified table / list of paths, update only `slides.md` to …” and exclude `layouts/` unless you intentionally extend the template.
- **Expect variance** — Output quality depends on the **model** and **prompt**. AI edits save time versus typing everything from scratch, but **layout names, YAML indentation, and paths are easy to get wrong** — treat the first result as a draft.
- **Human review is mandatory** — Open the deck in **`npm run dev`**, spot-check each slide, compare names and dates to your source, fix YAML typos, then export or ship.

If no existing **`layout:`** matches what you need (new props or structure), **add or extend a layout** under **`layouts/*.vue`** (and styles if needed), then reference it from `slides.md`. Prefer copying an existing layout as a starting point rather than prompting AI to redesign the whole design system.

## 3. Preview and ship

| Who | Action |
|-----|--------|
| Someone with Node | **`npm run dev`** — hot reload; default URL in [README — Quick start](../README.md#quick-start). |
| When distributing | **`npm run export`** (PDF), **`npm run build`** (`dist/`). Optional PDF cleanup: [pdf-export-shrinking.md](pdf-export-shrinking.md). |

**Page numbers:** If you use `pageNumber` in frontmatter, it is manual ([README](../README.md#editing-a-monthly-deck)).

## Optional branches (same as before)

| Goal | Document |
|------|----------|
| Portrait pipeline into `public/` | [birthday-photo-workflow.md](birthday-photo-workflow.md) |
| Shrink rasters in `public/` | [python-scripts.md](python-scripts.md) |
| Smaller PDF after export | [pdf-export-shrinking.md](pdf-export-shrinking.md) |

**Repo layout (prep vs serve):** [repository-layout.md](repository-layout.md).

## Copy-paste prompts (AI assistants)

Use after assets exist on disk and you have a **fact list** (names, dates, exact `/…` paths). Attach or @ **`slides.md`**.

1. **Monthly refresh (facts attached):** “Here is the verified deck info: [paste date, title, no invented names]. Update only **`slides.md`** root frontmatter and slides that differ this month. Do not modify `layouts/`, `styles/`, or `package.json`. Use only these image paths (they already exist under `public/`): …”

2. **Single slide with constraints:** “In **`slides.md`**, update only the slide with `layout: certification` for **[Name]** to use exam **[Exam]** and path **`/certifications/[file].jpg`**. Keep all other slides unchanged.”

3. **New slide from a template block:** “Duplicate the **`event`** slide `---` block in **`slides.md`**. Set `heading:` (not browser `title:`), `image:` to **`/events/…`** (file exists at `public/events/…`). Fill bullets from this list: … Do not reorder unrelated slides.”
