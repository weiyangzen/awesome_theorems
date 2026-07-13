# Intake validation

Base revision: `d257e1e5e5fa003d6e1f26344c0331bf99374fa9` (tree
`fa06b50b528e038d182d5479a18296f63fa5eae5`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Heine-Borel statement
or proof because source-exact `R^n`, dimension, boundedness, binder, and boundary choices remain
open. The automation-provided canonical `.lake` symlink was pre-existing and used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
Dirty worker evidence is nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status remained clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

Commands ran from the repository root unless the command itself changes directory.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0618` | exit 0; rank 1312, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 4587,4592 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty package status |
| bounded exact-topic `rg` in pinned mathlib and repo-local Lean | exit 0; pinned mathlib explicitly documents the direct proper-space Heine-Borel equivalence and related one-way declarations; no source-approved `R^n` specialization or repo-local target artifact was inferred |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0618/IntakeProbe.lean)` | exit 0; seven direct or supporting interfaces elaborated; the direct equivalence and finite-dimensional properness declarations each reported `[propext, Classical.choice, Quot.sound]`; exact output SHA-256 `595dfde3b964b3bac43408cface3faeef50a1e3b0d11237a860e0e3257b5264f` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0618-pycache python3 -m py_compile Stage1_Instances/THM-M-0618/check_intake.py` | exit 0; checker compiled without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0618/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authorities, source and dependency pins, H1/M3/R4 planned state, null target, artifact hashes, receipt/packet, Lean probe, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0618/check_intake.py` | exit 0; public replay mode passed without the scheduler-only packet |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| scoped new-file whitespace checks and `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An immutable primary or authoritative source, exact theorem/page, incorporated definitions,
dimension convention, ordered proposition, assumption and proof crosswalk, attribution and date
review, translation, corrections or errata, and independent review remain open. So do the canonical
Lean expression and environment fingerprints, checked Euclidean specialization and alternate
boundedness encodings, statement mutations, exhaustive anchor and provenance audit, discovery and
obligation freezes, typed graphs, proof and composition, accepted trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a truthful
self-tested `planned` intake.
