# Intake validation

Base revision: `75ab5edd624df749325d391b41b669f8d72774b2` (tree
`26562e2b8168d91a92a8164c9d8f0fc55178836e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers manifest membership, the planned dossier and source/non-substitution
boundaries, the open task DAG, scoped intake invariants, and a narrow pinned Lean API probe. It
does not validate a canonical Schur proposition or proof because neither is frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no update,
build, clone, fetch, or other `.lake` mutation was performed. The dirty worker run is nonrelease
evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0066` | exit 0; rank 1097, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 491,496 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded `rg` and source inspection for Schur, irreducible-representation, simple-module, and simple-object declarations | exit 0; the three pinned formal leads recorded in the dossier were located; no source-to-canonical-target transport was assumed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0066/IntakeProbe.lean)` | exit 0; eight relevant APIs elaborated, and all three inspected Schur candidates reported only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, and `intake-receipt.json` | exit 0 for each |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0066-pycache python3 -m py_compile Stage1_Instances/THM-M-0066/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0066/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, H1/M3/R4 planned boundary, null target, source and pin hashes, receipt packet, exact owned inventory, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped `git diff --no-index --check /dev/null <new-file>` loop, followed by `git diff --check -- Stage1_Instances/THM-M-0066 .stage1-worker-selftest.json` | exit 0; every new owned file and the worker packet passed the explicit whitespace check, with no tracked-diff diagnostics |

## Known open gates

An accepted source edition and exact theorem passage, complete definition/assumption/errata
crosswalk, independent source review, acting-object and scalar domains, dimensionality,
representation and irreducibility conventions, intertwiner and isomorphism encodings, binder
order, boundary cases, and checked alternate transports remain open. So do canonical target
elaboration and mutations, exhaustive anchor/provenance/trust audits, discovery and obligation
freezes, typed graphs, proof and composition, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
