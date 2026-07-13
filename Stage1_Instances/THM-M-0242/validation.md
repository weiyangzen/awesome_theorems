# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978`; base tree:
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`.

This validation covers target membership, the planned dossier and open task DAG, source-record
provenance, JSON and scoped invariants, a narrow pinned Lean substrate probe, prohibited-construct
hygiene, and whitespace. It does not validate a canonical theorem statement or proof. The initial
worktree contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink; it
was used read-only and not modified.

## Source discovery boundary

The AMS copy of Hilbert's 1902 English publication was retrieved to `/tmp`, inspected at printed
pages 470-471, and hashed. It supports the historical problem-family crosswalk only. Crossref
metadata was also checked for Hilbert's publication and Bolibrukh's 1990 survey. No downloaded file
was added to the repository, and no primary proof, corrected theorem, counterexample, errata audit,
or H0 source review is claimed.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown. Final replay commands and
their exact results are also serialized in `intake-receipt.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0242` | 0 | rank 1252; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD` / `git rev-parse HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 1745,1750 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://www.ams.org/journals/bull/1902-08-10/S0002-9904-1902-00923-3/S0002-9904-1902-00923-3.pdf' -o /tmp/thm-m-0242-hilbert1902.pdf` | 0 | retrieved the AMS-hosted discovery copy outside the repository |
| `file`, `wc -c`, `sha256sum`, `pdfinfo`, `pdftotext`, `rg`, and `sed` over that `/tmp` copy | 0 each | 43-page, 4,596,239-byte PDF; SHA-256 `e5d069ad0d3644b2527737b67d7bf293fd2cb8acc576f1dbe8f19e12059bd2b3`; Problem 21 inspected at printed pages 470-471 |
| Crossref `curl`/`jq` queries for `10.1090/S0002-9904-1902-00923-3` and `10.1070/RM1990v045n02ABEH002350` | 0 | Hilbert publication and Bolibrukh survey metadata matched the recorded bibliography; Bolibrukh theorem text was not inspected |
| `rg -n -i 'Riemann.Hilbert\|Fuchsian\|regular singular\|monodromy' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | bounded search found covering/path-lifting monodromy declarations but no Hilbert 21 realization interface; negative result is discovery-only |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` / `HEAD^{tree}` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...85b1d2` and `321626c8...d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake 5.0.0 at the same revision |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0242/IntakeProbe.lean)` | 0 | five pinned punctured-sphere, fundamental-group, general-linear-group, and monodromy-representation substrate checks elaborated; no target theorem stated |
| `python3 -m json.tool` on the three JSON artifacts and root worker packet | 0 each | all structured records parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0242-pycache python3 -m py_compile Stage1_Instances/THM-M-0242/check_intake.py` | 0 | scoped checker compiled without writing cache into the owned path |
| `python3 Stage1_Instances/THM-M-0242/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned lifecycle, H5/M4/R4 boundary, null formal target, artifact inventory, packet, and six open tasks agreed |
| `python3 Stage1_Instances/THM-M-0242/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited-construct `rg` scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| no-index whitespace checks for every new file; `git diff --check -- Stage1_Instances/THM-M-0242 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0242-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact corrected source selection and independent
review, canonical Lean elaboration and mutation tests, anchor audit, discovery and obligation
freezes, typed graphs, proof, composition, trust closure, hermetic replay, deterministic release
bundle, and independent verification remain open. They prevent theorem completion but do not
invalidate the planned intake.
