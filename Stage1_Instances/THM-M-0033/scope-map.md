# Scope map

## Received claim

The repository record gives only the title "Serre's conjecture" and the gloss "projective modules
over polynomial rings are free." That is enough to identify a theorem family, but not enough to
select a truth-valued proposition. This intake freezes the family boundary rather than inventing a
canonical theorem.

## Candidate classical boundary

A familiar modern reading has the following ingredients, each still requiring a pinpoint source
and an independently checked Lean transport:

- a coefficient field or another precisely specified commutative base ring `k`;
- a polynomial algebra in a finite, explicitly indexed family of indeterminates;
- a module `P` over that algebra, with finite-generation or finite-presentation conditions fixed;
- projectivity of `P` under a selected equivalent definition;
- the conclusion that `P` is free as a module over the same polynomial algebra;
- an exact convention for whether freeness includes a finite basis and how rank is represented.

The quantifier order, universe levels, coefficient generality, and finite-variable encoding are part
of the theorem. They may not be selected merely because one modern slogan is common.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

1. `Module.Projective R P` expresses that a module is projective.
2. `Module.Free R P` expresses that a module is free.
3. `Module.Projective.of_free` supplies the general implication free implies projective. This is
   the converse direction from the requested projective-to-free result and cannot close the root.
4. `Polynomial k` and `MvPolynomial sigma k` supply candidate one-variable and indexed-variable
   polynomial encodings.

The bounded repository and pinned-mathlib search found no declaration named or documented as the
Quillen-Suslin theorem, Serre's conjecture, or the full projective-module-over-polynomial-ring
freeness result. The APIs above are adjacent definitions only, so the intake machine status is M4.

## Decisions required at statement freeze

1. Preserve and hash a lawful primary or authoritative source edition and independently review the
   exact problem/result passage, incorporated definitions, assumptions, conclusion, and errata.
2. Fix the coefficient domain: field, principal ideal domain, regular ring, or another class.
3. Fix one variable, finitely many named variables, or a finite index type, including the zero-
   variable case.
4. Fix finite generation, finite presentation, constant-rank, and any other module hypotheses.
5. Select the exact projective and free predicates and prove transports to source terminology.
6. Resolve the zero module, zero-variable algebra, rank-zero and nonconstant-rank cases, and all
   universe/typeclass constraints.
7. Decide whether the root is the original 1955 question, a Quillen or Suslin solution statement,
   or a later generalization. Alternate forms require checked transports rather than shared names.

## Explicit exclusions

- The adjacent `THM-M-0034` Quillen-Suslin catalogue entry as inherited proof or status evidence.
- A result about projective space, projective geometry, projective limits, or projective objects in
  an unrelated category.
- The implication free implies projective (`Module.Projective.of_free`) used in reverse.
- A one-variable, local-ring, PID, finite-rank, stable-freeness, or vector-bundle special case used
  as the unrestricted root without a source decision.
- A strengthened premise that assumes a basis, freeness, or the desired trivialization.
- Mathlib's `docs/1000.yaml` title entry, a search hit, or the catalogue's verified label used as
  theorem or proof evidence.

No canonical Lean expression, ordered binders, complete hypotheses, conclusion encoding, alternate
transport, or excluded degenerate case is frozen by this intake.
