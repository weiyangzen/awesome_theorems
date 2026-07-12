# THM-M-0774 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label
"Kuratowski-Zorn lemma". The repository's entire mathematical wording is "existence of a maximal
element in a partially ordered set". That wording omits the essential chain-upper-bound hypothesis
and does not say whether the intended result concerns the whole poset or a nonempty subset.

The provisional human scope is the standard Zorn form: a nonempty partially ordered type has a
maximal element when every chain has an upper bound. This is not yet an exact source statement.
Historical attribution and the repository's date `1922` must be checked against a primary edition;
the statement phase must not manufacture the missing quantifiers from the theorem name alone.

Pinned mathlib contains a strong candidate declaration, `zorn_le`, but this intake gives it no
statement or proof credit. The provisional root vector is `[H3, M4, R4]`. No canonical Lean target,
source fidelity, audit completion, or theorem completion is claimed. The scope map, source
crosswalk, open task DAG, and validation record define the boundary of this intake.
