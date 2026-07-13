# THM-M-0204 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0204`, the catalog item
`斯图尔特定理` (Stewart's theorem). The repository supplies only Matthew Stewart, the year 1746,
the gloss `三角形中线长度公式` (triangle median-length formula), and an untrusted `已验证` label.
Those fields identify a classical Euclidean-geometry family, but they do not state one exact
proposition or supply human-source or kernel evidence.

There is a material scope mismatch. Stewart's theorem conventionally denotes a general cevian
identity, whereas the received gloss names only its midpoint/median specialization, also known as
Apollonius's theorem. Pinned mathlib contains both
`EuclideanGeometry.dist_sq_mul_dist_add_dist_sq_mul_dist`, explicitly documented as Stewart's
theorem, and `EuclideanGeometry.dist_sq_add_dist_sq_eq_two_mul_dist_midpoint_sq_add_half_dist_sq`,
explicitly documented as Apollonius's theorem. Intake does not broaden the gloss to the general
cevian identity or substitute the convenient midpoint declaration.

The provisional vector is `[H1, M3, R4]`. `H1` records a historically established theorem family
whose exact source statement and catalog-to-source mapping remain unaudited. `M3` records direct
pinned formal interfaces while the source-selected canonical target and transports remain null.
`R4` records that no accepted source-faithful reconstruction can attach to an unfrozen root.
`IntakeProbe.lean` authenticates only the two candidates and adjacent angle/midpoint APIs.

`instance.json` is the structured scope authority. `scope-map.md` freezes every proposition-changing
choice, `source-statement-crosswalk.md` records the unresolved source and candidate mapping, and
`task-dag.json` leaves all six downstream phases open. This is a self-tested worker proposal only.
No exact statement, accepted proof state, H0, M0, R0, audit completion, theorem completion, or
master acceptance is claimed.
