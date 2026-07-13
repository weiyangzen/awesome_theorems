# THM-M-0633 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0633`, the catalog entry
named `一致连续性定理` (uniform continuity theorem). The repository gives only the gloss
`紧集上连续函数一致连续` (a continuous function on a compact set is uniformly continuous),
attributes it to many mathematicians in the nineteenth century, and labels it `已验证`. Under
rev-5.6 that label is untrusted metadata, not a source audit or a machine-proof claim.

The gloss identifies the classical Heine-Cantor theorem family and specifically mentions a compact
set. It does not fix the ambient and codomain structures, whether continuity and uniform
continuity are relative to a subset or are carried by the compact domain subtype, or which
uniformities are intended. It also supplies no primary citation, theorem/page locator, definition
chain, correction history, errata review, or independent source review. The canonical human
statement and canonical Lean expression therefore remain null at intake.

Pinned mathlib contains two direct Heine-Cantor interfaces in
`Mathlib.Topology.UniformSpace.HeineCantor`. The closest compact-subset candidate is
`IsCompact.uniformContinuousOn_of_continuous`; the compact-domain candidate is
`CompactSpace.uniformContinuous_of_continuous`. `IntakeProbe.lean` elaborates their exact types and
reports their axioms. This authenticates a strong formal candidate surface and supports provisional
`M3`, but it does not choose a source-identical root, freeze an expression fingerprint, audit the
terminal proof body, or grant proof credit.

The provisional root vector is `[H1, M3, R4]`: the classical theorem family is recognizable but no
exact human source is accepted; direct pinned formal interfaces exist but no canonical target is
frozen; and no source-faithful readable proof reconstruction is attached to an exact root. All six
downstream phases remain open. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
