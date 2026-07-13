# Intake validation

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and open DAG, exact repository
wording, source and non-substitution boundaries, JSON integrity, file hygiene, and a narrow pinned
Lean exact-topic discovery probe. It does not validate a canonical Ptolemy root or proof because
the source proposition and cyclic-quadrilateral encoding have not been frozen. The
automation-provided canonical `.lake` symlink was present before this work and was used read-only.
No dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty
worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Mathlib/Geometry/Euclidean/Sphere/Ptolemy.lean` SHA-256:
  `d13991b9cfa5aed210efd9dfa59ee78d50d7a73c6e7dcb74ea09b33b3785b547`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0201` | exit 0; rank 1533, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before editing | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 1450,1455 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` search for Ptolemy, cyclic quadrilateral, and the distance-product identity in pinned mathlib and repo-local Lean | completed; located the exact-topic equality module and a distinct inequality theorem; no repo-local `THM-M-0201` wrapper; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0201/IntakeProbe.lean)` | exit 0; `Cospherical`, `Concyclic`, the exact-topic equality interface, and the non-substitute inequality elaborated; both theorem bodies reported only `propext`, `Classical.choice`, and `Quot.sound`; no canonical root declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0201-pycache python3 -m py_compile Stage1_Instances/THM-M-0201/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0201/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null canonical root, H1/M3/R4 boundary, pins, exact artifact inventory, receipt, worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An approved immutable human source, exact ordered quadrilateral, circle and planarity definition,
convexity or diagonal-intersection encoding, vertex-distinctness policy, segment-length convention,
degenerate cases, complete premise/conclusion/proof-boundary/errata crosswalk, and independent source
review remain open. So do the canonical Lean expression and environment fingerprints, minimal
imports, checked transports, statement mutations, immutable anchor audit, terminal-body provenance,
transitive trust and placeholder closure, discovery and obligation freezes, typed graphs, proof
composition, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion.

The exact-topic pinned declaration makes the later formal route promising, but it does not change
the truthful planned-intake boundary: no canonical root or proof state is accepted by this phase.
