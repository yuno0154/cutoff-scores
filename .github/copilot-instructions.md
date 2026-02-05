# Copilot instructions — 추정분할점수 (cutoff-scores)

Purpose
- Small static web app + utility scripts to calculate and export 추정분할점수 (cutoff scores).
- Deployed as a GitHub Pages site: https://yuno0154.github.io/cutoff-scores/ (see `추정분할점수 웹주소.txt`).

Quick start ✅
1. Run locally:
   - Simple: open `index.html` in a browser.
   - Recommended for AJAX/Static-Server parity: from repo root run `python -m http.server 8000` and open `http://localhost:8000`.
2. Scripts: utility scripts are plain Python 3 (no virtualenv required for the current repo). Example: `python fix_file_v3.py` — **edit the `file_path` variable** inside the script before running (it uses an absolute Windows path by default).

Key files and patterns (what to inspect first) 🔎
- `index.html` — Single-page app (UI, styles, and client-side logic). Most changes to behavior/UI happen here.
- `나이스 추정분할점수 산출(YYYY-MM-DD_XXXX).json` — Example data file used for sample runs and debugging.
- `fix_file.py`, `fix_file_v2.py`, `fix_file_v3.py` — Python utilities that edit/wrap JavaScript snippets inside HTML files. They assume UTF-8 encoding and often use absolute Windows paths.
- `나이스 추정분할점수 실습*.html` — Example pages used for manual testing.
- `추정분할점수 웹주소.txt` — Where the site is published (useful when verifying deployment).

Conventions & important observables ⚠️
- Encoding: files are UTF-8. Use `encoding='utf-8'` when reading/writing files.
- Paths: several Python scripts use Windows absolute paths. When modifying scripts, prefer relative paths or make the path configurable so CI/collaborators can run them.
- No build system: front-end code is plain HTML/CSS/JS using CDN (e.g., `xlsx.full.min.js`). No bundler or npm config is present.
- Testing: there are no automated tests. Validate changes manually by loading `index.html` (or via `http.server`) and exercising the UI (import JSON, run export to Excel, verify modals and round calculations).

When making changes (concrete examples) 🛠️
- Fix a broken JS helper added by `fix_file_v3.py`:
  1. Open `fix_file_v3.py`, set `file_path` to a local copy of the target HTML.
  2. Run `python fix_file_v3.py` and confirm the inserted functions appear in the HTML.
- Add a UI tweak to `index.html`:
  1. Edit the HTML/JS, run `python -m http.server 8000` from repo root, open `http://localhost:8000` and verify behavior (round tabs, teacher inputs, export to excel).
  2. If you change text or structure, search for references to specific function names (e.g., `calculateRoundResult`, `exportRoundResultsToExcel`) to update call sites.

Automations & deployment notes 💡
- Deployment is manual via GitHub Pages (no CI scripts detected). Confirm live changes by visiting the URL in `추정분할점수 웹주소.txt` after pushing.

What NOT to do (observed anti-patterns)
- Do not assume Windows absolute paths will work for others — make file paths relative or configurable.
- Avoid introducing a build pipeline without a clear reason; existing UX is simple and static.

If you need more context
- If behavior is unclear, open `index.html` and search for the JS function names (e.g., `calculateRoundResult`, `openResultModal`). These functions implement the core calculation and UI flows.
- Ask maintainers for the expected sample JSON inputs if a change affects data parsing/export.

If this file is missing or unclear, tell me which area you want expanded (docs for `fix_file*.py`, deploy steps, or test checklist) and I'll iterate.