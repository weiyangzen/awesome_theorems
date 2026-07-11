# THM-M-1315 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Riemannian Penrose inequality. It records
scope and source candidates only; it contains no Lean declaration or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | The time-symmetric three-dimensional Riemannian Penrose inequality for a complete asymptotically flat manifold with nonnegative scalar curvature and outermost minimal boundary | The exact regularity, end, boundary, and ADM-mass APIs must be frozen in the statement phase |
| Quantitative conclusion | `m_ADM >= sqrt (area boundary / (16 * pi))` | Units and normalization are fixed mathematically; their Lean encoding is still open |
| Rigidity | Equality characterizes the spatial Schwarzschild exterior | Included in the theorem family, but whether it is one root or a linked rigidity root must be resolved against the primary theorem text |
| Geometric objects | Smooth Riemannian 3-manifold, chosen asymptotically flat end, scalar curvature, compact outermost minimal boundary, area, ADM mass | No repository-local definitions have yet been selected or credited |
| Proof routes | Huisken-Ilmanen inverse mean curvature flow for the connected-horizon case; Bray conformal flow for the general case | Architecture discovery only; neither route is machine-closed here |
| Foundations | Lean 4 kernel plus pinned mathlib differential geometry, measure, topology, and analysis | Exact toolchain, imports, classical axioms, and dependency closure remain open |

The root does not mean the Lorentzian Penrose conjecture, an arbitrary-dimensional analogue, or a
charged/cosmological variant. It also does not replace the ADM mass by an unspecified scalar or
drop asymptotic flatness, nonnegative scalar curvature, minimality, or outermostness.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact-statement gate: the primary-source assumptions have not yet been reduced to an elaborated
Lean expression and the needed geometric object model is not frozen. The theorem is not complete.

Validation and its limits are recorded in `validation.md`.
