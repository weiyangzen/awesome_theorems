# Intake validation

Base revision: `2226f559136f12fde46b1bf73cdf629043b8a648` (tree
`33cb254ed06b1391379b8e7f88c5e23188957b62`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, the source-family and neighboring-
target boundaries, the source-statement crosswalk, the open task DAG, JSON/scoped invariants, and a
narrow pinned Lean API probe. It does not validate a canonical source statement or proof because
the catalog does not choose the prime-distribution function, inequalities, constants, threshold,
domain, or endpoint conventions. The automation-provided canonical `.lake` symlink was pre-existing
and used read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was
performed. This dirty worker result is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- The NUMDAM source PDF was downloaded only to a temporary, untracked path for inspection; it was
  not made a dependency. Its SHA-256 is recorded in `instance.json`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0482` | exit 0; rank 1363, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | pre-edit exit 0; only the automation-provided `Formalizations/Lean/.lake` symlink existed; base revision/tree recorded above |
| `git blame -L 3539,3544 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| inspect the target manifest, execution node, repository source, Stage0 projection, nearby targets, repo-local Lean, and pinned Chebyshev sources | exit 0; identified an unstable theorem-family gloss, isolated neighboring targets, and found adjacent upper-bound APIs without transferring statement or proof credit |
| bounded search for `切比雪夫估计`, the catalog gloss, Chebyshev functions, and prime-counting bounds in repository sources and pinned mathlib | exit 0 overall; found only the catalog occurrence, separate legacy targets, definitions, upper bounds, and transfer infrastructure; intake discovery only |
| fetch and inspect NUMDAM metadata/PDF for `JMPA_1852_1_17__366_0` in a temporary path | exit 0 after one timed-out partial transfer was resumed; confirmed title, author, 1852 publication, pages 366-390, the printed 1850 presentation note, and multiple candidate bound formulations; no exact root or H0 admission |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0482/IntakeProbe.lean)` | exit 0; eight pinned definitions, upper bounds, and transfer interfaces elaborated; representative axioms were `propext`, `Classical.choice`, and `Quot.sound`; no target theorem or proof body declared; stdout SHA-256 `10e9505f0e987def5214385adcaac25a563d08afca14a4d4f4aebe69a9d5164f` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0482-pycache python3 -m py_compile Stage1_Instances/THM-M-0482/check_intake.py` | exit 0; scoped validator compiled without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0482/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, null canonical target, H5/M4/R4 boundary, primary-source lead, artifact inventory, source hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0482/check_intake.py` | exit 0 after finalization; public replay mode passed without requiring the scheduler-only worker packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0482` | exit 1 as expected for no match; no prohibited declaration or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-0482 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null <new-file>` | exit 0 for the tracked check; every no-index command found only the expected new-file difference and no whitespace diagnostic |

## Known open gates

An immutable exact proposition, incorporated definitions, constants, threshold, assumptions,
conclusion, proof boundary, transcription/translation, correction/errata disposition, and
independent source review remain open. So do the choice and relationship of `pi`, `theta`, and
`psi`; exact versus asymptotic form; bound directions; domain, floors, logarithms, endpoints, and
finite exceptions; canonical Lean expression and environment fingerprint; checked transports and
mutations; discovery protocol; obligation registry; typed graphs; exhaustive formal anchor and
provenance audit; lower-bound formalization; proof and composition; trust closure; readable
reconstruction; hermetic replay; deterministic evidence bundle; independent verification; master
acceptance; audit completion; and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
