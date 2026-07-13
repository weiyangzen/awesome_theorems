# THM-M-0078 intake dossier

This directory is the fail-closed `planned` intake dossier for `THM-M-0078`, catalogued as
`扎森豪斯定理` (Zassenhaus theorem). The received claim is only:

> About the classification of group extensions.

That gloss names a subject, not a stable proposition. It does not say which extensions are
classified, which data are fixed, which equivalence relation is used, what invariant does the
classification, or what hypotheses and conclusion form the theorem. Intake therefore preserves
the literal family label while leaving the canonical mathematical statement and Lean target unset.

The uncited attribution `Hans Zassenhaus, 1937` does not resolve the identity. Bibliographic
metadata locates a 1937 Zassenhaus paper titled *Beweis eines Satzes ueber diskrete Gruppen*, not a
paper whose metadata identifies an extension-classification statement. A much later 1971
Johnson-Zassenhaus paper is titled *On equivalence of finite group extensions*. Neither source was
available here as primary text, and neither is admitted as the target. The name also collides with
the butterfly/Zassenhaus lemma and the Schur-Zassenhaus complement theorem; both are explicit
non-substitutions.

Pinned mathlib supplies group-extension structures, equivalences, sections, splittings, and split
extension facts. Its own module documentation leaves the abelian-kernel classification of extension
equivalence classes by second group cohomology as a TODO. `IntakeProbe.lean` authenticates this
interface and boundary only. It declares no target and earns no proof credit.

The structured scope authority is [instance.json](instance.json). Proposition-changing choices and
exclusions are in [scope-map.md](scope-map.md), repository/source/formal provenance is in
[source-statement-crosswalk.md](source-statement-crosswalk.md), and all six downstream phases remain
open in [task-dag.json](task-dag.json).

Status boundary: provisional, self-tested planned intake only. No stable proposition, exact source
statement, canonical Lean target, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
