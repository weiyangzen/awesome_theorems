# THM-M-0020 rev-5.6 intake

`THM-M-0020` is the catalog item `哈塞-闵可夫斯基定理` (Hasse-Minkowski theorem). The
repository attributes it to Helmut Hasse and Hermann Minkowski in 1924 and supplies only the gloss
"local-global principle for quadratic forms" (`二次型的局部-整体原理`) plus an untrusted
`已验证` label. This identifies a classical theorem family, not a binder-complete proposition.

## Intake result

This directory is a fail-closed `planned` dossier. It preserves the classical local-global
quadratic-form family without silently choosing among materially different roots: isotropy of one
form, representation of a scalar, equivalence or classification of two forms, a rational-field
specialization, or a number-field theorem. Even within the isotropy reading, the catalog does not
fix finite dimension, regularity/nondegeneracy, coordinate conventions, the zero-witness rule, the
set of places, or whether the result is an equivalence or only its hard local-to-global direction.

Hasse's 1924 number-field paper and Minkowski's 1890 rational-field precursor are credible source
leads. Their bibliographic metadata has been confirmed, but no immutable primary text, pinpoint
theorem, complete premise map, translation, errata audit, or independent review has been admitted.
They therefore support `H1`, not `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned APIs for quadratic forms, anisotropy,
nondegeneracy, scalar extension, and number-field places. A bounded search found no terminal
Hasse-Minkowski declaration in pinned mathlib. The repository also contains statement-only and
substrate material under `THM-M-0423`, the broader Hasse-principle target. That material is useful
duplicate-scope discovery but belongs to another target and contributes no accepted statement or
proof evidence here.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: the theorem family and historical sources are known, no exact source-faithful root
or usable formal closure is accepted, and no proof reconstruction can attach to an unfrozen root.
All six downstream tasks remain open. No accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
