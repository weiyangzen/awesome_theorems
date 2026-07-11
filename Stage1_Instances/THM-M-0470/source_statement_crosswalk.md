# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Bogomolov conjecture for a curve in its Jacobian | E. Ullmo, *Positivite et discretion des points algebriques des courbes*, Annals of Mathematics 147 (1998), 167-179, DOI 10.2307/120986 | No repo-local declaration identified at intake | Primary proof paper and bibliographic locus identified; theorem/page premise mapping, immutable hash, and errata review remain open (`H1`) |
| Genus at least two, Jacobian embedding, and canonical height | Ullmo 1998, introductory setup and theorem statement | Future structures for curves, Jacobians, polarizations, and canonical heights | Exact notation, base extension, divisor choice, and normalization must be reconciled before statement credit |
| Finiteness below a positive height threshold | Ullmo's discreteness conclusion for small algebraic points | `Set.Finite {x | height (j x) <= epsilon}` as an expression shape only | Provisional semantic crosswalk, not elaborated Lean |
| Positive essential minimum / non-density form | S. Zhang, *Equidistribution of small points on abelian varieties*, Annals of Mathematics 147 (1998), 159-165, DOI 10.2307/120985, supplies the companion general framework used in the 1998 resolution | No checked candidate | Related source, not a replacement for Ullmo's curve theorem; equivalence transport remains open |
| Later general abelian-subvariety formulation | Later developments commonly called the Bogomolov conjecture | Explicitly excluded from the root | Prevents broadening the historical Ullmo attribution into a stronger theorem |

## Statement genealogy

The repository metadata names Emmanuel Ullmo and dates the item to 1998, while its Chinese
description says only "proof of the Bogomolov conjecture." The bibliographic match is Ullmo's
1998 curve theorem. Accordingly, the canonical intake claim is the small-points finiteness
statement for a curve of genus at least two inside its Jacobian. This is narrower than the modern
general formulation for arbitrary subvarieties of abelian varieties and preserves the theorem
actually attributable to the named source.

The common non-density form and the finite-small-points form require a bridge using irreducibility
and the fact that a proper closed subset of a curve is finite. The height also depends on an ample
symmetric line bundle and an embedding arising from a degree-one divisor. Neither invariance nor
equivalence is credited until checked in Lean.

## Evidence boundary

Discovery links are <https://doi.org/10.2307/120986> and
<https://doi.org/10.2307/120985>. They are not immutable evidence receipts. `H0` requires a pinned
edition or file hash, exact theorem/page/assumption mapping, correction and errata search, and
independent review. No public Lean 4 proof, mathlib anchor, or repo-local closure is claimed here;
that search belongs to the dependent anchor-audit phase.
