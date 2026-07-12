# THM-M-1399 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `向后微分公式`
(backward differentiation formula, BDF). The catalog supplies only that name, a collective
twentieth-century attribution, and the gloss `刚性方程的数值方法` (a numerical method for stiff
equations). It supplies no formula, cited source, order, coefficient convention, problem setting,
hypotheses, conclusion, or proof. Its `已验证` status is untrusted metadata under rev-5.6.

A backward differentiation formula names an implicit numerical-method family, not one
binder-complete theorem. Compatible readings include the recurrence for one fixed order, the
derivative-of-interpolant construction, a coefficient identity, consistency or order, zero
stability, convergence, a stability-region theorem, and an implicit-step solvability result. These
are different propositions. Choosing BDF1 or BDF2, constant steps, a scalar ODE, or a particular
stability theorem from memory would substitute a new target.

This intake freezes that ambiguity rather than inventing mathematics. The provisional root vector
is `[H5, M4, R4]`. `H5` records that the supplied method gloss is not a stable truth-valued
proposition; it does not say that standard BDF results are false or open. No source-identical Lean
target or readable proof route can be attached before a proposition is selected.

Curtiss and Hirschfelder's 1952 article *Integration of Stiff Equations* and Gear's 1971 article
*The automatic integration of ordinary differential equations* were identified through immutable
bibliographic metadata as historical discovery leads. Neither is selected by the catalog, and no
formula, theorem passage, assumptions, proof boundary, or errata record from either article is
accepted here.

`IntakeProbe.lean` checks only pinned derivative, ODE, Picard-Lindelof, and polynomial-interpolation
interfaces adjacent to a future encoding. It states no BDF theorem and receives no statement or
proof credit. The structured scope authority is `instance.json`, the resolution boundary is in
`scope-map.md`, the literal source crosswalk is in `source-statement-crosswalk.md`, and all six
downstream phases remain open in `task-dag.json`.

The lifecycle is `planned`. No canonical Lean expression, H0, M0, R0, accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
