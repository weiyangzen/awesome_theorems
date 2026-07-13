# Source-statement crosswalk

## Repository record

The canonical catalogue occurrence at `Docs/researches/math_theorems.md:298-303` records:

| Field | Literal value | Intake interpretation |
|---|---|---|
| Title | `卡普兰斯基定理` | Names Kaplansky but not one uniquely identified theorem. |
| Attribution | Irving Kaplansky | Consistent with the inspected primary-paper lead. |
| Year | 1958 | Conflicts with the strongest matching paper, published in 1948. |
| Gloss | `关于PI环的结构` | Constrains the topic to polynomial-identity rings but is not a proposition. |
| Importance | `中` | Scheduling metadata only. |
| Status | `已验证` | Untrusted under rev-5.6; grants no H/M/R or proof credit. |

All six catalogue lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Stage0 projects the same record as
`THM-M-0039` and explicitly leaves precise definitions, premises, proof history, equivalent
formulations, axioms, machine status, and artifact links open.

## Inspected primary-source lead

Irving Kaplansky, *Rings with a polynomial identity*, *Bulletin of the American Mathematical
Society* 54(6), 1948, 575-580, DOI `10.1090/S0002-9904-1948-09049-8`, is an official AMS primary
source. The observed six-page PDF had SHA-256
`5291a8b885fc8ca42b39d7c0d000a569600fa07c6fb0449b1b386dffe7221f27`; an independent second GET
was byte-identical. Theorem 1 appears on journal page 577 (PDF page 3) and states:

> A primitive algebra satisfying a polynomial identity is finite-dimensional over its center.

Section 2, journal page 575, defines an algebra satisfying a polynomial identity. Section 4(c),
journal page 580, explains an extension from algebras to rings under an injectivity condition on
polynomial coefficient operators. Crossref metadata independently confirms author, title, year,
volume, issue, pages, and DOI; its observed payload SHA-256 is
`6c1f7792450a577c0b318b850d1a226e23445408c3f63916c973de4548663bd5`.

This remains `H1`, not `H0`. The source is a strong candidate, but the catalogue chronology and
scope mismatch has not been adjudicated, the exact target has not been approved, the definitions
and proof nodes have not been completely mapped, no errata/correction audit is complete, and no
independent source reviewer is assigned.

## Clause crosswalk for the candidate

| Candidate clause | Primary-source surface | Lean discovery surface | Intake status |
|---|---|---|---|
| Algebra over a field | Section 2 begins with algebra `A` over field `F` | `Field F`, `Ring A`, `Algebra F A` | Candidate domain only; exact unital convention open. |
| Polynomial identity | Nonzero `f` in the free algebra `F[x1,...,xr]`, vanishing for all substitutions | `FreeAlgebra F X`, `FreeAlgebra.lift F` | Construction API exists; no frozen PI predicate or variable convention. |
| Primitive | "primitive algebras in the sense of Jacobson" | `IsSimpleModule A M`, `FaithfulSMul A M` | Plausible witness encoding; handedness and equivalence to source terminology are unchecked. |
| Center | Conclusion uses the center of `A` | `Subring.center A`, `IsSimpleRing.isField_center` in a stronger simple-ring context | Carrier API exists; required field instance and primitive-to-simple issues remain open. |
| Finite-dimensional | `A` is finite-dimensional over its center | `Module.Finite (Subring.center A) A` is a candidate encoding | Exact scalar tower and source equivalence are not elaborated. |
| Proof reduction | density gives arbitrarily large matrix subalgebras unless finite matrix order; identity contradicts all matrix sizes | `jacobson_density`, matrix and finite-module APIs | Ingredients only; no formal composition or target proof exists. |
| Division-algebra branch | reduce to a division algebra and extend scalars to a maximal subfield | division rings, tensor products, choice APIs | Full source-node and formal route audit remains downstream. |
| Ring extension | Section 4(c) permits operator coefficients satisfying an injectivity condition | no candidate selected | Distinct root; must not be merged with Theorem 1 silently. |

## Formal discovery boundary

`IntakeProbe.lean` elaborates eleven exact adjacent declarations from two pinned modules. The
representative axiom reports for `jacobson_density` and
`IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite` are recorded only as discovery output.
No theorem is declared, no canonical expression or transport is checked, and no proof body is
credited to `THM-M-0039`.

A bounded case-insensitive search over repository-local Lean and pinned mathlib found no occurrence
of Kaplansky's PI theorem, "primitive algebra satisfying a polynomial identity", or an equivalent
named target. Generic uses of the words "polynomial identity" and the unrelated `Matrix.piRingEquiv`
identifier do not constitute candidates.

## First failed source/statement gate

The exact statement gate fails closed until an independent reviewer resolves the 1958/1948
chronology, approves Theorem 1 or another pinpoint result as the intended catalogue root, freezes
all definitions and binders, and checks the source-to-Lean encoding. The inspected paper is real
evidence for a constrained theorem family, not permission to invent the missing selection.
