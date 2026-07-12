# THM-M-0788 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "large
cardinal axioms". The only source wording is "inaccessible cardinals, measurable cardinals, and
other large cardinals". That is a family of definitions and additional existence hypotheses, not
one theorem with fixed binders, assumptions, and conclusion.

The intake therefore freezes the ambiguity rather than silently choosing an existence axiom, a
consistency-strength comparison, or a consequence of such an axiom. It also separates ordinary
set-theoretic inaccessible cardinals from Lean universe cardinals: pinned mathlib defines
`Cardinal.IsInaccessible`, and proves `Cardinal.IsInaccessible.univ`, but the latter reflects
Lean's universe hierarchy and is not evidence that ZFC proves an inaccessible cardinal exists.

The root remains `[H5, M4, R4]`: as currently worded the target is not a stable proposition. A
pinned Lean probe checks only the available inaccessible-cardinal vocabulary. It supplies neither
a canonical target nor proof credit. Exact commands and results are recorded in `validation.md`.
