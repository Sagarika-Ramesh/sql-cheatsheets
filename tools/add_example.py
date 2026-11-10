#!/usr/bin/env python3
"""Add an example to the SQL cheat sheets with a REAL PostgreSQL result, or re-run every result.

All content lives in the `var DATA = {...};` JSON block inside index.html. This script runs the query
against tools/setup.sql (TEMP tables, fresh session each time, nothing persists), captures the real
result or error, and writes the item into DATA.

Examples
  python3 tools/add_example.py --list                       # sheets, sections, diagram keys
  python3 tools/add_example.py --sheet window --section Ranking \
      --name "CUME_DIST" --task "Cumulative share of employees at or below each salary." \
      --sql "SELECT name, salary, ROUND(CUME_DIST() OVER (ORDER BY salary)::numeric, 2) AS cume\nFROM employees;" \
      --v rank --dry-run                                    # print the result, change nothing
  ... same without --dry-run                               # writes into index.html
  python3 tools/add_example.py --refresh                     # re-run every non-static result

Options
  --sql / --sql-file     the query shown on the card (it is also what runs)
  --show / --show-file   run --sql silently, then display THIS query's result (for CREATE/ALTER)
  --v KEY                diagram key (see --list); or --io '[["input","output"], ...]' (1-3 pairs,
                         values copied from the real result) for function-style examples
  --note TEXT            optional 👉 note under the result
  --new-section          create --section at the end of the sheet if it doesn't exist
  --replace              overwrite an existing item with the same --name
Needs `psql` connected to a running Postgres (default database `postgres`; override with PGDATABASE).
"""
import argparse, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
SETUP = open(os.path.join(ROOT, "tools", "setup.sql")).read()
SEP, MAX_ROWS = "\x1f", 8
START, END = "var DATA = ", ";\nvar SHEETS = DATA.sheets;"


def load():
    s = open(INDEX, encoding="utf-8").read()
    a = s.index(START) + len(START)
    b = s.index(END, a)
    return s, a, b, json.loads(s[a:b])


def save(s, a, b, data):
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    open(INDEX, "w", encoding="utf-8").write(s[:a] + blob + s[b:])


def run(sql, show=None):
    hidden, shown = (sql, show) if show else ("", sql)
    script = "\\pset null NULL\n\\pset footer off\n\\o /dev/null\n" + SETUP + "\n" + hidden + "\n\\o\n" + shown + "\n"
    db = os.environ.get("PGDATABASE", "postgres")
    p = subprocess.run(["psql", "-X", "-q", "-d", db, "-A", "-F", SEP, "-v", "ON_ERROR_STOP=0", "-f", "-"],
                       input=script, capture_output=True, text=True, timeout=60)
    errs = [l for l in p.stderr.splitlines() if "ERROR:" in l]
    if errs:
        return {"error": errs[-1].split("ERROR:", 1)[1].strip()}
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    if not lines:
        raise SystemExit("Query returned no output. psql said:\n" + p.stderr)
    rows = [[{"t": "true", "f": "false"}.get(v, v) for v in l.split(SEP)] for l in lines[1:]]
    return {"cols": lines[0].split(SEP), "rows": rows[:MAX_ROWS], "total": len(rows)}


def vz_keys(s):
    block = s[s.index("var VZ = {"):s.index("function viz(it)")]
    return re.findall(r'\n  "?([a-z0-9]+)"?: function', block)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--sheet"); ap.add_argument("--section"); ap.add_argument("--name"); ap.add_argument("--task")
    ap.add_argument("--sql"); ap.add_argument("--sql-file"); ap.add_argument("--show"); ap.add_argument("--show-file")
    ap.add_argument("--v"); ap.add_argument("--io"); ap.add_argument("--note")
    ap.add_argument("--new-section", action="store_true"); ap.add_argument("--replace", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    s, i0, i1, data = load()

    if a.list:
        for sh in data["sheets"]:
            print(f'{sh["id"]:<11} {sh["title"]}')
            for sec in sh["sections"]:
                print(f'    {"[flip] " if sec.get("flip") else ""}{sec["title"]}  ({len(sec["items"])} items)')
        print("\ndiagram keys:", " ".join(vz_keys(s)))
        return

    if a.refresh:
        n, changed = 0, []
        for sh in data["sheets"]:
            for sec in sh["sections"]:
                if sec.get("flip"):
                    continue
                for it in sec["items"]:
                    if it.get("result", {}).get("static"):
                        continue
                    new = run(it["sql"], it.get("show"))
                    if new != it.get("result"):
                        changed.append(f'{sh["id"]} / {it["name"]}')
                    it["result"] = new
                    n += 1
        print(f"re-ran {n} queries; {len(changed)} results differ from the page")
        for c in changed:
            print("  changed:", c)
        if not a.dry_run:
            save(s, i0, i1, data)
        return

    sql = open(a.sql_file).read() if a.sql_file else (a.sql or "").replace("\\n", "\n")
    show = open(a.show_file).read() if a.show_file else (a.show.replace("\\n", "\n") if a.show else None)
    for need in ("sheet", "section", "name", "task"):
        if not getattr(a, need):
            ap.error(f"--{need} is required")
    if not sql.strip():
        ap.error("--sql or --sql-file is required")
    if a.v and a.v not in vz_keys(s):
        ap.error(f"unknown diagram key {a.v!r}; run --list")

    sheet = next((x for x in data["sheets"] if x["id"] == a.sheet), None)
    if not sheet:
        ap.error("unknown --sheet; run --list")
    sec = next((x for x in sheet["sections"] if x["title"].lower() == a.section.lower()), None)
    if not sec:
        if not a.new_section:
            ap.error("unknown --section (add --new-section to create it); run --list")
        sec = {"title": a.section, "items": []}
        sheet["sections"].append(sec)

    item = {"name": a.name, "task": a.task, "sql": sql.strip("\n")}
    if show: item["show"] = show.strip("\n")
    if a.v: item["v"] = a.v
    if a.io: item["io"] = json.loads(a.io)
    if a.note: item["note"] = a.note
    item["result"] = run(item["sql"], item.get("show"))

    print(json.dumps(item["result"], indent=1, ensure_ascii=False))
    existing = [k for k, x in enumerate(sec["items"]) if x["name"] == a.name]
    if existing and not a.replace:
        ap.error("an item with this --name already exists in that section (use --replace)")
    if a.dry_run:
        print("\n(dry run: index.html not changed)")
        return
    if existing:
        sec["items"][existing[0]] = item
    else:
        sec["items"].append(item)
    save(s, i0, i1, data)
    print(f'\nadded "{a.name}" to {sheet["id"]} / {sec["title"]}')


if __name__ == "__main__":
    main()
