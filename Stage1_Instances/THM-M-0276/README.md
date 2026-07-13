# THM-M-0276 rev-5.6 statement

This directory is the fail-closed `planned` dossier for the Banach open mapping theorem.
The repository gives Stefan Banach, 1929, and only the gloss "a surjective bounded linear
operator is an open map." Its `已验证` ("verified") label is untrusted inventory metadata under
rev-5.6, not a source audit, exact Lean proposition, or proof receipt.

The gloss identifies the classical functional-analysis theorem family, but by itself omits
proposition-changing choices. The immutable modern source admitted at intake resolves those
choices for the statement proposal: its standing convention restricts scalars to `Real` or
`Complex`, it defines Banach spaces as complete normed spaces, uses the ordinary bounded-operator
space, and defines an open map as one sending every open set to an open set.

A versioned set of Technion functional-analysis lecture notes was inspected as a modern
lecture-note source lead. Its Open Mapping Theorem states that an onto bounded operator between Banach
spaces is open and presents the standard Baire-category proof route. The printed proof has a
material but apparently repairable typo: its Baire cover repeats the unit ball where the subsequent
argument requires balls of radius `n`. No accepted correction or independent review is recorded.
The notes are not cited by the catalog, and the proof gap has no accepted correction or independent
review. They therefore continue to support only provisional `H2`, not `H0`, even though their exact
statement and definition chain are now sufficient to select a Lean statement proposal.

`Statement.lean` freezes a closed conjunction of the ordinary same-field real and complex claims.
For arbitrary universe-polymorphic complete normed spaces `E` and `F`, a bundled
`ContinuousLinearMap` with `Function.Surjective f` must satisfy `IsOpenMap f`. A checked
definitional transport expands that conclusion to the source wording `forall U, IsOpen U ->
IsOpen (f '' U)`. The stronger open-class semilinear theorem in pinned mathlib is not substituted
for this root.

The statement module uses only `Mathlib.Analysis.Complex.Basic`; it deliberately does not import
the proof-bearing Banach module. Deleting that sole import fails. Five structural mutations remove
surjectivity, drop the complex case, change binder scope, omit domain completeness, or add
injectivity, and Lean distinguishes each from the root. This is statement identity evidence, not a
proof.

The anchor audit has classified the exact pinned mathlib candidate, and the obligation-tree phase
now freezes 29 semantic IDs across the visible Baire-category, rescaling, convergent-series, and
open-image route. `typed-graphs.json` keeps proof, refinement, provenance, evidence, trust,
documentation, and workflow edges separate. `ObligationTree.lean` checks the literal upstream
terminal, same-field specialization adapter, and exact root composition; internal source-body
relations remain explicitly unverified composition plans for the proof phase.

`obligation-registry.json` is the frozen denominator authority. `typed-graphs.json`,
`validation-specs.json`, `obligation-tree.md`, `obligation-tree-validation.md`, and
`obligation-tree-receipt.json` record this provisional architecture and its validation boundary.
Real and Complex are distinct semantic branches but share one generic mathlib terminal-body
identity, so they cannot duplicate distinct-body credit.

The vector remains `[H2, M3, R4]`: the exact candidate is only unaccepted `M1/E2` evidence, the
printed human-source proof gap and independent review remain open, and no registry obligation is
closed. No H0, M0, R0, accepted proof state, audit completion, theorem completion, release, or
master acceptance is claimed.
