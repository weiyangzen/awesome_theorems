# THM-M-0724 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"PSPACE completeness". The source inventory supplies only the phrase "PSPACE-complete problems",
a collective attribution, and the period "1970s". It does not name a decision problem or state a
theorem.

Completeness is not a property of PSPACE alone: it is a property of a particular language relative
to a specified reduction and encoding. Plausible readings include the theorem that TQBF is
PSPACE-complete, the analogous result for another problem, or the existential claim that PSPACE has
complete languages. Those claims are not interchangeable. Selecting one without an exact source
would substitute invented mathematics for the repository record.

The intake therefore freezes this ambiguity, the required scope decisions, and an open downstream
task DAG. The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib exposes formal
languages, Turing machines, polynomial-time machines, and computable many-one reductions. The
bounded search found no general space-complexity or PSPACE interface. The probe is encoding and
blocker evidence only; it is not a theorem statement or proof.

Exact commands and results are recorded in `validation.md`. No H0, M0, R0, audit completion, or
theorem completion is claimed.
