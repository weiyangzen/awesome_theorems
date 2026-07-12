# THM-M-0676 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "prime models". The
source inventory supplies only the gloss "existence and uniqueness of prime models". Taken without
hypotheses, existence is not a valid general theorem: the theory, language, and a condition that
actually ensures a prime model are essential parts of the proposition. Uniqueness also needs a
fixed theory and a specified notion of isomorphism.

The intake therefore preserves a theorem family rather than silently choosing the standard
countable complete-theory/isolated-types criterion, the atomic-model characterization, or merely
conditional uniqueness of an already existing prime model. The provisional root vector is
`[H4, M4, R4]`. No exact source statement, Lean target, source-fidelity result, proof, audit
completion, or theorem completion is claimed.

`scope-map.md` records the proposition-changing choices, `source-statement-crosswalk.md` separates
the repository record from candidate textbook discovery anchors, and `task-dag.json` leaves all
downstream phases open. The self-test boundary and exact commands are recorded in `validation.md`.
