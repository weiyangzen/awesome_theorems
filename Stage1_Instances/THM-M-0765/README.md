# THM-M-0765 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`图灵机可识别语言` (Turing-machine-recognizable languages). The catalog supplies only the gloss
`递归可枚举语言` (recursively enumerable languages), an attribution to Alan Turing, and the year
1936. Those data identify a computability and formal-language concept family, but not one stable
truth-valued proposition.

Plausible readings include a definition of recognizable languages, an equivalence between
Turing recognition and recursive enumerability, an equivalence with the domain of a partial
computable function, or an enumerator/range characterization. The record fixes neither a language
alphabet and word encoding nor a Turing-machine model, acceptance semantics, enumerator contract,
quantifier order, hypotheses, conclusion, or equivalence direction. Selecting one familiar result
would substitute mathematics not supplied by the source.

The provisional catalog-target vector is `[H5, M4, R4]`. Here `H5` classifies the received wording
as not yet a stable proposition; it does not refute standard characterization theorems about
recognizable or recursively enumerable languages. `IntakeProbe.lean` checks only adjacent pinned
partial-recursive and Turing-machine interfaces. In particular, pinned mathlib's `REPred` chooses
one predicate-level definition and its `PartrecToTM2` development proves a computation simulation,
but neither is credited as the unidentified catalog root.

`instance.json` is the structured scope authority. The scope map and source-statement crosswalk
freeze the unresolved choices and exclusions, while `task-dag.json` leaves all six downstream
phases open. This is a self-tested worker proposal only. No canonical statement, source proof,
formal proof body, H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
