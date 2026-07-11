# Source-statement crosswalk

| Claim component | Primary-source anchor | Lean concept | Intake assessment |
|---|---|---|---|
| Multiplicative ergodic theorem | V. I. Oseledets, "A multiplicative ergodic theorem. Characteristic Ljapunov exponents of dynamical systems," *Transactions of the Moscow Mathematical Society* 19 (1968), 197-231 | root over an ergodic probability base and finite-dimensional cocycle | Primary publication identified; theorem/page, translation, assumptions, and errata review remain open: `H1` |
| A.e. exponential rates | same paper, regular-point construction | `Filter.Tendsto` for normalized `log` norm | zero-vector and extended-real conventions unfrozen |
| Invariant Lyapunov splitting | same paper, invertible regular case | measurable equivariant direct-sum subspaces | Grassmannian/submodule representation open |
| Integrability | primary theorem hypotheses on cocycle and inverse | integrable positive logarithmic operator norms | equivalence to source coordinate conditions unproved |
| Ergodic specialization | primary theorem with ergodic base | exponents constant a.e. | nonergodic spectrum excluded |

The legacy phrase omits the base system, cocycle law, integrability, exceptional set, and the
filtration/splitting distinction. The chosen invertible variant prevents silently merging
incompatible formulations, but remains provisional until exact Lean elaboration.

Discovery record (not immutable evidence): Oseledets, 1968, MathNet record
<https://www.mathnet.ru/eng/mmo214>.

No `H0` or machine-closure claim is made. Follow-up must pin a stable edition, record exact pages,
review translation/corrections, map every premise, and obtain independent review.

