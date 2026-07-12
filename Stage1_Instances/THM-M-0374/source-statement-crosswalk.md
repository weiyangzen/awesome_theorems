# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `插值定理`, attributes it to "many
mathematicians," dates it only to the twentieth century, and states `各种插值定理` ("various
interpolation theorems"). Stage0 repeats this metadata and leaves exact definitions, assumptions,
proof history, equivalences, axioms, and machine artifacts open. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted`.

The same catalog separately records the Riesz-Thorin theorem as interpolation theory for operators
and the Marcinkiewicz theorem as interpolation of weak-type operators. Those entries demonstrate
that the generic phrase names a family, but do not identify which family member this target means.

## Candidate source work

Classical papers and authoritative analysis monographs are candidate locators for the competing
results, but no edition or passage is accepted during intake. The source audit must locate a stable
source that actually determines this target, record edition, theorem/page, assumptions, proof
boundary and errata, crosswalk every binder and hypothesis, and obtain independent review. Until
then, assigning a named theorem or formula would not be `H0` evidence.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "interpolation" | strong endpoint operator bounds | `MeasureTheory.Lp`, bounded linear operator, exponent relation | candidate only |
| "interpolation" | weak endpoint bounds and strong intermediate bound | distribution/weak-type predicate, sublinear operator, `Lp` conclusion | candidate only |
| "interpolation" | analytic strip boundary-to-interior estimate | complex differentiability/continuity on a strip and boundary bounds | candidate only |
| "interpolation" | real or complex interpolation of compatible spaces | an interpolation functor, parameters, equality or embedding | candidate only |
| "various" | one theorem, a package, or a survey topic | exact root proposition and scope rule | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports the `Lp` API and Hadamard three-lines module. It checks `MeasureTheory.Lp`,
`MeasureTheory.MemLp`, `ContinuousLinearMap.compLp`, and the simpler-bound three-lines declaration
`Complex.HadamardThreeLines.norm_le_interp_of_mem_verticalClosedStrip₀₁'`. This confirms useful
infrastructure and one related theorem, not the identity or closure of the catalog target. A
broader immutable candidate audit belongs to the dependent anchor-audit phase.
