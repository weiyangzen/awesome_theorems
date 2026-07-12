# THM-M-0025 scope map

## Human claim selected at intake

For every commutative ring `R`, if `R` is Noetherian, then the univariate polynomial ring `R[X]`
is Noetherian. The ordered mathematical binders are the ring, its commutative-ring structure, and
its Noetherian hypothesis; the conclusion concerns the polynomial ring over that same coefficient
ring.

This is a repository-scope selection from a concise catalog gloss, not an `H0` source finding. The
statement phase freezes the conventional scope as an elaborated canonical Lean expression; a
pinpoint immutable historical source packet and independent source review remain open on the H
axis.

## Scope decisions

| Surface | Selected meaning | Open verification |
|---|---|---|
| Base object | commutative ring `R` | primary-source convention and exact structure hierarchy |
| Noetherian hypothesis | every ideal of `R` is finitely generated | checked finite-generation iff exists; source definition chain remains open |
| Polynomial ring | one indeterminate over `R` | exact carrier and universe fingerprint frozen |
| Conclusion | every ideal of `R[X]` is finitely generated | canonical elaboration and checked iff frozen |
| Logic | ordinary proposition; no computational output | exact foundation and transitive trust audit |

## Boundary cases

- The intended target includes the zero ring; mathlib's `CommRing` does not impose
  `Nontrivial`, and the catalog supplies no exclusion.
- Fields, integral domains, principal ideal rings, and finite rings are included only as instances
  of the general hypothesis, never as replacements for it.
- Constant and zero polynomials are elements of `R[X]`; the theorem is about every ideal of the
  whole polynomial ring, not about one chosen polynomial.
- One variable is selected. The finite-variable multivariate theorem is a consequence/extension
  that requires a separate checked relationship; arbitrary infinitely many variables are not the
  theorem and need not preserve Noetherianity.
- Noncommutative left- or right-Noetherian polynomial-ring variants are excluded. Mathlib's generic
  `IsNoetherianRing` terminology can describe a left-module convention, but the located Hilbert
  basis declaration explicitly assumes `CommRing R`.

## Non-substitution rules

- Do not substitute Hilbert's Nullstellensatz, the weak Nullstellensatz, Hilbert polynomials, or a
  finite-generation theorem about one ideal.
- Do not weaken the claim to a field, PID, integral domain, finite ring, or fixed coefficient ring.
- Do not broaden it to all finite type algebras or finitely many variables without a checked
  directional crosswalk back to the exact root.
- Do not assume the conclusion as an instance, structure field, oracle result, or unchecked
  certificate.
- Do not treat the catalog's verified label, a declaration name, or successful `#check` output as
  proof credit.

## Downstream handoff

The statement phase has fixed the Noetherian finite-generation encoding, elaborated the target
with two statement-only imports, recorded expression and environment fingerprints, checked its
credited alternate encoding and zero-ring boundary, and distinguished all four required mutation
classes. The anchor audit has now authenticated an exact pinned mathlib wrapper, inspected its
terminal body and provenance boundary, and recorded its sorry/axiom result as an unaccepted
`M0-W / E2` candidate. `BoundaryProbe.lean` separately validates `PUnit` as a concrete zero-ring
coefficient antecedent. Obligation-tree expansion, proof-phase integration, full transitive trust,
release-grade evidence, source fidelity, and independent review remain open.
