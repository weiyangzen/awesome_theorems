# THM-M-0046 intake validation

Base revision: `7e54c0fcaf9c0e53fa7afbbeb0a36218152f932c` (tree
`80ece87e35401b07ba76abc36ea83440b5fa7f31`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, the
six-node open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does
not validate a canonical QR proposition or proof because neither has been frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0046` | exit 0; rank 1086, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 349,354 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the author-hosted Axler fourth-edition PDF | exit 0; Theorem 7.58 on printed page 264 located; PDF digest `45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| exact-topic `rg` search for QR decomposition/factorization in pinned mathlib and repo-local Lean | bounded search completed; no QR-named or documented terminal declaration found; Gram-Schmidt APIs were identified as ingredients only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0046/IntakeProbe.lean)` | exit 0; ten adjacent Gram-Schmidt, upper-triangular, orthonormal-basis, and unitary APIs elaborated; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target declaration |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0046-pycache python3 -m py_compile Stage1_Instances/THM-M-0046/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0046/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, planned scope, pins, exact artifact hashes, receipt, packet, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0046 --glob '*.lean'` | exit 1 as expected; no prohibited Lean construct matched |
| scoped `git diff --check` and per-new-file no-index whitespace checks | exit 0; no whitespace diagnostics |

## Known open gates

Immutable pinpoint source admission, reconciliation of `THM-M-1448`, field/shape/rank/full-reduced
factor choices, triangularity and diagonal conventions, uniqueness and boundary cases, historical
and correction audit, and independent source review remain open. So do the canonical Lean
expression and environment fingerprint, checked transports and mutations, exhaustive anchor audit,
obligation registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a truthful
self-tested `planned` intake.
