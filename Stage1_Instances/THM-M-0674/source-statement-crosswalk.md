# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records only the twentieth-century label, the sentence
"existence of saturated models", importance `high`, and an untrusted `verified` status. It gives no
author, publication, theorem number, page, hypotheses, proof, or formal-project anchor. Thus it is
not H0 evidence and cannot determine a unique proposition.

## Primary-source candidates

- C. C. Chang and H. J. Keisler, *Model Theory*, saturation chapter. This is a candidate standard
  reference for elementary extensions and prescribed-cardinality variants; exact edition,
  theorem/page, wording, assumptions, and errata have not yet been inspected.
- Wilfrid Hodges, *Model Theory*, saturation chapter. This is a candidate independent modern
  reference, not yet an accepted source anchor.

These bibliographic leads are discovery anchors only. The statement phase must inspect a stable
edition and record theorem/page and definitions before assigning H0/H1.

## Crosswalk

| Source component | Required mathematical decision | Required Lean component | Intake status |
|---|---|---|---|
| "model" | model of `T` or elementary extension of `M` | `FirstOrder.Language.Structure`, `⊨`, elementary embedding | family included; choice open |
| "saturated" | parameter-set and tuple-arity convention | complete types over named parameters and realization | convention open |
| "existence" | output size and relation to input | existential carrier/package, perhaps embedding | exact output open |
| cardinal hypotheses | language bound, regularity, power closure | `Cardinal` inequalities/equalities | source-dependent |
| theory hypotheses | satisfiable or complete theory | `Theory.IsSatisfiable` / `Theory.IsComplete` | source-dependent |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_300.lean` elaborates a historical candidate with
`SaturatedModelExistenceHypotheses`, `IsKappaTupleSaturatedAt`, `SaturatedModelPackage`, and
`StatementShape`. Its own documentation says no terminal theorem was found, and its application
lemma assumes `StatementShape`. This is useful API discovery but neither source fidelity nor root
closure. It must be re-audited after the exact source statement is frozen.

