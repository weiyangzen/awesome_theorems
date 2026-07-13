# THM-M-1460 intake validation

Base revision: `22a0a0cce5163426b024f44f1a7ac09fa81c64a6` (tree
`08e2b7d76500c77153cb79a6c9de86989d879cc8`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set identity, dossier structure and scope invariants, source-record
provenance, pinned environment identity, a narrow Lean statement/interface probe, bounded local
searches, proof-escape hygiene, JSON integrity, and whitespace. The catalog record is not an exact
proposition, so elaborating a purported canonical Lean target would invent missing mathematics.
`IntakeProbe.lean` checks only adjacent substrate and introduces no theorem.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This dirty worker run is nonrelease evidence.

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

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1460` | 0 | rank 1137, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match this record |
| `git blame -L 10658,10663 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over manifest, blueprint, execution DAG, skill, guidelines, catalog, Stage0, toolchain, lockfile, and inspected mathlib files | 0 | repository and pinned input hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| bounded exact-topic `rg` searches for numerical spectral, collocation, pseudospectral, and orthogonal-polynomial methods in pinned mathlib and repo-local Lean | 0 | no target-relevant named method declaration; generic spectral vocabulary and adjacent Chebyshev/Fourier/approximation APIs were separated; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1460/IntakeProbe.lean)` | 0 | nine adjacent pinned APIs elaborated; three representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; exact output SHA-256 `764e3a18c3f5304e16bb3b6f8cfe3047b368e1a1186929182449ed2d53ae20fc`; no target declaration |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1460-pycache python3 -m py_compile Stage1_Instances/THM-M-1460/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1460/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, planned H5/M3/R4 boundary, null target, pins, inventory, handoff, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1460 -g '*.lean'` | 1 | expected no-match; no prohibited proof escape in the API-only probe |
| scoped `git diff --check` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog method-family label and gloss do not select one exact truth-valued proposition or an
  approved primary source.
- The problem/operator, domain, boundary data, basis and weight, discretization, truncation,
  regularity, norm, conclusion, convergence or error rate, arithmetic model, and boundary cases
  remain open.
- Modern references listed in the crosswalk are uninspected, uncited source-family leads, not
  independently accepted complete source/proof crosswalks.
- Pinned mathlib's Chebyshev orthogonality and quadrature, Fourier `L2` expansion, and Weierstrass
  polynomial approximation are substantive interfaces, but none is a spectral numerical-method
  root theorem.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Source and formal anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle,
  independent release verification, master acceptance, audit completion, and theorem completion
  remain open.

These failures block ordinary theorem execution and completion. They do not invalidate a truthful,
self-tested `planned` intake whose deliverable is to preserve ambiguity, scope, crosswalk,
statement/interface discovery evidence, and the open DAG. Only the integration lane may accept the
provisional worker receipt.
