# THM-M-0270 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Fatou's lemma. The repository gives
only the gloss "an inequality for the liminf of integrals," attributes it to Pierre Fatou in 1906,
and labels it verified. Under rev-5.6 that label is untrusted inventory metadata, not a pinpoint
human source, an exact proposition, or kernel proof evidence.

The gloss identifies the classical measure-theoretic theorem family but omits material choices. It
does not fix the measure space, natural indexing, pointwise versus almost-everywhere convention,
nonnegative versus lower-bounded functions, measurability versus a.e. measurability, extended-real
codomain, integral convention, or the exact filter interpretation of `liminf`. Intake does not
silently choose those clauses.

Sheldon Axler's author-hosted *Measure, Integration & Real Analysis* was inspected as a modern
source lead. Section 3A, Exercise 17 on printed page 86 states the familiar nonnegative measurable
sequence inequality and explicitly calls it Fatou's Lemma. This supports `H1`, not `H0`: the
catalog does not cite Axler, Exercise 17 leaves its proof to the reader, historical provenance and
the 1906 source passage are unverified, and no independent source review is recorded.

Pinned mathlib directly contains `MeasureTheory.lintegral_liminf_le'` for a.e.-measurable
`ENNReal`-valued functions and `MeasureTheory.lintegral_liminf_le` for measurable functions, both
documented as Fatou's lemma. `IntakeProbe.lean` authenticates their interfaces and reports only
`propext`, `Classical.choice`, and `Quot.sound` in their axiom outputs. The two interfaces are close
formal candidates, not a source-transported root.

The provisional vector is `[H1, M3, R4]`: a complete standard statement and proof route are known
through a modern source lead but exact source fidelity remains open; usable pinned candidates exist
but no canonical source statement or checked transport is frozen; and no source-faithful readable
proof reconstruction is accepted. All six downstream phases remain open. No exact statement, H0,
M0, R0, accepted state, audit completion, theorem completion, or master acceptance is claimed.
