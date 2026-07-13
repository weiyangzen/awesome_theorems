# Intake validation

Base revision: `b4e1220a37cc10a96534cfd411e3b29523d7fd81` (tree
`a67dd08a83c396119f4762e0ff109cd0df43ee60`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API/LDL probe. It does not validate
a canonical Cholesky proposition or proof because none is frozen. The automation-provided canonical
`.lake` symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or
other `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1447` | exit 0; rank 1124, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 10567,10572 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| inspected Netlib LAPACK Users' Guide section 2.3.4 | exit 0; symmetric/Hermitian positive-definite upper/lower Cholesky family located; observed HTML SHA-256 `f81af691fc5fa08f7f2e9a93943d03d3ad530c30c1f406c227208cd1a7039621`; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| bounded exact-topic `rg` search in repo-local Lean and pinned mathlib | completed; no Cholesky-named or source-identical `LLᴴ` target declaration found; adjacent `LDL.lower_conj_diag` and its explicit triangularity TODO identified; no root credit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1447/IntakeProbe.lean)` | exit 0; twelve adjacent positive-definite, Gram, and LDL APIs elaborated, and an LDL-only wrapper checked; stdout SHA-256 `a4d31abc707294d88f3595526d08177d0140011d7e5454df2ac5ceeae6919dc7`; wrapper axioms were `propext`, `Classical.choice`, and `Quot.sound`; no Cholesky target declared |
| first attempted Lean probe before correction | exit 1; transpose notation was not enabled, and Lean exposed `sorryAx` for the failed declaration; changed to explicit `L.transpose`, reran successfully, and retained no failed or placeholder declaration in the artifact |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1447-pycache python3 -m py_compile Stage1_Instances/THM-M-1447/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1447/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source and dependency pins, exact artifact hashes, provisional receipt and worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An accepted immutable source edition and exact proposition, real/complex domain, finite index order,
symmetry/Hermitian encoding, positive-definiteness mapping, lower/upper factor orientation,
transpose/conjugate-transpose convention, triangularity, positive-diagonal normalization,
existence/uniqueness decision, every boundary case, corrections audit, and independent source review
remain open. So do the canonical Lean expression and environment fingerprints, checked transports,
statement mutations, exhaustive formal anchor audit, discovery protocol, obligation registry, typed
graphs, proof and composition, trust and provenance closure, readable reconstruction, hermetic
replay, deterministic bundle, independent verification, master acceptance, audit completion, and
theorem completion. These open gates do not invalidate a truthful self-tested `planned` intake.
