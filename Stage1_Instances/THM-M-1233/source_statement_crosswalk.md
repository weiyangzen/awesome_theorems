# Source-statement crosswalk

| Claim component | Human source anchor | Lean target candidate | Intake assessment |
|---|---|---|---|
| Three-dimensional incompressible Euler evolution | J. T. Beale, T. Kato, A. Majda, "Remarks on the breakdown of smooth solutions for the 3-D Euler equations", *Communications in Mathematical Physics* 94 (1984), 61-66, Theorem 1 | PDE and solution predicates not yet located | Primary paper and theorem pinpoint located; exact transcription still needs source-file pin and independent review |
| Finite-time breakdown/continuation boundary | Same, Theorem 1 and its stated smooth-solution setting | maximal solution and extendibility predicates | Must not be weakened to an a priori estimate |
| Vorticity diagnostic | Same, Theorem 1: time-integrated maximum norm of `omega = curl u` | `curl`, `L∞`/essential-supremum, and interval integral expression | Mathematical objects identified; no elaborated Lean expression exists |
| Contrapositive continuation form | Same theorem, read as the continuation criterion | checked equivalence between noncontinuation and finite-integral implication | Logical transport and local well-posedness premises remain to be checked |
| Sobolev propagation machinery | Same paper, proof estimates following Theorem 1 | future subsidiary obligations | Proof architecture only; it cannot replace the root statement |

Bibliographic discovery link: <https://doi.org/10.1007/BF01212349>. This URL and citation are not an
immutable evidence receipt. `H1` records that a primary theorem anchor has been found but its exact
assumptions, notation, page-level clauses, publication scan hash, corrections/errata, and an
independent source review are not accepted.

The Stage0 wording omits dimension, spatial domain, solution regularity, initial-data conditions,
maximal-time semantics, and the precise integrability norm. Those omissions are filled here from the
named original theorem rather than by choosing an easier modern variant. The statement phase must
verify every filled field against a pinned copy. It must also mutation-test removal of divergence
freedom and maximality, replacement of `R^3` by `T^3`, replacement of `L∞` by a finite `L^p` norm,
and conversion of the improper endpoint integral.

No claim is made that mathlib currently formalizes the incompressible Euler solution theory or the
Beale-Kato-Majda criterion. Anchor discovery, exact declaration types, revisions, licenses,
placeholder checks, and integration feasibility belong to the dependent anchor-audit phase.
