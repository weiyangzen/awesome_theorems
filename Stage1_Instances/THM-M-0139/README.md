# THM-M-0139 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the classical Kazhdan-Lusztig
conjecture. The repository's inherited phrase "Kazhdan-Lusztig polynomials in
representation theory" is not itself an exact theorem statement. This intake therefore
freezes the intended source family and records the convention-sensitive formula as an
open statement-phase obligation rather than silently choosing conventions.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | The classical multiplicity conjecture of Kazhdan-Lusztig (1979), Conjecture 1.5: composition multiplicities of simple highest-weight modules in Verma modules are given by values at `1` of Kazhdan-Lusztig polynomials | Weyl-group indexing, dot-action, longest-element, and Verma-module conventions must be copied from a pinned primary source before a formula is frozen |
| Coxeter/Hecke layer | Weyl group, Bruhat order, Hecke algebra, Kazhdan-Lusztig basis and polynomials | Definitions and normalizations are not credited or formalized here |
| Representation layer | A regular integral block of BGG category `O`, Verma modules, simple quotients, and Jordan-Holder multiplicity | Singular, parabolic, affine, and arbitrary Coxeter generalizations are outside the root unless connected later by checked transports |
| Geometric proof layer | Localization/intersection-cohomology routes used by the historical proofs | Source/proof architecture only; no machine closure is claimed |
| Lean layer | A future exact Lean 4 expression using pinned algebra, Coxeter, category, and representation APIs | No repo-local declaration or elaborated expression is claimed at intake |
| Foundations | Lean 4 kernel under versioned foundation, TCB, and computation profiles | Exact profiles and dependency closure remain open |

Positivity of coefficients, the Kazhdan-Lusztig basis, character formulas, and later
generalizations are related results, not interchangeable roots. The dependent statement phase
must resolve the remaining convention choices against the primary text or stop; it must not
replace the root with a convenient polynomial identity.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
the exact statement gate: the inherited metadata is underspecified, the source-native formula has
not yet been pinned and transcribed, and no Lean expression fingerprint exists. No proof state is
accepted and the theorem is not complete.

Validation commands and their exact results are recorded in `validation.md`.
