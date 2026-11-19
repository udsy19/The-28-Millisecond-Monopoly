# Handoff requests

## From Agent C (Docs)

- **Re-render after merging Agent A.** `deliverables/assumptions.md` (row A19) was rendered with temporary values `endpoint_source_max_km_max_ent = "7.5 km"` and `endpoint_source_max_km_partial = "15.1 km"`. Until A's keys land in `results/results.json`, `render_deliverables.py` fails on these keys and `check_numbers.py` reports 2 problems (the 7.5 and 15.1 in `deliverables/assumptions.md`). After merging A, run `python scripts/render_deliverables.py && python scripts/check_numbers.py`.
- **Rebuild committed PDFs** (`reports/memo.pdf`, `reports/phase1.pdf`, `reports/one_page_brief.pdf`; owned outside docs) from the new deliverables: `NODE_PATH=$(npm root -g) scripts/build_pdfs.sh`, then copy `build/*.pdf` into `reports/`. Memo is now 2 pages with about 9 lines spare on page 2; the brief is 1 page with almost no spare room.
