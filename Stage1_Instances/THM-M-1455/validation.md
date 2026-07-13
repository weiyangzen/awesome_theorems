# THM-M-1455 intake validation

Base revision: `22a0a0cce5163426b024f44f1a7ac09fa81c64a6` (tree
`08e2b7d76500c77153cb79a6c9de86989d879cc8`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, the
six-node open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does
not validate a canonical conjugate-gradient proposition or proof because neither has been selected.
The automation-provided canonical `.lake` symlink was pre-existing and used read-only; no
dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker
run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux `7.0.0-27-generic` x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1455` | exit 0; rank 1132, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 10623,10628 -- Docs/researches/math_theorems.md` | exit 0; all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| official NIST PDF GET plus `sha256sum`, `pdfinfo`, `pdftotext`, and bounded inspection | exit 0; 1952 Research Paper 2379 and distinct Sections 3, 5, and 6 results inspected; PDF digest `0b5d9955...5262`; source-family lead only, no selected root or H0 |
| independent second official NIST PDF GET and `cmp` | exit 0; second digest also `0b5d9955...5262` and bytes agreed with the first observation |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` searches in pinned mathlib and repo-local Lean | no conjugate-gradient declaration found; this is intake discovery only, not an exhaustive external anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1455/IntakeProbe.lean)` | exit 0; ten adjacent positive-definite and matrix-vector APIs elaborated; representative axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`; output SHA-256 `a7c1a1f4...046e`; no target declaration |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1455-pycache python3 -m py_compile Stage1_Instances/THM-M-1455/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1455/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, H5/M4/R4 boundary, pins, artifacts, receipt, packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

The catalog names a method family rather than one proposition. An accepted immutable source
proposition, complete incorporated definitions and premise/conclusion crosswalk, correction audit,
independent review, recurrence and early-stop convention, and exact-arithmetic boundary remain
open. So do the canonical Lean expression and environment fingerprint, checked transports and
mutations, exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs,
proof and composition, trust and provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
