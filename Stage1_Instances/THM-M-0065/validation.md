# Intake validation

Base revision: `75ab5edd624df749325d391b41b669f8d72774b2` (tree
`26562e2b8168d91a92a8164c9d8f0fc55178836e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical group Jordan-Holder proposition or proof because neither has been frozen. The
automation-provided canonical `.lake` artifact was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0065` | exit 0; rank 1096, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` existed before this intake |
| `git blame -L 484,489 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of Milne *Group Theory* v4.01 | exit 0; Definition 6.1, Theorem 6.2, proof, and Remark 6.3 on printed pages 87-89 located; observed PDF digest `826a86c9faebaa3a8f398655da515a0ee8cd922a05787fdc3a1f21a16db73633`; H1 source lead only |
| bounded inspection of Holder 1889 publisher/Crossref metadata | exit 0; DOI, volume, pages, year, and Jordan references located; observed Crossref digest `35cbb8661e80d3a3a675b017159c62528ff5a0d7eb7a918de5af07ded7735d0f`; bibliographic lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| bounded `rg` search for a subgroup Jordan-Holder instance or group-specific wrapper | search completed; no `JordanHolderLattice (Subgroup G)` or exact group wrapper found; the module TODO explicitly leaves the subgroup realization open |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0065/IntakeProbe.lean)` | exit 0; abstract lattice, series, equivalence, length, theorem, axiom report, and generic use elaborated; axioms `[propext, Classical.choice, Quot.sound]`; no group target declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0065-pycache python3 -m py_compile Stage1_Instances/THM-M-0065/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0065/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and DAG identity, null target, H1/M3/R4 boundary, source and dependency pins, exact artifact hashes, provisional receipt, worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An accepted immutable source edition, exact finite or conditional-arbitrary proposition, historical
genealogy and correction audit, independently reviewed source mapping, proof-carrying subnormal
series, quotient-factor orientation, group realization of the abstract lattice interface, and all
boundary cases remain open. So do the canonical Lean expression and environment fingerprints,
checked transports, statement mutations, exhaustive formal anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a truthful
self-tested `planned` intake.
