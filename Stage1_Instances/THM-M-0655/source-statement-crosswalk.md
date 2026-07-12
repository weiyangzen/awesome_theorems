# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` provide the Chinese title
`联合一致性定理`, date it only to the twentieth century, attribute it to "many mathematicians", and
gloss it as `理论联合的相容性` (compatibility of the union of theories). They provide no theorem
statement, proof, bibliography, definitions, or assumptions. The generated `已验证` status is
untrusted metadata and gives no human-source or machine-proof credit.

The literal gloss is insufficient to select a true proposition. Separate satisfiability does not
survive arbitrary union: in a language with a nullary predicate `P`, the theories `{P}` and `{not
P}` are separately satisfiable and have an unsatisfiable union. A compatibility condition must be
sourced, not invented.

## Candidate human source

Abraham Robinson, "A result on consistency and its application to the theory of definition",
*Proceedings of the Royal Netherlands Academy of Arts and Sciences, Series A* 59 / *Indagationes
Mathematicae* 18 (1956), 47-58, is the leading historical source candidate for the Robinson joint
consistency result. The bibliographic locator is discovery evidence only. This intake has not
inspected an immutable scan, located the exact result and page, transcribed incorporated
definitions, checked corrections or errata, or reconciled its terminology with the separate
`THM-M-0654` entry. It therefore does not establish `H0`.

## Provisional crosswalk

| Repository phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| theories | first-order theories, potentially over different overlapping signatures | `Theory` objects plus explicit language maps | candidate; domains open |
| union | union after translation into a common union signature | sentence translation and `Set.union` | encoding open |
| compatibility | absence of a common-language sentence entailed on one side and refuted on the other | semantic consequence or derivability over the intersection language | candidate; exact polarity open |
| consistency | existence of a nonempty model, or syntactic non-derivability of contradiction | `IsSatisfiable` or a fixed proof calculus with a checked bridge | convention open |
| joint conclusion | one model satisfying both translated theories | satisfiability of the translated union | candidate |

## Pinned Lean discovery boundary

The pinned mathlib snapshot contains general first-order semantics and satisfiability APIs in
`Mathlib.ModelTheory.Semantics` and `Mathlib.ModelTheory.Satisfiability`. A scoped repository search
found `Theory.isSatisfiable_directed_union_iff`, but that is a directed-union theorem and is not the
Robinson joint consistency claim. No exact declaration has been identified. This is incomplete
discovery evidence, not an anchor audit or `M`-axis proof credit.

Before the statement gate, a source reviewer must select and inspect an immutable primary or
critical edition, record exact theorem/page and every incorporated definition and assumption,
resolve the relation to `THM-M-0654`, audit errata, and approve a row-by-row mapping. Only then may
the formal reviewer freeze language transports, binder order, exact Lean expression, alternate
encodings, and structural mutations.
