# Source-statement crosswalk

| Claim component | Primary source anchor | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Ricci flow framework and entropy/noncollapsing estimates | G. Perelman, *The entropy formula for the Ricci flow and its geometric applications*, arXiv:math/0211159 (2002), especially introduction and Sections 1-4 | smooth 3-manifold, Riemannian metric, Ricci flow, entropy and noncollapsing predicates | Primary proof-series source identified; exact premise-to-node and correction audit remains open |
| Ricci flow with surgery and long-time analysis | G. Perelman, *Ricci flow with surgery on three-manifolds*, arXiv:math/0303109 (2003), especially Sections 1, 4-8 | surgery solution, canonical neighborhoods, topology-preserving transition certificates | Primary source identified, but it is not by itself a concise formal root statement |
| Finite extinction used for the simply connected/spherical case | G. Perelman, *Finite extinction time for the solutions to the Ricci flow on certain three-manifolds*, arXiv:math/0307245 (2003), Theorem 1.1 | finite-extinction predicate and a checked bridge to spherical topology | Pinpoint theorem located; all hypotheses and the topological consequence need formal crosswalk |
| Geometrization root | The three papers above as the primary proof series; theorem formulation must also be reconciled with a primary formulation of Thurston's conjecture | a predicate expressing canonical decomposition into pieces supporting the prescribed locally homogeneous geometries | Root wording is frozen, but source edition, exact formulation, errata, and assumption mapping are not accepted: `H1` |
| Poincare corollary | Simply connected specialization of geometrization, supported by the finite-extinction branch | `ClosedSimplyConnectedThreeManifold M -> Nonempty (M ≃ₜ S3)` or an equivalent checked formulation | Candidate expression only; object types, homeomorphism API, and implication are deferred |

The papers establish a deep proof architecture rather than presenting a single declaration-shaped
sentence matching a current Lean API. The statement phase must choose the precise manifold category,
define the geometrization conclusion without weakening it, elaborate the root, and mutation-test
dimension, compactness/boundary, orientability, connectedness, and simple connectivity. It must also
prevent the Poincare corollary from replacing the stronger root.

Discovery links, not immutable evidence receipts:

- <https://arxiv.org/abs/math/0211159>
- <https://arxiv.org/abs/math/0303109>
- <https://arxiv.org/abs/math/0307245>

No `H0` or machine-closure claim is made. Required follow-up includes immutable file hashes,
publication-version reconciliation, errata/correction search, theorem/section-to-obligation mapping,
and independent review.
