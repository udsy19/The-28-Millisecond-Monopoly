# Handoff requests from Agent A (model)

Changes needed outside Agent A's allowed files:

1. **Re-render deliverables.** `deliverables/assumptions.md` (rendered) still says "c/1.468". The
   template uses `{{fibre_index}}`, which is now "c/1.47" in `results/results.json`. Run
   `scripts/render_deliverables.py` and `scripts/check_numbers.py`.
2. **Regenerate `analysis_executed.html`** from the new `analysis_executed.ipynb` (it now includes
   section E4b and the `frontier_states` table).
3. **Docs may use the new placeholders:** `{{endpoint_source_max_km_max_ent}}` (7.5 km),
   `{{endpoint_source_max_km_82}}` (5.4 km), `{{endpoint_source_max_km_partial}}` (15.1 km),
   `{{endpoint_eta_max_ent}}` (0.707), `{{endpoint_eta_82}}` (0.781), `{{endpoint_eta_partial}}` (1/2),
   `{{endpoint_mc_err}}`. The finding: the midpoint-source assumption favours the startup (8.2 / 5.7 / 17.6 km
   at the midpoint vs 7.5 / 5.4 / 15.1 km with the source at one desk).
4. **Site parity (site agent):** `values.frontier_states` in results.json lists the causal state name and
   loss/frontier region for each landmark at 7.5 µs, 1 ms, 20 ms and 100 ms. model.js should reproduce it,
   using the boundaries excluded `w < d/c`, arrives `w >= route latency`, with the default route latency
   `1.47 * d / c` (computed as `FIBRE_GROUP_INDEX * d / c`).
5. **DECISIONS.md / CHANGELOG.md:** record the group index change (1.468 to 1.47), the boundary change
   (inclusive at d/c, inclusive at route latency), and the new E4b sensitivity experiment.


## From Agent C (Docs)

- **Re-render after merging Agent A.** `deliverables/assumptions.md` (row A19) was rendered with temporary values `endpoint_source_max_km_max_ent = "7.5 km"` and `endpoint_source_max_km_partial = "15.1 km"`. Until A's keys land in `results/results.json`, `render_deliverables.py` fails on these keys and `check_numbers.py` reports 2 problems (the 7.5 and 15.1 in `deliverables/assumptions.md`). After merging A, run `python scripts/render_deliverables.py && python scripts/check_numbers.py`.
- **Rebuild committed PDFs** (`reports/memo.pdf`, `reports/phase1.pdf`, `reports/one_page_brief.pdf`; owned outside docs) from the new deliverables: `NODE_PATH=$(npm root -g) scripts/build_pdfs.sh`, then copy `build/*.pdf` into `reports/`. Memo is now 2 pages with about 9 lines spare on page 2; the brief is 1 page with almost no spare room.
