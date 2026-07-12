# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` names Pyotr Novikov and William Boone, dates the entry to 1955,
and gives only `\u7fa4\u7684\u5b57\u95ee\u9898\u4e0d\u53ef\u5224\u5b9a` ("the word problem for groups is undecidable").
`Docs/researches/cs_theorems.md` independently repeats a high-level range `1955-59` and the same
gloss. Stage0 says that exact definitions, assumptions, proof history, dependencies, axioms, and
formal artifacts are still to be supplied. The manifest deliberately retains `\u5df2\u9a8c\u8bc1` only as
an untrusted source-status string.

These repository records identify the classical theorem family but do not contain an edition,
paper title, theorem number, page, quotation, assumptions, errata, or proof boundary. Intake does
not promote them to `H0` and does not guess bibliographic details from memory.

## Provisional mathematical crosswalk

| Repository phrase | Mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| "group" | group given by finitely many generators and relators | `PresentedGroup rels` | pinned API probed; concrete presentation open |
| "word" | finite string of generators and formal inverses | effectively coded word type mapping to `FreeGroup` | effective representation open |
| "word equals identity" | image of the word in the presented quotient is `1` | `PresentedGroup.mk rels w = 1` | quotient predicate API probed |
| "word problem" | decide identity for all encoded words in one presentation | unary predicate on the effective word code | exact predicate open |
| "undecidable" | no algorithm computes that predicate | `\u00ac ComputablePred p` after providing `Primcodable` input | candidate semantics only |
| Novikov-Boone | existential construction of a finite presentation with that property | existential proposition packaging all finite/effective data | provisional standard reading |
| `\u5df2\u9a8c\u8bc1` | untrusted inventory label | no proposition or proof term | rejected as evidence |

## Primary-source work required

The source audit must independently inspect immutable copies of the relevant Novikov and/or Boone
publication(s), recording edition or publication identity, theorem/page, exact quantifier scope,
presentation and coding assumptions, proof boundaries, later corrections or errata, and a
source-to-obligation map. It must distinguish historical priority and possibly different theorem
strengths rather than merging two proofs under a title. Until that work is reviewed, the root is
`H1`, not `H0`.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe imports
`Mathlib.GroupTheory.PresentedGroup` and `Mathlib.Computability.Halting`. It checks the free-group
and presented-group types, the quotient map and identity characterization, `ComputablePred`,
`Primcodable`, and finite-set infrastructure. This establishes only that adjacent encoding
ingredients exist. It does not establish a suitable effective coding, an exact Novikov-Boone
declaration, or any proof closure; those belong to later statement and anchor-audit phases.
