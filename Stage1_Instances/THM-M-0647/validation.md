# Intake validation

Base revision: `f53f980e1606a9b2eb406153ede39662661a45c2`.

Validation date: 2026-07-12 (Asia/Shanghai). The worker clone already had an untracked
`Formalizations/Lean/.lake` link/artifact at preflight. It was used read-only; no `lake update`,
`lake build`, dependency clone, or fetch was run. This is scoped, nonrelease intake evidence.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0647` | exit 0; rank 693, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | exit 0; Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| repository and pinned-mathlib `rg` searches for the theorem name, elementary equivalence, elementary substructures, and cardinal model declarations | exit 0; repository source reduced to secondary metadata; pinned candidate located in `Mathlib.ModelTheory.Satisfiability` |
| `python3 -m json.tool Stage1_Instances/THM-M-0647/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0647/task-dag.json` | exit 0 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0647/IntakeProbe.lean` | exit 0; candidate elaborated and printed with quantified `L`, infinite `M`, `kappa`, `aleph_0` and language-cardinality bounds, and an elementarily equivalent `N` with `#N = kappa` |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0647 .stage1-worker-selftest.json` | exit 0; no output |

The Lean probe establishes candidate availability only. It is not the statement gate: the
repository metadata does not identify an exact primary theorem, and no canonical wrapper,
expression hash, checked source transport, or structural mutation suite has been created.

Known downstream failures are the primary-source edition/theorem/page/errata review, exact choice
between all-cardinals and merely different-cardinality formulations, canonical statement and
mutation gate, anchor/provenance audit, frozen obligation graphs, proof integration, hermetic replay,
readable reconstruction, and independent review. These failures prevent theorem completion but do
not invalidate this fail-closed planned intake.
