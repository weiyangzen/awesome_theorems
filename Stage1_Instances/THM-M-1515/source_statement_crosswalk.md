# Source-statement crosswalk

| Claim component | Human source anchor | Intended formal surface | Intake assessment |
|---|---|---|---|
| Continuous variational symmetry gives a first integral | E. Noether, *Invariante Variationsprobleme*, Nachrichten von der Gesellschaft der Wissenschaften zu Goettingen, Math.-Phys. Klasse (1918), pp. 235-257, especially the first theorem and its finite-group case | Root implication from variational symmetry and Euler-Lagrange dynamics to conserved charge | Primary historical source identified, but German wording, theorem scope, page-level premises, and corrections are not yet independently audited: `H1` |
| Euler-Lagrange solution condition | Same paper's variational setup and Lagrange expressions | `IsEulerLagrange`: a covector-valued `HasDerivAt` equation on a `ContDiff Real 2` curve | Exact Lean statement frozen; historical convention match remains `H1` |
| Boundary-term form of a variational symmetry | Modern quasi-invariance formulation; precise primary/secondary edition not yet selected | `IsVariationalSymmetry`: infinitesimal variation equals `fderiv Real boundary x v` | Sign and vertical-transformation convention frozen in Lean; source genealogy remains open |
| Noether charge | Momentum paired with the infinitesimal configuration generator, adjusted by `B` | `noetherCharge E D q t = partial_v L (generator) - boundary` | Time transformations are explicitly excluded rather than conflated |
| Constancy conclusion | Derivative-zero lemma on a connected interval | `forall t, HasDerivAt (noetherCharge E D q) 0 t` | Exact derivative-zero expression elaborates; conversion to pairwise constancy is a downstream lemma, not part of this target |

Discovery links, not immutable evidence receipts:

- Noether's original paper bibliographic record: <https://eudml.org/doc/59024>
- English translation: M. A. Tavel, *Invariant Variation Problems*, Transport Theory and Statistical Physics 1 (1971), pp. 186-207, <https://arxiv.org/abs/physics/0503066>

The repository phrase "symmetry and conservation quantity correspondence" is broader than the
selected implication. Calling it a correspondence could include converse theorems or Noether's
second theorem, so those are excluded rather than silently claimed. The statement node selects
vertical transformations that fix time, freezes the total-derivative and charge-sign conventions,
elaborates the resulting expression, and mutation-tests four material changes. No `H0`,
machine-proof, or source-completeness claim is made.
