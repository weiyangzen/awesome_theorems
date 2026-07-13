# THM-M-0092 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Cartan-Weyl theorem. The repository supplies only the gloss "classification and representations of
semisimple Lie algebras," attributes it jointly to Elie Cartan and Hermann Weyl in 1913, and labels
it verified. Under rev-5.6 that label is untrusted inventory metadata, not an exact proposition,
source audit, or proof.

The wording combines at least two large, non-interchangeable theorem families: classification of
finite-dimensional semisimple Lie algebras by root data/Dynkin type, and structure or classification
theorems for their finite-dimensional representations. It does not say whether the representation
clause means Weyl complete reducibility, highest-weight classification, a character theorem, or a
combined classification program. Selecting any one would silently narrow the catalog target.

Pinned mathlib contains genuine adjacent infrastructure: semisimple Lie algebras, their atomic
simple ideals and trivial radical, Cartan subalgebras, a root-system construction under explicit
finite-dimensional splitting hypotheses, classical Lie algebras, and Cartan matrices. The bounded
`IntakeProbe.lean` authenticates those interfaces. None is credited as a proof of the unresolved
catalog root, and the later anchor audit remains open.

The provisional vector is `[H1, M3, R4]`: classical source families exist, but no exact source
statement or assumption crosswalk has been accepted; only definitions, directional constructions,
and interfaces are identified for the unresolved formal root; and no source-faithful reconstruction exists. `instance.json` is the
structured scope authority and `task-dag.json` keeps all six downstream phases open. No H0, M0,
R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
