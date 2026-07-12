# Anchor audit

Item: `S56-M-0696-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`

## Result

The pinned mathlib tree at `8a178386ffc0f5fef0b77738bb5449d50efeea95` has no exact
object-language propositional completeness theorem. Its relevant facilities are `itauto` and
SAT/LRAT support for ambient Lean propositions, while `Mathlib.ModelTheory` concerns first-order
semantics. None exposes the frozen `Formula`, arbitrary `Set` premise consequence, or `Derives`
calculus. The audit records the pinned Lean-source-tree digest so this negative inventory is tied
to an immutable checkout rather than a moving search result.

The strongest external Lean 4 anchor found is
`FormalizedFormalLogic/Foundation@87d4dd68835a6c1eb8448b9c392d9ca51fe08d63`. In
`Foundation.Propositional.Boolean.Hilbert`, theorem
`LO.Propositional.Hilbert.Cl.provable_of_tautology` proves that Boolean tautologies are provable in
Foundation's classical Hilbert system. Its source body uses a saturated consistent tableau,
Lindenbaum extension, a canonical valuation, and a truth lemma. The commit-addressed terminal file
has SHA-256 `89b51a...2508`; the inspected archive has SHA-256 `051d93...f077`; the terminal file has
no `sorry`, `admit`, declaration-level `axiom`, or `unsafe` token.

This candidate is deliberately classified only `E2 / M3`. It is an empty-context theorem for a
different formula type and calculus, requires `DecidableEq` and `Encodable` atoms, and does not
provide the arbitrary-context and finite-use/deduction transport needed by the exact root. Its
toolchain is Lean 4.31.0 with mathlib `fabf563a...`, whereas the worker has Lean 4.29.0 and mathlib
`8a178386...`. Those artifacts are absent, and this phase did not fetch or build them. Thus there
is neither an exact checked transport nor a local kernel/axiom report.

`avigad/lamr@06907e8513fbebdcd8422925e7203ef58ca17d78` was also inspected by immutable
archive path inventory; it has no path matching propositional, Hilbert, completeness, or semantics
and supplies no candidate endpoint. A repo-local search outside this dossier likewise found no
exact proof declaration.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all rework-required |
| `python3 scripts/stage1_target.py show THM-M-0696` | 0 | rank 737, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i --glob '*.lean' 'propositional.*complete\|complete.*propositional\|completeness\|tautolog\|Hilbert\|Derivation\|Semantics' .../Mathlib/Logic .../Mathlib/ModelTheory` | 0 | no exact endpoint; only ambient tactics and first-order/unrelated results |
| deterministic SHA-256 over every pinned `Mathlib/**/*.lean` content hash and mathlib-relative path | 0 | tree digest `47418ab6...676f5` |
| repo-local `rg` over Lean files excluding this target and `.lake` | 0 | no exact root proof |
| `git ls-remote https://github.com/FormalizedFormalLogic/Foundation.git HEAD` | 0 | immutable head `87d4dd68...d63` |
| `git ls-remote https://github.com/avigad/lamr.git HEAD` | 0 | immutable head `06907e85...d78` |
| commit-addressed Foundation raw/archive inspection with `curl`, `tar`, `rg`, and `sha256sum` | 0 | endpoint, proof body, pins, license, hashes, and token scan recorded |
| `lake env lean ../../Stage1_Instances/THM-M-0696/Statement.lean` | 0 | frozen canonical statement re-elaborated in the pinned environment |
| `python3 ../../Stage1_Instances/THM-M-0696/check_anchor_audit.py` | 0 | structured audit invariants, local pins, source-tree digest, and negative exact-candidate scan passed |
| `git diff --check -- Stage1_Instances/THM-M-0696 .stage1-worker-selftest.json` | 0 | whitespace check passed |

## Status boundary

This phase freezes a revision-addressed candidate inventory and actionable mismatch/integration
blockers. It does not import an external proof, prove the canonical theorem, establish trust or
composition closure, or claim theorem completion. The root remains `M3`; the next proof work must
construct the local completeness argument or provide checked syntax, calculus, context, and
unrestricted-atom transports from a compatible immutable body.
