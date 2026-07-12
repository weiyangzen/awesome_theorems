# THM-M-1332 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Picard-Lindelof theorem. The
repository catalog gives only the title, the attribution to Emile Picard and Ernst Lindelof, the
year 1894, and the gloss "existence and uniqueness of ODE solutions." That identifies a classical
theorem family, but it does not fix a truth-valued proposition with ordered binders, hypotheses,
an interval, a solution predicate, and a uniqueness boundary.

Pinned mathlib contains a module explicitly named for Picard-Lindelof. Its main theorems establish
existence for time-dependent vector fields on complete normed real vector spaces under a bundled
quantitative hypothesis. The same module explicitly delegates uniqueness to separate Gronwall
theorems. Those declarations are strong formal discovery anchors, but no single inspected
declaration is the catalog's unspecified existence-and-uniqueness root. Selecting or composing
them before the source and statement gates would decide missing mathematics rather than crosswalk
it.

The intake therefore freezes the recognizable family, proposition-changing choices, source gaps,
neighboring-target exclusions, and formal leads while leaving the canonical statement and Lean
target null. The provisional vector is `[H1, M3, R3]`: the historically proved theorem family is
recognizable but its exact primary-source mapping is unaudited; pinned exact-family statement and
proof interfaces exist but root identity, composition, provenance, and trust are open; and this
dossier explains the boundary but reconstructs no proof.

`instance.json` is the structured scope authority. `scope-map.md` records the candidate boundary
and exclusions, `source-statement-crosswalk.md` maps the catalog and formal leads, and
`task-dag.json` leaves all six downstream phases open. `validation.md` and
`intake-receipt.json` record the bounded worker checks. No canonical statement, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
