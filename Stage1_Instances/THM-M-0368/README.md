# THM-M-0368 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Hardy-Littlewood maximal
function weak-type estimate. The repository source identifies the theorem family, but it does not
give a formula, source edition, theorem number, dimension, centeredness convention, normalization,
function class, or constant. Those choices change the proposition, so none is silently selected.

The intended family is the weak `(1,1)` estimate
`measure {x | M f x > lambda} <= C / lambda * integral |f|`, normally over Euclidean space, but
this display is only a scope guide. It is not the frozen canonical claim. The root remains
`[H3, M4, R4]` until an exact source fixes every parameter and the statement phase elaborates it.

A narrow pinned Lean probe confirms that mathlib contains the relevant measure, ball, integral,
covering, and Vitali-family APIs. It does not assert a maximal-function definition or theorem.
Exact commands and results are recorded in `validation.md`.
