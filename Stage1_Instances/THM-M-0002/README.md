# THM-M-0002 rev-5.6 dossier

This directory is the `planned` intake dossier for the five lemma. The repository source says only
that morphisms in a commutative diagram have an isomorphism property. The scope map therefore fixes
the conventional five-object, two-exact-row theorem family while leaving the exact primary-source
wording and canonical Lean declaration to the statement phase.

The statement phase now freezes the intake-selected category-theoretic formulation as
`Stage1Instances.THM_M_0002.FiveLemmaTarget` in `Statement.lean`. It uses two exact
`ComposableArrows C 4` rows in an abelian category, epi/iso/iso/mono hypotheses on components
0/1/3/4, and concludes `IsIso` at component 2. The minimal direct import, explicit elaborated
expression fingerprint, structural mutation checks, and pinned environment are recorded in
`statement.json` and `statement-validation.md`.

The legacy Lean module identifies a plausible mathlib encoding, but it is discovery input and has
not been accepted under rev-5.6. The statement is self-tested but awaits master acceptance. This
dossier now also contains a self-tested canonical proof in `Proof.lean`. It explicitly derives the
middle mono and epi facts through the two pinned four lemmas and then obtains the middle isomorphism.
The proof node remains provisional pending master acceptance and does not claim H0/R0, downstream
validation, audit completion, or theorem completion. Pinpoint primary-source fidelity remains open.

The scope map, source crosswalk, open task DAG, and exact intake checks are recorded alongside this
file.
