# THM-M-0910 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Caucal定理`
(Caucal theorem). The catalog supplies Didier Caucal, the year 1996, and only the gloss
`图的可判定性` (graph decidability). Stage0 explicitly leaves the exact definitions, premises,
source, equivalent formulations, and formal artifacts open. The label `已验证` is untrusted
metadata and supplies no human-source or kernel-proof credit.

The matching source-family lead is Didier Caucal's 1996 ICALP paper *On Infinite Transition
Graphs Having a Decidable Monadic Theory*. An inspected IRISA-hosted expanded manuscript defines several
related graph classes and contains multiple distinct results: preservation of monadic-theory
decidability under rational restriction and inverse rational substitution, decidability for the
class `REC_Rat`, effective representative results, and consequences for rationally restricted
right closures of recognizable word graphs, pushdown graphs, and regular graphs. The catalog does
not cite the paper or select one of those propositions.

Material scope is therefore unresolved: the graph representation and labels; the graph family;
monadic second-order syntax and semantics; the effective presentation of formulas, graphs, and
rational languages; per-graph versus uniform decidability; reduction versus decision procedure;
and the intended theorem or corollary. Reading the gloss as a statement about all graphs would be
false, while choosing familiar Corollary 2.8 or 3.7 would substitute missing mathematics.

`IntakeProbe.lean` checks only adjacent pinned mathlib interfaces for first-order simple-graph
structures, formula semantics, regular languages, finite automata, and computable predicates.
Mathlib's inspected model-theory API is first-order and does not supply Caucal's monadic
second-order graph language, graph family, effective reduction, or target theorem. The probe is an
intake feasibility observation, not a formal candidate or proof.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the received catalog gloss as not
one stable truth-valued proposition; it does not refute Caucal's published results. The canonical
human and Lean statements remain null, all six downstream tasks remain open, and no H0, M0, R0,
accepted state, audit completion, theorem completion, or master acceptance is claimed.
