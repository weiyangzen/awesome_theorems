# THM-M-1345 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Hartman-Grobman theorem. The
repository supplies only the gloss "local linearization of a hyperbolic equilibrium," attributes
the result to Philip Hartman and David Grobman in 1960, and labels it `已验证`. Under rev-5.6,
that label is untrusted metadata and supplies neither a source statement nor proof credit.

The gloss identifies the classical continuous-time theorem family but not one binder-complete
proposition. In particular, it does not select finite-dimensional Euclidean or Banach-space scope,
the regularity of the vector field, the definition of hyperbolicity, the local neighborhoods and
time domain, or whether the conjugacy preserves time parametrization. It also does not rule out the
distinct discrete-map formulation.

One primary historical candidate was inspected: Philip Hartman's 1960 paper, Theorem (II), page
615. It treats `x' = T x + F(x)` near zero, assumes `F = o(|x|)`, `F` is `C2`, and every eigenvalue
of the real matrix `T` has nonzero real part, and obtains a local continuous one-to-one coordinate
map conjugating the nonlinear flow to `exp(tT)`. This is a strong source candidate, but the
catalogue does not select it, the incorporated definitions and boundary conventions have not been
fully transcribed into a canonical claim, and no independent source review is complete. A modern
textbook candidate has different presentation and regularity conventions. Neither is silently
promoted to the target.

This intake freezes the received wording, source candidates, proposition-changing decisions,
neighbor boundaries, and adjacent pinned Lean APIs. It deliberately leaves the canonical
mathematical statement and Lean target null. The root vector is `[H1, M4, R4]`: a published primary
candidate and proof are known but their exact source-to-target mapping is unaccepted; no usable
exact Lean artifact was located; and no source-faithful proof reconstruction can attach before the
proposition is frozen.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` preserve the mathematical and source boundaries, while
`task-dag.json` keeps all downstream phases open. `IntakeProbe.lean` checks only adjacent pinned
ODE, flow, derivative, fixed-point, and local-homeomorphism interfaces. No exact-statement, H0,
M0, R0, audit-completion, theorem-completion, or master-acceptance credit is claimed.
