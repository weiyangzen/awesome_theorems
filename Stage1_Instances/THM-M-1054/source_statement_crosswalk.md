# Source-statement crosswalk

| Claim component | Human source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Cesaro means converge in Hilbert norm to the invariant component | J. von Neumann, "Proof of the Quasi-Ergodic Hypothesis", *Proceedings of the National Academy of Sciences* 18 (1932), 70-82, DOI 10.1073/pnas.18.1.70 | Abstract contraction/isometry theorem on a Hilbert space | Primary historical source identified, but its notation and hypotheses have not received a page-level premise and errata audit: `H1` |
| Measure-preserving map acts on L2 | The same paper's unitary/operator formulation of measure-preserving dynamics | Koopman operator from `T`, with well-definedness on ae-equivalence classes | Required bridge; exact mathlib construction and declaration candidates are deferred |
| Limit is the fixed component | von Neumann's decomposition into invariant and difference components | Orthogonal projection onto `ker (U - I)` / fixed-point closed subspace | Source-to-modern-form equivalence needs a detailed crosswalk and checked Lean transport |
| Probability-space L2 formulation | Repository source gloss: `L^2` ergodic theorem | Real-valued `MeasureTheory.Lp` root described in `intake.json` | This is the frozen Stage1 root; the repository supplies no more detailed original statement |
| Conditional-expectation formulation | Standard modern ergodic-theory restatement | Conditional expectation onto the invariant sigma-algebra | Alternate encoding only; not part of the root and not credited |

The root deliberately asserts norm convergence, not pointwise or almost-everywhere convergence.
Those stronger modes belong to Birkhoff-type results and would broaden this target. It also does not
assume ergodicity: without ergodicity the limit is the invariant projection rather than necessarily
the constant expectation.

Discovery link (not an immutable evidence receipt):

- von Neumann paper: <https://doi.org/10.1073/pnas.18.1.70>

No `H0` or machine-closure claim is made. The source audit must still acquire a content-addressed
copy, pinpoint pages and premises, check corrections and translation conventions, and obtain
independent review. The statement phase must then select the actual mathlib types, elaborate the
ordered binders, serialize the normalized expression, and mutation-test the probability,
measure-preservation, L2, averaging-index, and convergence-mode boundaries.
