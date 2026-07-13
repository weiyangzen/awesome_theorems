# THM-M-0064 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item named the
Abel-Ruffini theorem. The repository attributes it to Niels Abel and Paolo Ruffini, dates it to
1824, and gives only the gloss `五次及以上一般多项式方程无根式解` (general polynomial equations
of degree five and above have no solution by radicals). Its `已验证` label is untrusted inventory
metadata, not an exact statement or proof receipt.

## Planned boundary

The gloss does not define a "general" polynomial, the coefficient field, the quantifier over
degree, or "solution by radicals." It might mean that no uniform radical formula solves all monic
polynomials of degree at least five, that a generic polynomial has nonsolvable Galois group, or
only that for every such degree some polynomial is not solvable by radicals. Those are different
propositions. Intake records the theorem family and requires the statement phase to select a
source-ratified variant rather than silently substituting the easiest one.

Abel's *Demonstration de l'impossibilite de la resolution algebrique des equations generales qui
passent le quatrieme degre*, collected edition pages 66-94, DOI
`10.1017/CBO9781139245807.008`, is the strongest matching primary-source lead found. Bibliographic
metadata was inspected, but no complete source proposition, incorporated definitions, proof
boundary, translation, correction/errata record, or independent review was accepted. This
supports provisional `H1`, not `H0`.

Pinned mathlib has a module explicitly titled `Mathlib.FieldTheory.AbelRuffini`. Its own module
documentation says it proves only one direction: a root solvable by radicals forces the
polynomial's Galois group to be solvable. Pinned mathlib also proves the symmetric group on five
letters is not solvable. `IntakeProbe.lean` checks these interfaces and their axiom reports. They
are substantive discovery anchors, but they do not state the catalog's generic degree-at-least-five
impossibility or provide the missing generic-polynomial/Galois-group bridge. They receive `M3`
interface credit, never root proof credit.

The provisional vector is `[H1, M3, R4]`. All six downstream tasks remain open. No canonical Lean
expression, exact source statement, accepted execution state, `H0`, `M0`, `R0`, audit completion,
theorem completion, or master acceptance is claimed.
