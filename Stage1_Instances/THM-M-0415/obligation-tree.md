# THM-M-0415 frozen obligation tree

The frozen route follows the actual pinned mathlib construction.  It specializes the general
class-number theorem to a number field, reduces finite extensions to the algebraic-extension
construction, builds a finite approximation, obtains representative ideals, proves a surjection
onto the class group, constructs `Fintype` data, and finally transports that data to `Finite`.

## M0415-ROOT

The exact `IdealClassGroupFiniteTarget`.  Its only proof child is the final checked wrapper.

## M0415-S-DEFINITIONS

Freeze the arbitrary universe, `Field K`, `NumberField K`, ring of integers, `ClassGroup`, and
propositional `Finite` interface.  This is a refinement obligation, not duplicate root credit.

## M0415-S-BOUNDARY

Keep the rational field, class-number-one fields, every finite degree, and every signature.  The
statement phase checked the rational boundary and rejected four scope mutations.

## M0415-S-TRANSPORT

`idealClassGroupFiniteTarget_iff_fintypePresentation` checks both directions between the exact
`Finite` proposition and inhabited `Fintype` data.

## M0415-S-FOUNDATION

Audit the complete axiom, quotient, classical-choice, imported-artifact, and TCB closure.  The
anchor's three-axiom report is scoped evidence, not this release-grade closure.

## M0415-X-NUMBERFIELD-INSTANCE

`NumberField.RingOfIntegers.instFintypeClassGroup` specializes
`ClassGroup.fintypeOfAdmissibleOfFinite` to `Q`, `K`, and `AbsoluteValue.absIsAdmissible`.

## M0415-N-FINITE-EXTENSION

`fintypeOfAdmissibleOfFinite` supplies the fraction-ring and Dedekind-domain instances, chooses an
integral basis, and reduces the finite-extension case to `fintypeOfAdmissibleOfAlgebraic`.

## M0415-C-FINITE-APPROX

Construct the finite admissible-absolute-value approximation and prove the norm approximation
property.  This central construction remains explicit even though the public instance is one line.

## M0415-C-IDEAL-REPRESENTATIVES

`exists_mk0_eq_mk0` proves that every ideal class has a representative containing the product of
the finite approximation, placing representatives in a finite divisor subtype.

## M0415-L-SURJECTION

`mkMMem_surjective` maps that finite subtype to the class group and proves every class is hit.

## M0415-T-ALGEBRAIC-FINTYPE

`fintypeOfAdmissibleOfAlgebraic` applies `Fintype.ofSurjective` to the finite representative type
and the preceding surjection.

## M0415-T-FINTYPE-PRESENTATION

`fintypePresentation_mathlib` packages the pinned instance into the exact data-bearing child.

## M0415-T-FINITE-WRAPPER

`finiteTarget_of_fintypePresentation` is the checked child-to-root composition.  The additionally
checked `idealClassGroupFinite_mathlib` composes it with the pinned candidate, without relocating
or duplicating the mathlib proof body.

## M0415-X-SOURCE

Pinpoint reviewed primary-source passages for admissibility, approximation, ideal representatives,
and surjectivity.  This human-source boundary carries no machine-proof credit and remains open.

## M0415-X-PROVENANCE

Resolve terminal bodies, all transitive declarations/imports, axioms, TCB elements, source hashes,
licenses, and replay receipts.  It is an informational release overlay and remains open.

All leaf budgets are at most 100.  That is a split threshold, not `R0`.  The exact wrapper and
pinned candidate elaborate provisionally, but H0, R0, complete provenance/trust, accepted receipts,
audit completion, theorem completion, and master acceptance are not claimed.
