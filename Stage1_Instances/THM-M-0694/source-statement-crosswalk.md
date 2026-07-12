# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` records the title `自然演绎`, attributes it to Gerhard Gentzen,
dates it to 1934, and gives only `自然风格的证明系统` ("a natural-style proof system").
`Docs/researches/cs_theorems.md` instead dates the entry to 1935 and says `自然推理系统` ("natural
deduction system"). `Docs/researches/formalization_classification.md` describes paired
introduction/elimination rules and tree-shaped proofs, with examples, but states no metatheorem.
Stage0 repeats the 1934 gloss. None supplies an edition, section/page, exact calculus, hypotheses,
conclusion, or proof boundary. The date disagreement is also unresolved.

The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`; it supplies no proof
credit. A later source audit must inspect an immutable primary edition/translation, identify a
specific definition and theorem, record the calculus and assumptions, resolve the date and any
errata, and obtain independent review.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "natural deduction" | a derivability judgment with tree constructors | formula/context types and an inductive derivation family | topic only; calculus absent |
| "introduction/elimination pairs" | connective- and quantifier-specific inference rules | typed constructors with side conditions | examples only; exact rules absent |
| "proofs are trees" | inductively generated derivation objects | an inductive family indexed by context and conclusion | representation hint only |
| "proof system" | soundness, completeness, normalization, or derivability | one concrete `Prop` with all hypotheses | conclusion absent |
| `已验证` | untrusted inventory label | no Lean expression or proof body | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
imports `Mathlib.Logic.Basic` and checks core conjunction, disjunction, implication, existential,
and absurdity rule declarations. They demonstrate available encoding vocabulary only. They neither
define the intended object calculus nor select a theorem. The repository-local partial calculus in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_298.lean` was inspected only as discovery context
and is explicitly excluded from target identity and proof credit.
