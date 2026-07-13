# THM-M-0244 intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978`; base tree:
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`.

This validation covers target membership, the fail-closed planned dossier, source-record provenance,
the source-statement and non-substitution boundaries, JSON and scoped invariants, an open six-node
task DAG, a narrow pinned Lean candidate probe, prohibited-construct hygiene, and whitespace. It
does not validate or select a canonical theorem statement or proof. The initial worktree contained
only the automation-provided untracked `Formalizations/Lean/.lake` symlink. The symlink and pinned
artifacts were used read-only; no Lake update, build, fetch, or dependency mutation was run.

## Source boundary

The joint 1908 Acta Mathematica paper was retrieved to `/tmp` through Zenodo record `2177451` and
inspected in the published scan at Part I, nos. 1-2, pages 381-383, and Part II, nos. 4-5, pages
385-387. The 1,210,412-byte, 26-page PDF has SHA-256
`f9eaba25b730f11a762b67e0bd8472198e08c918689ab6b9c4ad4917264989a8`. No. 4 states a centered
sector result; no. 5 gives a connected-domain-in-a-sector generalization with a different growth
premise. The catalog does not select between them. Zenodo and Crossref metadata were observed and
hashed outside the repository. This supports H1 intake discovery only: exact root selection,
formula and definition review, translation, correction and errata audit, preservation, and an
independent source review remain open.

## Commands and results

All commands ran from the repository root unless a working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0244` | 0 | rank 1254; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD` / `git rev-parse HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 1759,1764 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Zenodo API retrieval for record `2177451`, its `article.pdf` content URL, and Crossref DOI `10.1007/BF02415450`, all to `/tmp` | 0 | published scan and metadata retrieved outside the repository; no repository source or dependency changed |
| `file`, `wc -c`, `pdfinfo`, `pdftotext -layout`, page extraction, and visual inspection for the observed PDF | 0 | PDF 1.3, 26 pages, 1,210,412 bytes; printed pages 381-387 and the no. 4/no. 5 formulas inspected |
| `sha256sum /tmp/phragmen-lindelof-1908-primary.pdf /tmp/zenodo-pl.json /tmp/crossref-pl.json` | 0 | PDF `f9eaba25...9a8`; Zenodo response `a8dfd59b...9d5b`; Crossref response `2bbeb31c...1407` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...85b1d2` and `321626c8...d81` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0244/IntakeProbe.lean)` | 0 | nine pinned proof-bearing declarations elaborated; stdout SHA-256 `e4ce8508ffbb8e8952809e962d2429dbe26e430c63d4e3243fc7847dfc03e839`; empty stderr SHA-256 `e3b0c442...b855`; no canonical root selected |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0244-pycache python3 -m py_compile Stage1_Instances/THM-M-0244/check_intake.py` | 0 | scoped validator syntax-compiled outside the owned path |
| `python3 -B Stage1_Instances/THM-M-0244/check_intake.py --worker-packet .stage1-worker-selftest.json --replay-recipes` | 0 | recorded after final packet creation: target identity, source and pin hashes, planned H1/M3/R4 boundary, receipt, packet, artifact inventory, recipes, and six open tasks agree; both structured recipes replay byte-for-byte |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0244` | 1 (expected) | no prohibited Lean declaration or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0244 .stage1-worker-selftest.json`, plus per-file `git diff --no-index --check /dev/null` diagnostics | 0 gate result | no whitespace diagnostics; no-index exit 1 per untracked file is only the expected new-file difference |

## Structured replay boundary

The provisional receipt records two network-denied structured recipes. The structure recipe runs
the scoped checker without the scheduler packet and emits one exact line. The Lean recipe runs only
`lake env lean` on `IntakeProbe.lean`. Each action binds the recipe, a manifest of its direct input
files, stdout, stderr, and combined log hashes. These mutable worker records are not release-grade
content-addressed receipts. Master acceptance must replay and recapture them against the integrated
snapshot.

## Result boundary

The planned intake self-test passes with provisional vector `[H1, M3, R4]`. It establishes a real
primary-source and pinned-formal-candidate crosswalk while refusing to choose one underdetermined
root. It adds no theorem declaration or proof body and grants no H0, accepted M0, R0, accepted task
state, audit completion, theorem completion, or master acceptance. The first acceptance gate still
open is integration-lane acceptance of `S56-M-0244-INTAKE`; the first theorem gate is source-reviewed
canonical statement identity. All six dependent tasks remain open.
