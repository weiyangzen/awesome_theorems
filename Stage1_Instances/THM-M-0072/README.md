# THM-M-0072 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0072`, catalogued as the
Thompson transfer lemma. The repository gives only the gloss "about the relation between local and
global properties of groups," attributes the item to John Thompson in 1964, and labels it verified.
It supplies no formula, citation, definition, binder, hypothesis, conclusion, or proof boundary.
Under rev-5.6 the label is untrusted inventory metadata and grants no source or machine credit.

A precise eponym lead was located. Justin Lynd's versioned paper *The Thompson-Lyons transfer lemma
for fusion systems* identifies the classical Thompson transfer lemma as Lemma 5.38 in Thompson's
1968 paper *Nonsolvable finite groups all of whose local subgroups are solvable*. The original
Lemma 5.38(a)(i), printed page 411, says that if a finite group has even order and no subgroup of
index two, then, for a Sylow 2-subgroup and a maximal subgroup of it, every involution of the Sylow
subgroup has a conjugate in that maximal subgroup. The source also gives a short transfer proof.

This is a strong source-statement lead, not an accepted canonical claim. The catalog does not cite
the paper and says 1964 rather than 1968. Lynd's common nontrivial formulation assumes the
involution lies outside the maximal subgroup, while Thompson's printed clause quantifies over every
involution. The complete role of the surrounding parts (a)(ii) and (b), incorporated definitions,
errata, preservation, translation, and independent source review remain open. Intake therefore
does not silently choose between the exact printed clause and the restricted modern formulation.

Pinned mathlib supplies Sylow subgroups, subgroup index and maximality, element order and conjugacy,
the transfer homomorphism, Burnside's normal-complement result, and the focal subgroup theorem.
`IntakeProbe.lean` authenticates those interfaces. A bounded search found no declaration named for
Thompson and no 2-perfect-group predicate or exact conjugacy conclusion. Burnside's normal
`p`-complement theorem and the focal subgroup theorem are adjacent transfer results, not substitutes.

The provisional vector is `[H1, M3, R4]`: a primary proof passage and a precise eponym crosswalk are
known but source identity and assumptions are not independently accepted; direct formal statement
and proof substrate exists without a frozen canonical target; and there is no source-faithful
readable proof reconstruction. `instance.json` is the structured scope authority, and
`task-dag.json` keeps all six downstream phases open. No canonical Lean statement, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
