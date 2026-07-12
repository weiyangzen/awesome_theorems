# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `复乘理论`, attributes it only to
"many mathematicians", dates it to the nineteenth century, and gives the gloss `虚二次域的类域论`
("class field theory of imaginary quadratic fields"). Stage0 repeats that gloss while leaving exact
definitions, assumptions, proof history, axioms, machine status, and artifacts open. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted`.

This is subject metadata, not a theorem statement: it supplies no quantified objects, selected
order or field, modular function, hypotheses, conclusion, edition, theorem number, page, proof
boundary, or errata record. The neighboring entries for Shimura reciprocity and Kronecker's
Jugendtraum underscore the need to avoid absorbing those distinct targets; adjacency supplies no
statement evidence.

## Candidate source work

Classical texts organize complex multiplication into multiple "main theorems" and variants. The
source audit must choose and independently inspect an authoritative edition, then record its exact
definition/theorem/page, assumptions, notation translation, proof boundary, and errata. No such
passage is accepted at intake. Consequently this dossier does not choose a first-main-theorem,
second-main-theorem, or ring-class-field formulation and makes no `H0` claim.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "imaginary quadratic field" | a quadratic number field with no real embedding | number field, quadratic extension, embeddings | nearby pinned APIs probed; exact domain open |
| "complex multiplication" | endomorphism order of a complex torus or elliptic curve | elliptic curve/lattice and endomorphism-ring encoding | absent as a selected source claim |
| "class field" | Hilbert class field or ring class field of an order | abelian extension, ramification, Artin map, class group | exact field and API open |
| "theory" | generation, algebraicity, reciprocity, or classification theorem | one concrete `Prop` with all binders and hypotheses | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports the CM-number-field, class-number, and elliptic-curve modules. It checks
`NumberField.IsCMField`, `NumberField.maximalRealSubfield`, `NumberField.classNumber`,
`ClassGroup`, and `WeierstrassCurve`. These demonstrate nearby vocabulary only. A bounded textual
search found no class-field, Hilbert-class-field, ring-class-field, Artin-map, or classical complex-
multiplication main-theorem declaration in pinned mathlib. That negative name search is not the
later immutable anchor audit and receives no proof credit.
