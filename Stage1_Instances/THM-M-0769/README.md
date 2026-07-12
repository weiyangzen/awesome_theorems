# THM-M-0769 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the axiom of choice. The repository
claim is: "every family of nonempty sets has a choice function." The dossier fixes its ordinary
indexed-family meaning while leaving universe levels, `Nonempty` versus explicit witnesses, and
the exact Lean declaration for the statement phase.

The claim is foundational rather than a theorem derivable in a choice-free base. Lean exposes
`Classical.choice` as an axiom and `Classical.axiomOfChoice` as its dependent-family formulation. The bounded
Lean probe confirms these pinned APIs and the candidate proposition elaborate. It does not provide
proof credit or complete the statement, anchor-audit, proof, validation, or release phases.

The intake root remains `[H2, M3, R4]`: the repository wording has a clear mathematical reading and
a primary historical source is located, but edition/page/translation and exact proposition review
remain open. Exact commands and results are recorded in `validation.md`.
