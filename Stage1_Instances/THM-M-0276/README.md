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

The vector remains `[H2, M3, R4]`: the exact Lean interface is frozen, while the printed proof gap,
catalog identity, primary history, independent source review, formal anchor/provenance audit, and
readable reconstruction remain open. `statement.json` and `statement-receipt.json` record the
provisional node evidence. No H0, M0, R0, accepted proof state, audit completion, theorem
completion, or master acceptance is claimed.
