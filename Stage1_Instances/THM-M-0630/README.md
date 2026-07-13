# THM-M-0630 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Stone-Cech
compactification. The repository catalog gives only the gloss `完全正则空间的最大紧化`
("the greatest compactification of a completely regular space"), attributes it to Marshall Stone
and Edward Cech in 1937, and labels it `已验证`. Under rev-5.6 that label is untrusted discovery
metadata, not source or kernel evidence.

The gloss identifies the classical Stone-Cech family but not one binder-complete proposition. It
does not say whether complete regularity includes a separation axiom, define a compactification,
specify compact Hausdorff competitors, orient the compactification order behind "greatest", or
state whether the factor map must be unique. These choices affect the theorem. In particular,
pinned mathlib's `CompletelyRegularSpace` omits T0/T1 separation; its Stone-Cech unit is inducing
under that assumption but becomes a dense embedding only under `T35Space`.

A bounded inspection of Stone's 1937 paper located Definition 21 and Theorems 78, 79, and 88 as a
strong primary-source family lead. They construct a bicompact Hausdorff extension of a CR-space,
extend bounded continuous real functions, and show every competing bicompact Hausdorff extension
is its continuous image. Complete historical-definition translation, proof-boundary and errata
review, reconciliation with Cech's 1937 paper, and independent review remain open.

`IntakeProbe.lean` authenticates the pinned Stone-Cech construction, universal property,
complete-regularity interface, dense-embedding interface, and categorical hom-set equivalence. It
does not select the source-identical root or prove `THM-M-0630`. The provisional root vector is
`[H1, M3, R4]`: a published source family and usable pinned formal interfaces are known, but no
exact source statement, checked source-to-Lean transport, or readable proof reconstruction is
accepted. All six downstream phases remain open in `task-dag.json`.

No canonical mathematical or Lean proposition, H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
