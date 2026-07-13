# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1787-1792` supplies exactly the Chinese title "Bishop theorem,"
Errett Bishop, 1959, the gloss "necessary and sufficient condition for rational approximation,"
high importance, and status `已验证` ("verified"). All six uncited lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, bibliography, definitions,
hypotheses, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:6869-6894` repeats the gloss and explicitly leaves the formal system,
precise definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Inspected source candidate

Errett Bishop, *Some theorems concerning function algebras*, *Bulletin of the American
Mathematical Society* 65(2) (1959), pages 77-78, DOI
`10.1090/S0002-9904-1959-10283-4`, was inspected at Theorems 1 and 4 on printed pages 77-78.
Theorem 1 defines the minimal boundary for a uniformly closed separating algebra on a compact
metric space. Theorem 4 applies it to rational approximation on a compact plane set with no
interior and ends by saying that it gives a necessary and sufficient condition for every
continuous function on the set to be uniformly approximable by rational functions.

The source is an announcement containing theorem statements rather than the full proof of Theorem
4. It is a strong identity and H1 source candidate, not an H0 record: the precise OCR-sensitive
notation, incorporated definitions, proof-body location or dependency, corrections and errata,
and a complete independently reviewed premise-to-target mapping remain open.

## Literal crosswalk

| Repository phrase | Candidate source component | Prospective Lean component | Intake status |
|---|---|---|---|
| `毕晓普定理` | Bishop 1959, Theorem 4 is the closest located match | one source-approved declaration or checked equivalent family | candidate identity; not frozen |
| `有理逼近` | uniform limits on compact `C` of rational functions with poles off `C` | controlled-pole rational-function restrictions and uniform/topological closure | object model open |
| `充要条件` | equivalence of universal approximation, real-part approximation, `M = C`, and planar measure zero of `C \ M` | explicit iff chain or one approved iff with checked transports | canonical equivalence open |
| compact plane set | compact `C` with empty interior | `C : Set Complex`, `IsCompact C`, `interior C = empty` | binders and degenerate cases open |
| minimal boundary `M` | smallest norm-attaining boundary of the closed separating algebra | set-valued definition plus existence/minimality theorem | no exact API selected |
| `已验证` | untrusted inventory label | human proof and kernel receipts would be required | no H0 or M credit |

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`Complex`, compactness, set interior, continuous maps, separating subalgebras, and two real
Stone-Weierstrass density declarations. Stone-Weierstrass is supporting infrastructure only: it
does not define the rational functions, pole restriction, Bishop minimal boundary, or four-way
equivalence from Theorem 4. A bounded exact-topic search found no terminal declaration. No
canonical target, expression fingerprint, proof body, trust result, or machine-proof credit follows.

## Source gate

Before H0 or statement acceptance, accountable reviewers must preserve a lawful immutable source
edition; confirm target identity; transcribe the theorem and incorporated definitions without OCR
ambiguity; locate and review the proof boundary; map every hypothesis and equivalence; inspect
corrections and errata; resolve all boundary cases; and independently approve the source-to-Lean
crosswalk. Until then the canonical statement and elaborated expression remain null.
