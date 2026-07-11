# Source-statement crosswalk

The repository's legacy phrase "properties of birational morphisms" is too broad to be an exact
root. This dossier selects the quasi-finite separated factorization theorem, a standard modern form
of Zariski's Main Theorem. Changing to a birational corollary requires explicit scope revision; it
cannot happen during proof search.

| Claim component | Human source anchor | Lean target candidate | Intake assessment |
|---|---|---|---|
| Quasi-finite separated `f : X -> Y` factors through an open immersion and a finite morphism | Grothendieck and Dieudonne, *EGA IV*, Zariski Main Theorem family around IV, 8.12; exact edition/page and hypotheses require source audit | Existential statement over `Scheme` morphisms and morphism-property predicates | Root formulation selected; source pinpoint and Lean names unresolved |
| Modern factorization statement | The Stacks Project, chapter *More on Morphisms*, section "Zariski's Main Theorem" (living reference; tag/revision must be pinned later) | `∃ Xbar j g, IsOpenImmersion j ∧ Finite g ∧ j ≫ g = f` in API-adjusted form | Useful statement anchor only; not immutable H0 evidence |
| Open-immersion factor | Same theorem's construction of the open part of the finite envelope | mathlib scheme open-immersion predicate, exact namespace unknown | Predicate/API audit deferred to statement phase |
| Finite factor | Same theorem's finite envelope over `Y` | mathlib finite-morphism predicate, exact namespace unknown | Predicate/API audit deferred to statement phase |
| Birational consequences | Classical corollaries often also called Zariski's Main Theorem | Possible later transports/corollaries | Explicitly excluded as substitutes for the root |

No assertion is made that the displayed Lean-shaped expression currently elaborates. In particular,
mathlib may encode morphism properties through bundled predicates, typeclasses, or `HasRingHomProperty`;
the statement phase must inspect the pinned API and serialize the normalized expression.

Required source work is still open: pin the exact EGA edition and theorem/page, pin a dated Stacks
revision and tag, map every assumption and convention (especially the definition of quasi-finite),
check corrections/errata, and obtain independent review. Consequently no `H0` claim is made.
