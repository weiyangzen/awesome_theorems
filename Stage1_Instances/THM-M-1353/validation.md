# Intake validation

Base revision: `122f443c54e4e81d1bf325b07e18ba095823da6d`; base tree:
`2629bb0cacebd896715a9abad7c52ad60e7bccd0`.

This validation covers manifest membership, the fail-closed dossier and open DAG, source-family
crosswalk, JSON and scoped invariants, and a narrow pinned Lean API probe. Because the catalog does
not select an exact proposition, no canonical expression, statement mutation result, source H0,
formal anchor, or proof is claimed. The automation-provided canonical `.lake` symlink was used
read-only; no update, build, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1353` | 0 | rank 963, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD HEAD^{tree}` | 0 | recorded base revision and tree above |
| `git blame -L 9866,9871 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa...` |
| Numdam landing-page inspection and Crossref DOI query | 0 | Floquet primary-paper title, author, journal, 1883, volume 12, pages 47-88, and DOI identified; no theorem text credited |
| Encyclopedia of Mathematics stable revision `46944` raw inspection | 0 | distinguished factorization, reduction, spectral branches, and complex `T` versus real `2T`; raw response SHA-256 `f3b82c3b...` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib `8a178386...`, tree `bdc39a31...` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1353/IntakeProbe.lean)` | 0 | six adjacent APIs elaborated; complete output SHA-256 `7318d5f8...` |
| bounded `rg` for Floquet and periodic-linear-ODE fundamental-matrix names in pinned mathlib and repo-local Lean | 1 (expected) | no target-specific declaration found; discovery only, not a complete anchor audit |
| `python3 -m json.tool` on the three owned JSON artifacts and root packet | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1353-pycache python3 -m py_compile Stage1_Instances/THM-M-1353/check_intake.py` | 0 | scoped checker compiles without generated owned files |
| `python3 -B Stage1_Instances/THM-M-1353/check_intake.py` | 0 | durable public recipe: closed top-level schemas, planned H1/M4/R4 boundary, target identity, artifacts, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1353/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | scheduler handoff additionally agrees with the public dossier and provisional receipt |
| prohibited-construct scan over owned Lean | 1 (expected) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` and `git diff --check` | 0 aggregate | no whitespace diagnostics |

The exact primary proposition and independent source review, canonical Lean elaboration and four
mutation classes, discovery and obligation freezes, anchor audit, proof, composition, trust and
provenance closure, readable reconstruction, hermetic replay, deterministic release bundle, and
independent verification remain open. These failures block audit and theorem completion, but they
do not invalidate a truthful self-tested `planned` intake.
