# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `Daubechies小波`, attributes it to Ingrid Daubechies,
dates it to 1988, and states only `紧支集正交小波` (compactly supported orthogonal wavelet).
`Docs/Stage0_Blueprint.md` repeats that gloss while leaving definitions, assumptions, proof route,
axioms, and formal artifacts open. The manifest preserves `已验证` only in the explicitly untrusted
field `source_status_untrusted`.

## Candidate source work

Ingrid Daubechies's 1988 paper *Orthonormal Bases of Compactly Supported Wavelets* is the obvious
primary-source locator. No immutable copy, theorem number, page-level statement, definitions,
assumptions, proof boundary, or errata was independently inspected during this intake, so the title
and date receive no `H0` credit. In particular, the repository gloss does not identify which result
in that work it intends. The statement phase must pin and independently review an exact passage
rather than infer a stronger parameterized construction from the paper title.

## Crosswalk

| Repository phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "wavelet" | mother function whose dyadic dilates and integer translates form a basis | explicit `L^2` element and indexed family | function, index convention, and scalars open |
| "orthogonal" | pairwise orthogonality, possibly orthonormality | inner-product equations or `Orthonormal` | whether normalization is included is open |
| implicit "basis" | complete span of all dilates/translates | `OrthonormalBasis` or a checked dense-span equivalent | completeness wording open |
| "compactly supported" | compact support of a representative or essential support | `HasCompactSupport` or an a.e.-invariant support predicate | exact meaning and transport open |
| "Daubechies" | construction from a finite quadrature-mirror filter | filter/refinement equations and construction obligations | order and construction data absent |
| 1988 / Ingrid Daubechies | historical locator | no Lean term or proof credit | exact primary passage open |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks compact support, `L^p`, inner-product orthonormality, and Hilbert/orthonormal-basis
interfaces. A
bounded repository and pinned-mathlib content search found no occurrence of `wavelet` or
`Daubechies` in mathlib Lean sources. This is an intake observation, not the later immutable anchor
audit and not proof of global absence.

Before statement credit, every source component must map to one elaborated proposition, and every
alternate encoding needs a checked transport. Before `H0`, an independent reviewer must approve
the pinned passage, assumptions, definitions, proof boundary, and errata record.
