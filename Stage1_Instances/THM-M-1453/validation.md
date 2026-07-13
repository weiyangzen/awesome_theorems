# THM-M-1453 intake validation

Base revision: `03bed3c211cb739ccd2629908210fda0f9adf6ca` (tree
`a48670276bfe2105ddbfb4057314b21056dae0cb`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical Arnoldi proposition or proof because no source-selected root exists. The automation-
provided canonical `.lake` symlink was pre-existing and used read-only; no dependency update,
build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is nonrelease
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
| `python3 scripts/stage1_target.py show THM-M-1453` | exit 0; rank 1130, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10609,10614 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the Netlib Arnoldi Method and Basic Algorithm pages | exit 0; observed HTML digests `ef995d676bc6e07a06a3684b0936dae53f9aa41ebff47ab13f4cf323d82fddbe` and `f075d2f07bb23d136f9f047add18ccb25fc6f0115cc3b395eebb401ed4cc95e1`; orthonormal-basis, Arnoldi-relation, breakdown, and approximation claims are distinct; source-family lead only |
| Crossref lookup for DOI `10.1090/qam/42792` | exit 0; bibliographic metadata for Arnoldi 1951 located with observed response digest `a50b805e8ea81602545f593c4e16bbaa34242f869c5c87474f3871352a0ba78b`; primary article body not inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | completed; no Arnoldi-, upper-Hessenberg-, or matrix-Krylov-subspace-named terminal theorem found; unrelated PDE Krylov records excluded; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1453/IntakeProbe.lean)` | exit 0; nine adjacent Gram-Schmidt, span, orthonormality, matrix-action, composition, and power APIs elaborated; stdout SHA-256 `ddd27121197695cbd7b60f231dced63bb802e1f38d76bcec0b444dadeb4632f2`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1453-pycache python3 -m py_compile Stage1_Instances/THM-M-1453/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1453/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, exact inventory, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1453 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the API-only probe |
| scoped new-file no-index whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

The method label must be redirected to an independently reviewed, immutable, exact proposition.
The scalar field, matrix/endomorphism representation, dimension, start vector, iteration count,
Krylov definition, orthogonalization and breakdown policies, Hessenberg relation, Ritz/exactness or
convergence conclusion, arithmetic model, ordered binders, neighbor boundaries, and degenerate cases
remain open. So do the canonical Lean expression and environment fingerprint, checked transports,
statement mutations, exhaustive formal anchor audit, discovery protocol, obligation registry,
typed graphs, proof and composition, trust/provenance closure, readable reconstruction, hermetic
replay, deterministic bundle, independent verification, master acceptance, audit completion, and
theorem completion. These open gates do not invalidate a truthful self-tested `planned` intake.
