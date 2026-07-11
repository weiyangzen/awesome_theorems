# Source-statement crosswalk

| Claim component | Human source anchor | Intended formal surface | Intake assessment |
|---|---|---|---|
| Continuous variational symmetry gives a first integral | E. Noether, *Invariante Variationsprobleme*, Nachrichten von der Gesellschaft der Wissenschaften zu Goettingen, Math.-Phys. Klasse (1918), pp. 235-257, especially the first theorem and its finite-group case | Root implication from variational symmetry and Euler-Lagrange dynamics to conserved charge | Primary historical source identified, but German wording, theorem scope, page-level premises, and corrections are not yet independently audited: `H1` |
| Euler-Lagrange solution condition | Same paper's variational setup and Lagrange expressions | A predicate on a twice differentiable curve | Coordinate/chart and regularity conventions must be frozen before Lean elaboration |
| Boundary-term form of a variational symmetry | Modern quasi-invariance formulation; precise primary/secondary edition not yet selected | Equality of the infinitesimal Lagrangian variation with a total derivative of `B` | This strengthens the usability of the selected scope but needs an accepted source genealogy and sign convention |
| Noether charge | Momentum paired with the infinitesimal configuration generator, adjusted by `B` (and by time transformation terms when admitted) | A real-valued function along a solution whose derivative vanishes | Exact formula depends on whether time transformations are in scope; statement phase must choose rather than conflate variants |
| Constancy conclusion | Derivative-zero lemma on a connected interval | `IsConstant` or pointwise equality along the trajectory | Candidate transport only; no checked Lean witness |

Discovery links, not immutable evidence receipts:

- Noether's original paper bibliographic record: <https://eudml.org/doc/59024>
- English translation: M. A. Tavel, *Invariant Variation Problems*, Transport Theory and Statistical Physics 1 (1971), pp. 186-207, <https://arxiv.org/abs/physics/0503066>

The repository phrase "symmetry and conservation quantity correspondence" is broader than the
selected implication. Calling it a correspondence could include converse theorems or Noether's
second theorem, so those are excluded rather than silently claimed. The statement phase must decide
whether transformations act on time as well as configuration, freeze the total-derivative and sign
conventions, elaborate the resulting expression, and mutation-test every material hypothesis.
No `H0`, exact-statement, machine-proof, or source-completeness claim is made.

