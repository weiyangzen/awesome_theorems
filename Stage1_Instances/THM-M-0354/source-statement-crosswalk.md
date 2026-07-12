# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `哈尔小波基`, attributes it to Alfred Haar and 1909, and
states only `L^2[0,1]的完备正交小波基` (a complete orthogonal wavelet basis of `L^2[0,1]`).
`Docs/Stage0_Blueprint.md` repeats that gloss while leaving precise definitions, assumptions, proof
route, axioms, and formal artifacts open. The manifest's `已验证` value is explicitly untrusted.

## Candidate source work

Haar's 1909 work introducing the system and a modern harmonic-analysis text with an explicit
unit-interval Haar-basis theorem are discovery leads. No exact edition, article title, theorem
number, page, wording, proof boundary, or errata was independently inspected during intake. They
therefore provide no `H0` credit. The statement phase must select an immutable passage and map its
conventions without retrofitting a convenient formalization.

## Crosswalk

| Repository phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `L^2[0,1]` | square-integrable functions modulo a.e. equality | `MeasureTheory.Lp` over a fixed unit-interval measure model | API probed; model and scalars open |
| Haar wavelets | normalized signed indicators of dyadic half intervals | an explicit valid-index family of `L^2` elements | definition, endpoints, and normalization open |
| basis | constant function plus all dyadic wavelets | `HilbertBasis`/`OrthonormalBasis` or checked equivalent | interface available; exact target open |
| orthogonal | distinct indexed elements have inner product zero | exact orthonormality proposition | normalization and index equality open |
| complete | closed linear span is the whole `L^2` space | basis surjectivity/dense span/Parseval with transport | formulation open |
| Haar / 1909 | historical locator | no Lean term or proof credit | exact primary passage open |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks the unit interval, `Lp`/`MemLp`, and Hilbert/orthonormal basis interfaces. A bounded repository
and pinned-mathlib name/content search found no theorem-specific Haar wavelet basis declaration.
This is an intake observation, not the later immutable anchor audit and not proof of global absence.

Before statement credit, every source row must map to one elaborated proposition and any alternate
encoding must have a checked transport. Before `H0`, an independent reviewer must approve the
pinned edition, passage, assumptions, definitions, proof boundary, and errata record.
