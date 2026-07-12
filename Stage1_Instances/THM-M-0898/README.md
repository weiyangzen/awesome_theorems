# THM-M-0898 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0898`, the repository label
`Kirkman女学生问题` (Kirkman's schoolgirl problem). The catalog attributes the target to Thomas
Kirkman in 1850 but supplies only the gloss `Steiner三元系的存在性` (existence of Steiner triple
systems), no citation, and an untrusted `已验证` status.

The name and gloss do not identify the same exact proposition. The named schoolgirl problem is the
15-point scheduling/construction problem: partition fifteen girls into five triples on each of
seven days so that each unordered pair occurs together exactly once. In design terminology this is
a resolvable Steiner triple system of order 15, often called a Kirkman triple system. The catalog
gloss could instead mean existence of an ordinary Steiner triple system of a fixed unspecified
order or the general admissible-order theorem. Resolvability, order 15, and a seven-class resolution
are substantive requirements, not harmless notation.

This intake preserves that conflict rather than selecting a convenient theorem. `instance.json`
therefore leaves the canonical mathematical and Lean statements null and records `[H5, M4, R4]`:
the catalog wording is not yet one stable truth-valued proposition, no source-identical Lean target
is available, and no readable proof reconstruction exists. `IntakeProbe.lean` elaborates only
generic pinned finite-set, fixed-cardinality-subset, disjointness, and congruence interfaces. It
provides no statement or proof credit.

All six downstream tasks remain open in `task-dag.json`. No canonical statement, H0, M0, R0,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
