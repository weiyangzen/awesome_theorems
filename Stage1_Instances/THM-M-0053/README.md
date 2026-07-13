# THM-M-0053 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry `盖尔圆盘定理`
(Gershgorin circle theorem). The repository attributes it to Semyon Gershgorin in 1931 and gives
only the gloss `矩阵特征值的定位定理` (a localization theorem for matrix eigenvalues). Its
`已验证` label is untrusted inventory metadata, not a source audit, exact proposition, or proof
receipt.

The label identifies the classical Gershgorin family, but the gloss does not fix complex versus
more general normed-field matrices, the finite index type and empty-dimension convention, row
versus column discs, the eigenvalue encoding, or whether the target is only spectral inclusion or
also the stronger connected-component eigenvalue-count result. Intake does not silently choose
among these proposition-changing clauses.

An inspected secondary source lead, Richard S. Varga's revision 56196 of the *Encyclopedia of
Mathematics* entry, gives the standard complex row-disc inclusion and a proof, and identifies
Gerschgorin's 1931 paper, pages 749-754. The original paper, its exact theorem boundary, correction
history, and an independent source review have not been admitted. This remains an `H1` lead rather
than `H0` evidence.

Pinned mathlib contains the direct exact-topic candidate `eigenvalue_mem_ball` in
`Mathlib.LinearAlgebra.Matrix.Gershgorin`. It proves a generalized row-ball statement for square
matrices over a normed field. `IntakeProbe.lean` authenticates its interface and reports its direct
axioms. That is useful `M3` statement/interface evidence, but the canonical root, source transport,
terminal-body provenance, transitive trust closure, and wrapper have not passed later gates, so no
`M0-W` proof credit is claimed.

The provisional vector is `[H1, M3, R4]`: the human theorem and proof lead are not yet admitted at
pinpoint primary-source fidelity; a direct pinned formal interface exists without an approved
canonical target or proof credit; and no source-faithful readable reconstruction is accepted.
`instance.json` is the structured scope authority and `task-dag.json` keeps all six downstream
phases open. No H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
