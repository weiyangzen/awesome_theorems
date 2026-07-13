# THM-M-0634 rev-5.6 intake

This directory is the self-tested `planned` intake dossier for `介值定理` (the intermediate
value theorem). The repository catalog supplies Bernard Bolzano, the year 1817, and only the
gloss `连通空间上连续函数的值域` ("the range of a continuous function on a connected
space"). It does not give a citation, an ordered codomain, binders, hypotheses, or a conclusion.
The catalog label `已验证` is untrusted metadata and supplies no source or proof credit.

The title and attribution point toward the ordered intermediate-value theorem, but the literal
gloss also fits the separate theorem that a continuous image of a connected set is connected.
Even within the ordered family, it does not choose a set or whole-space formulation, connected
versus preconnected domain, endpoint orientation, closed-interval specialization, or zero/root
corollary. Intake therefore preserves the family and ambiguity rather than inventing one exact
proposition.

The structured authority is `instance.json`. `scope-map.md` freezes proposition-changing choices
and neighboring-target boundaries. `source-statement-crosswalk.md` maps the complete repository
record to the candidate mathematical and Lean components. `task-dag.json` leaves all six dependent
phases open.

`IntakeProbe.lean` checks only adjacent declarations in the pinned mathlib snapshot. Its successful
elaboration proves that those interfaces are present; it does not select the canonical target,
perform the scheduled anchor audit, or provide proof credit. Exact commands and results are in
`validation.md`, and `intake-receipt.json` is an unsigned provisional worker receipt.

The provisional root vector is `[H1, M4, R4]`: a published classical theorem family is known but
not source-audited, no usable source-identical formal root is credited while the proposition is
unresolved, and no source-faithful proof reconstruction is accepted. No H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
