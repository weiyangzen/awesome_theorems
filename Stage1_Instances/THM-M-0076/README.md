# THM-M-0076 intake dossier

This directory is the fail-closed `planned` intake dossier for `THM-M-0076`, the catalog item
`布劳尔特征标定理` (Brauer character theorem). The received claim is only:

> Properties of characters in modular representation theory.

That gloss names a subject, not a proposition. It does not select a theorem about constructing
Brauer characters, their restriction to prime-regular elements, irreducibility, decomposition
numbers, blocks, lifting, or a relation with ordinary characters. It also does not fix a finite
group, prime, modular system, coefficient fields, representation category, character codomain,
binders, hypotheses, or conclusion. Intake therefore preserves the named family while leaving the
canonical mathematical statement and Lean target unset.

The repository attribution (`Richard Brauer`, `1956`) is not accompanied by a citation. Bounded
bibliographic discovery found relevant Brauer and Brauer-Nesbitt modular-character papers from
1941, not an exact 1956 source matching the catalog. These are source leads only. Pinned mathlib
provides ordinary representation characters, while its `ModularCharacter` API is the unrelated
Haar-measure homomorphism of locally compact groups. The discovery probe authenticates that formal
boundary; it declares no target and earns no proof credit.

The structured scope authority is [instance.json](instance.json). Proposition-changing decisions
and exclusions are in [scope-map.md](scope-map.md), the repository/source/formal mapping is in
[source-statement-crosswalk.md](source-statement-crosswalk.md), and every downstream phase remains
open in [task-dag.json](task-dag.json).

Status boundary: provisional, self-tested planned intake only. No exact source proposition,
canonical Lean target, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
