# Source-statement crosswalk

## Repository source

The source record is `Docs/researches/math_theorems.md` under “理想类群有限性”. It states
`数域的理想类群有限` (“the ideal class group of a number field is finite”), attributes the item
to Richard Dedekind (1871), and labels it `已验证`. The theorem manifest repeats the name,
category, and label but expressly marks the label untrusted. This is sufficient to identify the
human claim, not to establish source fidelity or proof status.

## Crosswalk

| Source phrase | Frozen meaning | Intended Lean object | Disposition |
|---|---|---|---|
| `数域` | arbitrary finite extension `K/Q` | `[Field K] [NumberField K]` | included |
| `理想类群` | fractional ideals of `O_K` modulo principal ideals | `ClassGroup (NumberField.RingOfIntegers K)` | exact namespace/type to elaborate next |
| `有限` | finite underlying type | `Finite (...)` | canonical conclusion |
| `已验证` | untrusted source metadata | none | no H/M/R credit |
| Dedekind, 1871 | historical attribution without edition/page | none | discovery only; requires source audit |

## Lean discovery boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_070.lean` proposes the same normalization and
names `NumberField.RingOfIntegers.instFintypeClassGroup` from
`Mathlib.NumberTheory.NumberField.ClassNumber`. Those paths are useful candidates for the
statement and anchor-audit phases. The legacy file predates rev-5.6 acceptance and is not an
immutable receipt; this intake neither replays it nor credits its proof.

Before `H0`, the source audit must select a stable mathematical edition, record theorem/page and
the definitions of the class group, map every assumption and conclusion, inspect relevant errata,
and obtain node-specific review. Before machine credit, the statement phase must elaborate the
exact normalization against the pinned environment and check any `Fintype`-to-`Finite` transport.
