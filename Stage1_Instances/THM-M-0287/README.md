# THM-M-0287 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0287`, the catalog item
`卢津定理` (Lusin's theorem). The repository attributes it to Nikolai Luzin in 1912 but supplies
only the gloss `可测函数与连续函数的关系`, literally "the relationship between measurable functions
and continuous functions." Its `已验证` label is untrusted metadata under rev-5.6.

Lusin's 1912 note *Sur les proprietes des fonctions mesurables* is a strong primary-source lead.
Printed page 1689 states an interval theorem: for a measurable function on `[0,1]` and arbitrarily
small positive epsilon, there is a perfect nowhere-dense set of measure greater than `1 - epsilon`
on which the function is relatively continuous. The same note also states distinct polynomial-
series and almost-everywhere primitive theorems. The repository does not cite the note or say
whether the intended root is that interval result, a modern finite Radon-measure generalization, a
large closed/compact restriction, or a global continuous function agreeing off a small set.

Those forms differ in domains, measures, codomains, regularity hypotheses, binder order, and exact
conclusions. Selecting one at intake would substitute proposition-changing mathematics. The
canonical mathematical and Lean statements therefore remain null. `IntakeProbe.lean` checks only
adjacent pinned measurability, continuity, and compact-regularity APIs; none proves this target.

The provisional vector is `[H1, M4, R4]`: a matching primary source and exact theorem passage were
inspected, but source identity, assumptions, translation, corrections, and independent review are
open; no usable exact formal artifact is credited; and no readable proof reconstruction binds to a
frozen root. All six downstream phases remain open. No H0, M0, R0, accepted execution state, audit
completion, theorem completion, accepted receipt, or master acceptance is claimed.
