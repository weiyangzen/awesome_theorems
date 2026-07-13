# THM-M-0224 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the complex-analysis Liouville
theorem. The repository gives the title, Joseph Liouville, 1844, and the gloss "every bounded
entire function is constant." That identifies a classical theorem family, but the record supplies
no bibliography, exact definition of entire or bounded, binder order, conclusion encoding, proof
boundary, correction history, or independently reviewed source crosswalk. Its `已验证` label is
untrusted inventory metadata, not proof evidence.

Pinned mathlib contains direct named interfaces in `Mathlib.Analysis.Complex.Liouville`. They prove
a stronger vector-space formulation for complex-differentiable maps `E -> F` with bounded range,
using pairwise equality, an existential pointwise constant, or equality with `Function.const` as
the conclusion. `IntakeProbe.lean` authenticates these interfaces. Intake does not silently choose
the general `E -> F` theorem instead of the scalar `Complex -> Complex` catalog family, decide
among the three conclusion encodings, or credit an unaudited proof body.

The provisional vector is `[H1, M3, R4]`: the historically proved family is recognizable but no
pinpoint human source and assumption mapping has been accepted; usable exact-topic pinned
interfaces exist but no canonical source-faithful Lean expression or checked transport is frozen;
and no readable proof reconstruction exists. `instance.json` is the structured scope authority,
while `task-dag.json` keeps all six downstream phases open.

The same title is also used by separate repository targets for Hamiltonian volume preservation and
bounded harmonic functions. Those targets, number-theoretic Liouville results, and their evidence
are explicitly outside this target. No canonical proposition, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
