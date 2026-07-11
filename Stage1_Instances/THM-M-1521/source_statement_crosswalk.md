# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Finite invariant measure implies recurrence | H. Poincare, *Sur le probleme des trois corps et les equations de la dynamique*, Acta Mathematica 13 (1890), pp. 1-270, especially the recurrence discussion near pp. 65-72 | local candidate `StatementShape`; mathlib `MeasurePreserving.conservative` plus `Conservative.ae_mem_imp_frequently_image_mem` | Primary historical source located, but edition-level translation, exact premise mapping, and errata audit are not accepted: `H1` |
| Almost every point of a measurable set returns infinitely often | K. Petersen, *Ergodic Theory*, Cambridge University Press (1983), recurrence theorem in the introductory measure-preserving theory | `Conservative.ae_mem_imp_frequently_image_mem` | Modern formulation candidate; theorem/page and assumption crosswalk must be verified against a fixed edition |
| Neighborhood recurrence | Standard topological consequence of conservativity | `Conservative.ae_frequently_mem_of_mem_nhds` | Optional strengthening requiring second countability and measurable opens; excluded from the exact root |
| Bounded Hamiltonian system wording | Physical corollary only after an invariant finite-measure region and measure-preserving time map are constructed | future finite invariant model wrapper | Not equivalent by wording alone; phase-space, Liouville, energy-shell, and flow bridges remain `formalization_debt` |

The frozen human claim deliberately uses a discrete transformation. A continuous measure-preserving
flow may instantiate it at a chosen positive time, but that bridge must be stated and checked. The
word "bounded" is not substituted for finite invariant measure: topological boundedness alone does
not supply a finite invariant measure or preservation proof.

No `H0` or machine-closure claim is made. Later source audit must pin scans/editions, verify page and
theorem locations, map every assumption, search corrections and translation issues, and obtain
independent review. Later anchor audit must inspect actual declaration types at the repository's
immutable mathlib revision rather than trusting the historical local wrapper.
