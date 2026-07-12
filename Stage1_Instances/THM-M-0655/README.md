# THM-M-0655 rev-5.6 intake

This directory is the fail-closed `planned` intake for the entry named "joint consistency theorem".
The repository gives only "the compatibility of the union of theories". Read literally as
"separately consistent theories have a consistent union", that phrase is false: `{P}` and `{not
P}` are separately satisfiable but their union is not.

The leading identification is therefore the Robinson joint consistency theorem: absence of
opposed consequences expressible in the common language permits joint satisfiability after both
theories are translated into a union language. That identification is a candidate, not a frozen
source statement. Primary-source inspection must also determine whether this entry intentionally
duplicates or distinguishes the adjacent `THM-M-0654` Robinson consistency entry.

The scope map and crosswalk preserve this ambiguity instead of selecting an easy union lemma. The
root remains `[H1, M4, R4]`; there is no exact Lean target, accepted proof state, audit completion,
or theorem completion. `validation.md` records the intake self-tests and `task-dag.json` leaves all
downstream phases open.
