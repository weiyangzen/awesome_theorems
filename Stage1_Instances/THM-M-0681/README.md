# THM-M-0681 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository item "differentially
closed fields". The repository supplies only the phrase "axiomatization of differentially closed
fields", attributes it to Abraham Robinson in 1959, and labels it verified. That is a theorem
family, not yet an exact proposition: it does not say whether the intended root is Robinson's
first-order axiomatization, the later one-variable differential-polynomial criterion commonly
associated with Blum, model-completeness, or equivalence of two presentations.

The human scope is bounded to an axiomatization theorem for ordinary differential fields of
characteristic zero with one derivation. A source-faithful root must state explicit axioms and prove
that they characterize existentially closed differential fields. The statement phase must inspect
and pinpoint the intended primary source before choosing a particular axiom scheme or encoding it
in Lean; silently replacing the repository claim by the definition of a structure named
`DifferentiallyClosed` would be circular.

Pinned mathlib supplies ordinary differential fields, derivations, differential extensions, and
characteristic-zero infrastructure, but the bounded intake search found no differential-polynomial
syntax or differentially-closed-field characterization. `IntakeProbe.lean` checks only those
available ingredients. Lifecycle remains `planned` at `[H2, M4, R4]`; no exact Lean statement,
source acceptance, proof state, audit completion, or theorem completion is claimed.
