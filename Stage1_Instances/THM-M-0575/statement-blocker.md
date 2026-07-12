# Exact-statement gate: blocked

Item: `S56-M-0575-STATEMENT`  
Base revision: `be98a856ad5cbf322fb2fda71f1506bd05f1d355`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the repository record.
The complete source wording is `K-理论的周期性` ("periodicity of K-theory"), attributed to Raoul
Bott in 1959. It does not determine whether the intended root is the stable classical-group
theorem, complex topological K-theory of compact spaces, reduced K-theory of based finite CW
complexes, or another standard formulation. It also omits the category of spaces, reduced versus
unreduced convention, degree direction, Bott-class normalization, and whether naturality and
multiplicativity are part of the conclusion.

The intake correctly treats complex period-two K-theory as provisional and records its canonical
formal target as blocked. Choosing binders or a K-theory model now would invent the missing
mathematics. An abstract `K : X -> Int -> Type` parameter together with a supplied periodicity
equivalence would instead assume the theorem and would be a broadened substitute, not an encoding
of Bott periodicity. Real `KO` period eight and a sphere-only computation are likewise excluded.

The intake source crosswalk lists Bott's 1959 paper and Atiyah's 1967 monograph only as discovery
anchors. It has no accepted edition/file hash, pinpoint theorem and page, verbatim formulation,
assumption map, errata audit, or independent source review. Consequently ordered binders,
hypotheses, boundary cases, alternate-form transports, and meaningful removed-hypothesis/domain/
scope/boundary mutations cannot be frozen.

## Pinned Lean boundary

The pinned mathlib source tree was searched case-insensitively for `Bott`, `Bott periodicity`,
`topological K-theory`, `complex K-theory`, and `KTheory`; no relevant declaration or module was
found. `StatementProbe.lean` imports the nearest two independent substrates and checks
`Topology.CWComplex`, `Topology.CWComplex.Finite`, and `VectorBundle`. It elaborates, but it is only
an infrastructure probe. It does not introduce a K-theory functor, Bott element, periodicity map,
or canonical theorem, and supplies no statement or proof credit.

The environment is Lean `4.29.0`, repository base
`be98a856ad5cbf322fb2fda71f1506bd05f1d355`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, reused through the existing canonical pinned `.lake`
artifact. No dependency update, fetch, clone, or build was performed.

## Validation evidence

Commands were run from the worker clone on 2026-07-12.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0575` | exit 0; rank 621, planned, `L0`, rework required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0575/StatementProbe.lean)` | exit 0; the three substrate declarations printed with no elaboration error |
| `rg -ni 'Bott periodic|Bott element|topological K.?theory|complex K.?theory|KTheory' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; no matches |
| `rg -n "sorry|admit|sorryAx|^[[:space:]]*axiom[[:space:]]" Stage1_Instances/THM-M-0575 --glob '*.lean'` | exit 1; no forbidden proof escapes; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0575` | exit 0; no whitespace errors |

## Gate result

First failed gate: section 5 canonical mathematical-claim identity, before Lean expression
elaboration. Machine status remains `M4`; no expression fingerprint, statement credit, proof
credit, audit completion, or theorem completion is claimed. Retry requires an accountable source
reviewer to select and transcribe a pinpoint primary theorem and freeze the space category,
K-theory model, grading and suspension conventions, Bott class, naturality, and exact conclusion.

Because the assigned statement phase is not complete, no `.stage1-worker-selftest.json` is
emitted.
