# Source-statement crosswalk

## Repository evidence

The repository's only substantive anchors are `Docs/researches/math_theorems.md` and its generated
Stage0 projection. They give the Chinese title `谢拉赫分类定理`, attribution Saharon Shelah,
year 1990, and gloss `超稳定理论的分类`. They provide no bibliography, theorem number,
definitions, formal statement, hypotheses, proof, or formal artifact. Stage0 itself marks the exact
definitions, proof path, dependencies, axioms, and machine-checked artifact as missing.

Consequently, the generated `已验证` status is metadata only. It gives no `H`, `M`, or `R` credit.

## Bibliographic discovery lead

Saharon Shelah, *Classification Theory and the Number of Nonisomorphic Models*, second edition,
North-Holland, 1990, is consistent with the author, subject, and year metadata and is a natural
discovery lead. It is not yet an accepted pinpoint source. This intake did not select a theorem
number/page, verify an immutable edition, transcribe definitions, audit corrections or errata, or
obtain independent review. The book title cannot turn the broad repository gloss into one theorem.

## Provisional crosswalk

| Repository component | Source information required | Eventual Lean component | Intake status |
|---|---|---|---|
| Shelah classification theorem | Exact source theorem and locator | One named declaration or serialized exact proposition | unidentified |
| superstable theory | Language, completeness, and exact definition | language, `Theory`, and a sourced superstability predicate | definition open |
| classification | Classified objects and equivalence relation | model/decomposition objects plus equality, equivalence, or isomorphism target | meaning open |
| hypotheses | Cardinal, dividing-line, depth, and set-theoretic assumptions | ordered explicit binders and hypotheses | absent from repository |
| conclusion | Exact existence, uniqueness, decomposition, dichotomy, or spectrum assertion | exact `Prop` with checked boundary behavior | absent from repository |
| 1990 / Shelah | Edition-level bibliographic identity | source-revision record only | discovery hint |
| verified | Cited human proof or machine artifact | kernel declaration plus provenance and trust closure | unsupported |

## Lean discovery boundary

The repository's pinned environment runs Lean 4.29.0 and contains mathlib model-theory
infrastructure, but no exact expression is eligible for elaboration until the source claim is
fixed. A text search for the English family terms is not a formal-candidate audit and found no basis
for selecting a terminal declaration. This intake therefore records `M4`, not an anchor or proof.

The next phase must inspect and pin a primary or authoritative critical edition, identify the exact
theorem/page and incorporated definitions, check assumptions and errata, and secure independent
source review. It must then map every quantifier, hypothesis, and conclusion component to Lean and
mutation-test the resulting expression. Until then, selecting categoricity, a decomposition
theorem, the main gap, or another superstable-theory result would be a prohibited substituted
theorem.
