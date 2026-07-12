# Exact-statement gate: blocked

Item: `S56-M-0738-STATEMENT`  
Theorem: `THM-M-0738`  
Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the topic label `扩展Frege系统` and the gloss
`扩展Frege系统的性质` ("properties of Extended Frege systems"), with Stephen Cook and 1975 as
unverified discovery hints. The record supplies no bibliographic work, immutable edition,
theorem/page, definitions, assumptions, ordered binders, conclusion, proof, or errata disposition.

The label is compatible with materially different roots: soundness of a selected calculus,
implicational completeness, p-simulation of ordinary Frege, polynomial equivalence between
presentations, automatability, or a proof-length bound. Even within one family, the exact Frege
calculus, extension-axiom or extension-rule convention, freshness and acyclicity conditions,
sequence-versus-DAG representation, proof checker, and size measure change the proposition.
Selecting any convenient formulation would therefore broaden or substitute the theorem.

Consequently there is no canonical human claim from which to select minimal imports or derive an
exact Lean expression. There is also no expression to serialize and hash, no checked alternate
transport, and no meaningful removed-hypothesis, changed-domain, binder-scope, or boundary
mutation. Section 5.1 of the rev-5.6 blueprint fails before proof evidence may be inspected.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports finite-function/cardinality and polynomial-time
Turing-machine APIs and elaborates under the pinned environment. This establishes only that a few
possible encoding ingredients exist. A narrow pinned-mathlib search found no Extended Frege or
extension-rule proof-system declaration. Neither result identifies the missing proposition, so the
probe receives no target-statement or proof credit.

Environment used read-only:

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake `5.0.0-src+98dc76e`.
- Mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

No dependency update, build, clone, fetch, or `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0738` | 0 | rank 774, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese/English label, gloss, attribution, and year | 0 | found only underspecified metadata and this intake dossier; no exact source proposition |
| pinned-mathlib `rg` search for Extended Frege, extension axioms/rules, and proof-complexity simulation vocabulary | 1 | no theorem-specific proof-system declaration found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0738/IntakeProbe.lean` | 0 | five candidate-substrate API expressions elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0738 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0738/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0738` | 0 | no whitespace errors |

## Retry condition and status boundary

An accountable reviewer must preserve and hash an immutable primary source, select and transcribe
one exact proposition with all incorporated definitions and assumptions, audit errata, and
independently approve the mapping. A later statement run can then encode precisely that claim,
minimize imports, fingerprint the elaborated expression, check alternate transports, and run all
four required mutation classes.

The statement node remains `[ ]` and blocked at `M4`; the root remains `[H5, M4, R4]` with
`audit_complete: false` and `theorem_complete: false`. The assigned phase is not genuinely
self-tested to its completion gate, so no `.stage1-worker-selftest.json` is emitted.
