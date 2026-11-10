# SQL Cheat Sheets — how to add examples

Live site: https://sagarika-ramesh.github.io/sql-cheatsheets/
Repo: https://github.com/Sagarika-Ramesh/sql-cheatsheets (GitHub Pages, `main` branch, root folder)

This is a **separate site** from SQL Gotchas and from the ML Interview Prep site, with its own look.
Don't mix their styles. When Sagarika gives new SQL cheat-sheet content (a function, a pattern, an
analysis recipe, an interview problem), **append** it here in exactly this format. Don't redesign.

## File layout

```
index.html            the whole site: CSS, the DATA block, the diagram engine, mind maps and router
tools/setup.sql       the sample dataset (online bookshop) every example runs against
tools/add_example.py  runs a query in Postgres and writes the item + its REAL result into index.html
README.md
```

## How the content is stored

All content is the JSON in `var DATA = {...};` inside `index.html`:
`sheets[] → sections[] → items[]`. Sheet ids: `basics`, `joins`, `aggregates`, `functions`,
`window`, `analysis`, `postgres`, `interview`. Mind maps, the hub cards, search, section chips and
counts are all generated from DATA, so adding an item updates everything.

- Normal item: `{name, task, sql, v | io, note?, show?, result}`
  - `name`: short label (mind-map leaves cut at 22 characters, so keep it short).
  - `task`: one plain-English sentence, phrased as the question the query answers.
  - `sql`: PostgreSQL, formatted like the existing ones (keywords upper case, aligned columns).
  - `v`: diagram key (run `python3 tools/add_example.py --list`), or `io`: 1–3
    `["input", "output"]` pairs copied from the real result (best for functions).
  - `result`: produced by the tool. `{"error": ...}` is fine for deliberate "trap" examples.
  - `show`: optional query whose result is displayed after `sql` runs silently (CREATE/ALTER).
- Flip-card sections (`"flip": true`, only in `interview`): items are `{name, desc}`.
- `result.static: true` only for things that cannot run (psql meta-commands, `now()`).

## Steps

1. `git clone https://github.com/Sagarika-Ramesh/sql-cheatsheets.git` (or `git pull`).
2. Make sure Postgres is reachable with `psql -d postgres` (Sagarika's Mac has PostgreSQL 14 via
   Homebrew). The tool only creates TEMP tables, so nothing persists.
3. Dry run first, then for real:
   ```
   python3 tools/add_example.py --sheet window --section Ranking --name "CUME_DIST" \
     --task "Cumulative share of employees at or below each salary." \
     --sql "SELECT name, salary,\n       ROUND(CUME_DIST() OVER (ORDER BY salary)::numeric, 2) AS cume\nFROM employees;" \
     --v rank --dry-run
   ```
   Check the printed result makes sense, then rerun without `--dry-run`. Use `--new-section` for a
   new section, `--replace` to update an item, and `--refresh` after changing `tools/setup.sql`.
   **Never hand-write a result.** If the query needs data that isn't in the sample, add rows or a
   table to `tools/setup.sql`, then run `--refresh --dry-run` to make sure no existing result changes.
4. If no diagram key fits, add a new function to `var VZ = {...}` in `index.html`, in the same style
   as its neighbours: 260×120 viewBox, helpers `rc` `tx` `chip` `ar` `ln` `grid` `bars` `cap`
   `ioFit`, palette `P[]` / `INK` / `CREAM` / `TAN` / `CORAL` / `TEAL`. Draw what THIS query does.
5. Check locally with `python3 -m http.server` → `/index.html#<sheet>`: the new card's diagram,
   task, query and result; the mind map leaf; and 375px phone width (no sideways page scroll).
6. Commit and push to `main`; Pages rebuilds in about a minute. Check the live URL.

## Visual rules (keep exactly)

- Single black theme: background `#0a0a0d`, cards `#131319`, text `#eeeaf4`, muted `#a7a1b4`.
  Accents: pink `#f39ac8`, violet `#b9a0ff`, blue `#8ab4ff`. Title and section headings are white.
- Fonts: **Dancing Script** (title, sheet and section headings: signature look), **Caveat** (small
  handwritten accents), **Bricolage Grotesque** (labels, tasks), **Source Serif 4** (body),
  **JetBrains Mono** (code, item names, result tables).
- Example card, top to bottom: pink mono name + "got it" checkbox → diagram on a slate panel →
  tan `TASK` badge + white task sentence → dark code block with copy button → mint "▼ RESULT n rows"
  label + table (violet header, zebra rows, NULL in grey italics) or coral "POSTGRES SAYS" error box
  → optional blue 👉 note.
- Diagrams and mind maps use the slate illustration style: panel `#47577a`, cream `#f3ecdc` objects
  with 2–3px ink `#22252e` outlines and drop shadows, tan `#c9a063` connectors with dark casing,
  coral/teal accents, dark caption chips. Mind map: dark centre oval with coral ring, bold coloured
  branch pills, cream leaf labels.
- Footer text stays exactly: "Every result was produced by running the query in PostgreSQL 14
  against the sample data. Progress is saved in this browser only." + "Sagarika" signature.
- Don't add: a link box to the gotchas site, an "original examples" note, MySQL or SQL Server
  content. Don't copy text or visuals from LearnSQL or other cheat sheets; original examples only.
