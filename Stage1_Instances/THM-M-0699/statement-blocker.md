# Exact-statement gate: blocked

Item: `S56-M-0699-STATEMENT`  
Theorem: `THM-M-0699`  
Worker base revision: `6d9089613f4343925b2ff1ec1a221f0575a93b5f`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is the title "Loewenheim-Skolem theorem" and the gloss
`无穷模型的基数` ("cardinality of infinite models"). It gives no immutable source passage,
proposition, language, theory or source structure, ordered binders, cardinal bounds, elementary
relation, conclusion, or boundary cases. Stage0 explicitly leaves precise definitions,
assumptions, proof, dependencies, axioms, and machine artifacts open.

The pinned API probe demonstrates that the ambiguity is substantive. Mathlib offers distinct
declarations for an arbitrarily large model, a downward elementary substructure, an upward
elementary embedding, a bidirectional elementary embedding, an elementarily equivalent structure,
and an exact-cardinality model of a theory. These differ in hypotheses such as `Infinite M`,
`Nonempty M`, `aleph_0 <= kappa`, language-cardinality bounds, source-model bounds, containment of a
distinguished set, and in their conclusions. Choosing any one would invent missing mathematics.
The separately tracked upward, downward, and combined repository targets cannot silently supply
this target's claim.

Consequently there is no canonical expression to serialize or hash, no sound alternate-form
transport, and no meaningful removed-hypothesis, changed-domain, binder-scope, or boundary mutation
test. The rev-5.6 section 5.1 gate fails at exact source-statement identity. `IntakeProbe.lean` was
re-elaborated only to prove that the pinned Lean environment and candidate APIs are available. It
is not a canonical target and receives no statement or proof credit.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (`Asia/Shanghai`). The existing canonical `.lake`
artifacts were used read-only; no update, build, dependency clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0699` | 0 | rank 740, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the ID, names, and gloss | 0 | only the underspecified title/gloss and open Stage0 fields identify this target |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0699/IntakeProbe.lean)` | 0 | all six inequivalent candidate declarations elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0699 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom |

## Required unblocker

An accountable reviewer must preserve and independently inspect an immutable source passage and
select one exact proposition, fixing its language, model or theory domain, universes, ordered
binders, cardinal inequalities, elementary relation, conclusion, and degenerate cases. Only then
can a later statement worker minimize imports, elaborate and fingerprint the exact expression,
compile checked transports, and run all four required mutation classes.

The node remains `[ ]`, blocked at `M4`; the root remains `[H3, M4, R4]` with
`audit_complete: false` and `theorem_complete: false`. The assigned deliverable did not pass, so no
`.stage1-worker-selftest.json` is emitted.
