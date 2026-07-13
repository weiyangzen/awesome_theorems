# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and open DAG, exact repository
wording, source and non-substitution boundaries, JSON integrity, file hygiene, and a narrow pinned
Lean exact-topic discovery probe. It does not validate a canonical nine-point-circle root or proof
because the source proposition and root packaging have not been frozen. The automation-provided
canonical `.lake` symlink was present before this work and was used read-only. No dependency update,
build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is nonrelease
evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Mathlib/Geometry/Euclidean/NinePointCircle.lean` SHA-256:
  `929704e099f22672cb05e3847592d3e9084c209ae266473c71b105dd3bc63bc1`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0196` | exit 0; rank 1225, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before editing | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 1415,1420 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| exact-topic `rg` search for nine-point circle, Euler circle, and Feuerbach circle in pinned mathlib and repo-local Lean | bounded search completed; located the exact-topic pinned `NinePointCircle` module and no repo-local `THM-M-0196` wrapper; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0196/IntakeProbe.lean)` | exit 0; the circle definition, three-family membership surface, midpoint bridge, and medial-circumsphere bridge elaborated; all three membership bodies reported only `propext`, `Classical.choice`, and `Quot.sound`; no canonical root declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0196-pycache python3 -m py_compile Stage1_Instances/THM-M-0196/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0196/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null canonical root, H1/M4/R4 boundary, pins, exact artifact inventory, receipt, worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An approved immutable human source, exact proposition, definition of all nine points, triangle and
ambient-space boundary, circle/concyclicity encoding, indexed-family or set packaging, special and
degenerate cases, complete premise/conclusion/proof-boundary/errata crosswalk, and independent
source review remain open. So do the canonical Lean expression and environment fingerprints,
minimal imports, checked transports, statement mutations, immutable anchor audit, terminal-body
provenance, transitive trust and placeholder closure, discovery and obligation freezes, typed
graphs, proof composition, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion.

The exact-topic pinned declarations make the later formal route promising, but they do not
invalidate the truthful planned-intake boundary: no canonical root or proof state is accepted by
this phase.
