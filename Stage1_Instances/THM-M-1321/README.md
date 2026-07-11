# THM-M-1321 rev-5.6 intake

This directory is the `planned` intake for the Zhong-Yang estimate. The repository source phrase
"lower bound for the first eigenvalue of a convex domain" is not precise enough to freeze an exact
theorem: the classical Zhong-Yang result concerns the first nonzero Laplace-Beltrami eigenvalue of
a compact Riemannian manifold with nonnegative Ricci curvature, whereas a convex-domain lower
bound is commonly associated with the Payne-Weinberger inequality.

The intended claim is therefore recorded without silently repairing the source. Primary-source
inspection must resolve the attribution and choose the geometric setting before the statement
phase freezes binders or a Lean expression. The provisional root vector is `[H3, M4, R4]`; no
machine proof, audit completion, or theorem completion is claimed.

`scope-map.md`, `source-statement-crosswalk.md`, and `task-dag.json` define the downstream work.
Exact intake checks and their results are recorded in `validation.md`.
