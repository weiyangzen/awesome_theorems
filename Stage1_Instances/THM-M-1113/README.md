# THM-M-1113 rev-5.6 intake

This directory is the `planned` intake for the phase transition in the
Erdos-Renyi random graph. The intended human claim is the component-size
transition of `G(n,p)` in the sparse window `p` of order `1/n`: below the
critical value all components are small, while above it a unique component
has linear order. The critical-window law and exact probability modes remain
deliberately open for the statement phase.

The repository source supplies only the Chinese label, the broad phrase
"phase transition in random graphs", the year 1960, and an untrusted
"verified" tag. It is not an exact theorem statement and gives no proof
credit. No legacy Lean module for this target was found. The provisional root
vector is `[H2, M4, R4]`; no canonical Lean expression, audit completion, or
theorem completion is claimed.

`scope-map.md` records the boundary decisions, `source-statement-crosswalk.md`
maps the source phrase to the intended claim without inventing precision, and
`task-dag.json` keeps every downstream phase open. Intake validation evidence
is in `validation.md`.
