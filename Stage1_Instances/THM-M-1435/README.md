# THM-M-1435 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`McMullen定理` (`McMullen theorem`). The repository attributes it to Curtis McMullen, dates it
to 1994, and gives only the gloss `有理函数的Julia集` (`Julia sets of rational functions/maps`).
That wording names a subject, not a truth-valued proposition with ordered binders, hypotheses, and
a conclusion. The catalog status `已验证` is untrusted metadata under rev-5.6.

The ambiguity is material. A 1994 McMullen survey discusses many inequivalent statements about
rational maps and Julia sets, including conjectures, other authors' theorems, and McMullen's own
no-invariant-line-field result for infinitely renormalizable real quadratic polynomials. The
catalog gives no source, theorem locator, map class, Julia-set definition, conclusion, or boundary
conditions, so selecting any familiar result would substitute missing mathematics.

The repository also contains separately eligible target `THM-M-0259`, whose translated title and
all five remaining catalog fields are semantically identical. Exact-title deduplication left both
IDs in the authoritative 1546-target set. This intake neither merges the IDs nor borrows statement,
source, status, or proof credit from the other target; resolving the collision requires an
authoritative target-set correction.

This intake freezes those blockers. The provisional root vector is `[H5, M4, R4]`: `H5` says that
the received catalog wording is not yet a stable proposition, not that a reviewed McMullen theorem
is false or open. The structured authority is `instance.json`; `scope-map.md` records the permitted
boundary and prohibited substitutions; `source-statement-crosswalk.md` maps the literal record to
the unresolved source and Lean components. All six downstream phases remain open in
`task-dag.json`. `IntakeProbe.lean` checks only adjacent pinned APIs and states no target theorem.
No H0, M0, R0, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
