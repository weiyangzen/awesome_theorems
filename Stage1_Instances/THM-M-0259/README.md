# THM-M-0259 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`麦克马伦定理` (`McMullen theorem`). The repository attributes it to Curtis McMullen, dates it
to 1994, and gives only the gloss `有理函数的Julia集` (`Julia sets of rational functions/maps`).
That wording names a subject, not a truth-valued proposition with ordered binders, hypotheses, and
a conclusion. The catalog status `已验证` is untrusted metadata under rev-5.6.

The ambiguity changes the theorem. McMullen's 1994 survey discusses many inequivalent statements
about rational maps and Julia sets, including conjectures, results attributed to other authors, and
McMullen's no-invariant-line-field result for infinitely renormalizable real quadratic
polynomials. The catalog gives no source, theorem locator, map class, Julia-set definition,
conclusion, or boundary convention, so choosing any familiar result would substitute missing
mathematics.

The repository also schedules `THM-M-1435`, whose English title and all five remaining catalog
fields are semantically identical. The two IDs remain separate roots in the authoritative
1546-target set. This intake neither merges them nor borrows statement, source, status, receipt, or
proof credit from the other target; a master-level target-set correction is required to resolve the
collision.

The provisional root vector is `[H5, M4, R4]`. Here `H5` says that the received catalog wording is
not yet a stable proposition, not that a reviewed theorem by McMullen is false or open. The
structured scope authority is `instance.json`; `scope-map.md` records the proposition-changing
choices and exclusions; `source-statement-crosswalk.md` maps the literal record to the unresolved
source and Lean components. All six downstream phases remain open in `task-dag.json`.
`IntakeProbe.lean` checks only adjacent pinned APIs and states no target theorem. No H0, M0, R0,
accepted proof state, audit completion, theorem completion, duplicate resolution, or master
acceptance is claimed.
