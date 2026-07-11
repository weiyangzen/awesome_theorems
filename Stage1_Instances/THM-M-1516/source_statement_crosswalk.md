# Source-statement crosswalk

| Claim component | Human source anchor (discovery) | Lean candidate | Intake assessment |
|---|---|---|---|
| Canonical equations `qdot = partial H/partial p`, `pdot = -partial H/partial q` | V. I. Arnold, *Mathematical Methods of Classical Mechanics*, 2nd ed., Springer (1989), Chapter 8, sections 38-40 | `HamiltonianEquationOn` with `Matrix.J` | Conceptual match only; exact page text and conventions require audit |
| Hamiltonian/Lagrangian correspondence | Arnold, Chapter 8, sections 38-40 (Legendre transformation and Hamiltonian formalism) | `legendreTransformAvailable` and `equivalentEulerLagrangeForm` fields | Candidate component is only an assumed `Prop`; no checked bridge |
| Energy conservation for autonomous Hamiltonians | Arnold, Chapter 8, Hamiltonian equations discussion | `energyConservation` field | Distinct theorem requiring an exact differentiability model; not proved by the field |
| Preservation of symplectic structure by Hamiltonian flow | Arnold, Chapter 9, sections 44-45 | `symplecticFlowProperty` field; `Matrix.J_transpose`, `Matrix.J_squared` are algebraic anchors | Matrix identities alone do not establish flow existence or preservation |
| Blueprint phrase "经典力学的哈密顿形式" | `Docs/Stage1_Blueprint.md`, `S1-M-185` | legacy `StatementShape` | The phrase does not determine which of the above results is the root |

Bibliographic anchors are discovery leads, not accepted `H0` evidence. The source audit must pin a
specific edition/page/theorem, check assumptions and errata, and map every premise to the selected
Lean declaration. Arnold's book describes several related results; citing it does not license their
conjunction.

The legacy Lean candidate quantifies a data structure whose desired conclusions are themselves
unconstrained proposition fields. Its `StatementShape` asks that three hypothesis fields imply three
different conclusion fields, a claim not supplied by the source wording and generally unprovable
from those fields. It therefore cannot be frozen merely because it elaborated historically.

Required statement decision: select exactly one source-backed theorem (recommended first target:
energy conservation along a differentiable autonomous Hamiltonian trajectory on a fixed interval),
or obtain a more precise authoritative source statement. Until then the exact-statement gate remains
open and no legacy proof credit is inherited.
