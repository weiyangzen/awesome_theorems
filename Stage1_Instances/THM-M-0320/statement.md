# Exact statement freeze

The frozen target follows Theorem 1 of Shizuo Kakutani, *A generalization of Brouwer's fixed point
theorem*, **Duke Mathematical Journal** 8 (1941), 457-459: a closed, bounded, convex Euclidean set
and an upper semi-continuous point-set function with nonempty closed convex values contained in the
domain have a point belonging to its value. Kakutani's preceding upper-semicontinuity definition is
the open-set containment condition characterized by mathlib's `UpperHemicontinuousOn`.

`Statement.lean` freezes this proposition over `EuclideanSpace Real (Fin n)`. It exposes domain
nonemptiness, closedness, boundedness, convexity; value nonemptiness, closedness, convexity and
containment; upper hemicontinuity on the domain; and fixed-point membership. Explicit domain
nonemptiness prevents the false empty-domain instance.

Canonical declaration: `Stage1Instances.THM_M_0320.KakutaniFixedPointTarget`.

The minimal direct imports are `Mathlib.Analysis.InnerProductSpace.EuclideanDist` and
`Mathlib.Topology.Semicontinuity.Hemicontinuity`. A trial with only the latter fails because
`EuclideanSpace` and `Convex` are unavailable. Separately elaborated mutations remove domain
nonemptiness, value nonemptiness, value containment, or weaken the conclusion; none receives proof
credit. Dimension zero remains included and values cannot escape the domain.

This phase establishes exact Lean elaboration only. It does not prove the target, accept source
fidelity at `H0`, perform the anchor audit, or claim audit/theorem completion.
