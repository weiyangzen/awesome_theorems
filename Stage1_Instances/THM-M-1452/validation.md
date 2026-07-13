# THM-M-1452 intake validation

Base revision: `03bed3c211cb739ccd2629908210fda0f9adf6ca` (tree
`a48670276bfe2105ddbfb4057314b21056dae0cb`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, the source-statement and non-substitution boundaries,
the six-node open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It
does not validate a canonical Lanczos proposition or proof because neither has been selected. The
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
| `python3 scripts/stage1_target.py show THM-M-1452` | exit 0; rank 1129, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 10602,10607 -- Docs/researches/math_theorems.md` | exit 0; all six uncited target lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| official NIST PDF GET plus `sha256sum`, `pdfinfo`, `pdftotext`, and bounded inspection | exit 0; 1950 Research Paper 2133, sections VII and XIV inspected; PDF digest `ca3f1012...fc4b`; source lead only, no selected theorem or H0 |
| independent second official NIST PDF GET and `cmp` | exit 0; second digest also `ca3f1012...fc4b` and bytes agreed with the first observation |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded `rg` search for Lanczos, Krylov-subspace, and tridiagonalization terms in pinned mathlib and repo-local Lean | exit 1 expected no-match; no target-relevant named declaration found; intake discovery only, not an exhaustive audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1452/IntakeProbe.lean)` | exit 0; eleven adjacent Hermitian spectral and Gram-Schmidt APIs elaborated; representative axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`; output SHA-256 `3a3c3ebe...251`; no target declaration |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1452-pycache python3 -m py_compile Stage1_Instances/THM-M-1452/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1452/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, H5/M4/R4 planned scope, pins, receipt, packet, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1452 --glob '*.lean'` | exit 1 expected no-match; no prohibited Lean construct matched |
| scoped `git diff --check` and per-new-file no-index whitespace checks | exit 0; no whitespace diagnostics |

## Known open gates

The catalog names a method and computational topic but not one proposition. An immutable source
proposition, source corrections and independent review, matrix domain and symmetry, sparsity
semantics, start vector, recurrence, iteration count, breakdown behavior, exact output, arithmetic
model, ordered binders, hypotheses, conclusion, and boundary cases remain open. So do the canonical
Lean expression and environment fingerprint, checked transports and mutations, exhaustive anchor
audit, obligation registry, typed graphs, proof and composition, trust and provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a truthful
self-tested `planned` intake.
