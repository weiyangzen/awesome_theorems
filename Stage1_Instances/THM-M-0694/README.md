# THM-M-0694 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "natural
deduction". The source inventory calls it a natural-style proof system and separately describes
paired introduction/elimination rules and tree-shaped proofs. Those descriptions define a topic,
not a theorem.

Natural deduction varies materially with the object language and rule set. A later target might be
soundness, completeness, normalization, admissibility, equivalence with another calculus, or a
particular derivability judgment. Choosing one now would substitute invented mathematics for the
source target.

The intake therefore freezes the ambiguity and exclusion boundary rather than a proposition. The
root remains `[H3, M4, R4]`. A pinned Lean probe confirms that core proposition constructors and
eliminators needed to illustrate natural-deduction rules elaborate; it is neither a formalized
object calculus nor a theorem statement or proof. Exact commands and results are in
`validation.md`.
