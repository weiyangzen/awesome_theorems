# THM-M-0631 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `贝尔纲定理` (the Baire
category theorem). The repository supplies the claim `完备度量空间是第二纲集` ("a complete
metric space is of second category"), attributes it to Rene Baire in 1899, and labels it
`已验证`. Under rev-5.6, that label is untrusted catalog metadata rather than source, statement,
or proof evidence.

The wording identifies the classical theorem family but does not fix one proposition. In
particular, "of second category" can mean that the whole space is not meagre in itself, while the
standard Baire-space formulation says every countable intersection of dense open sets is dense,
equivalently that every nonempty open set is nonmeagre. The literal nonmeagreness statement needs
a nonempty-space boundary: the empty complete metric space is meagre. The catalog also leaves open
whether its metric is separated or pseudometric, whether a displayed metric or only a completely
metrizable topology is part of the data, and which equivalent category formulation is canonical.

Pinned mathlib contains the exact-topic interface
`BaireSpace.of_completelyPseudoMetrizable`, together with `BaireSpace.baire_property`,
`dense_iInter_of_isOpen_nat`, `not_isMeagre_of_isOpen`, and `IsMeagre`.
`IntakeProbe.lean` authenticates these interfaces and their empty-space behavior. They are strong
formal candidates, but no source-identical target or checked transport is selected at intake.

The provisional vector is `[H1, M3, R4]`: the recognizable classical result lacks an admitted
pinpoint primary statement and reviewed clause map; usable pinned formal interfaces exist without
a canonical target; and no source-faithful readable proof has been reconstructed. `instance.json`
is the structured scope authority, `task-dag.json` keeps all downstream phases open, and the
provisional receipt claims only a self-tested intake. No exact statement, H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
