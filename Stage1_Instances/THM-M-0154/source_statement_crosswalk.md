# Source-statement crosswalk

The repository source phrase `微分形式在流形边界上的积分` identifies generalized Stokes rather
than a unique formal proposition. The intake selects the compactly supported smooth-form version,
which covers noncompact manifolds. The citations below are discovery anchors, not accepted `H0`
evidence: immutable editions, page images/hashes, errata, assumption mapping, and independent review
are still required.

| Claim component | Human source anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Oriented smooth manifold with boundary and compactly supported `(n-1)`-form | John M. Lee, *Introduction to Smooth Manifolds*, 2nd ed., Graduate Texts in Mathematics 218, Springer, 2013, Stokes's theorem in Chapter 16 (commonly numbered Theorem 16.11) | charted manifold with boundary, finite-dimensional model, orientation, compact support, bundled alternating form | Primary modern textbook statement located; theorem numbering and exact pages must be checked against an immutable copy: `H1` |
| Equality `integral_M d omega = integral_boundary(M) i^* omega` | Same theorem; also Michael Spivak, *Calculus on Manifolds*, W. A. Benjamin, 1965, Chapter 4, Stokes theorem | exterior derivative, manifold-form integral, boundary inclusion pullback | The source-level equation is the root; no exact local declaration is credited |
| Boundary orientation and sign | Lee, same chapter, boundary-orientation convention preceding Stokes's theorem | induced boundary orientation with outward-normal-first convention | Mandatory scope component; reversing the convention changes the sign |
| Compact manifold formulation | Standard corollary obtained when `M` is compact | alternate target dropping compact support | Not the canonical root and no checked transport exists yet |
| Empty boundary consequence | Stokes gives `integral_M d omega = 0` when `boundary M` is empty | empty-boundary integral and zero-form lemmas | Required boundary mutation, not independent proof credit |

Pinned Lean discovery at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` found relevant but nonterminal surfaces:

- `Mathlib.Analysis.Calculus.DifferentialForm.Basic` defines exterior differentiation for forms on
  normed spaces and proves selected identities such as a second exterior derivative being zero.
- `Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary` and neighboring manifold modules provide
  boundary infrastructure.
- A repository-local search for `Stokes`, boundary-integral patterns, and exterior-derivative
  declarations did not locate a generalized manifold Stokes theorem. This bounded negative search
  must be repeated and expanded during anchor audit; it is not evidence of global absence.

The statement phase must choose explicit Lean encodings for differential forms on a manifold,
orientation, compact support, integration, exterior differentiation, boundary inclusion, and the
`n = 0` boundary. It must then elaborate and mutation-test the ordered binders and sign convention.
Until that succeeds, there is no machine statement credit and no broadened Euclidean-box,
divergence, Green, or contour theorem may substitute for the root.

Discovery links, not immutable evidence receipts:

- Lee 2013: <https://doi.org/10.1007/978-1-4419-9982-5>
- Spivak 1965: <https://archive.org/details/CalculusOnManifolds>
