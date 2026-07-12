# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `弱紧致基数`, attributes it only to
"many mathematicians", dates it to the twentieth century, and states `弱紧致基数的组合性质`
("combinatorial properties of weakly compact cardinals"). Stage0 repeats that phrase and marks the
exact definitions, assumptions, proof route, dependencies, axioms, and artifacts as `待补充` (to be
supplied). The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

No definition, theorem, hypotheses, conclusion, primary proof source, edition, page, errata record,
or formal declaration is supplied. The nearby entries for square principles and Ramsey cardinals
locate the broad subject but do not identify this theorem.

## Candidate source work

Authoritative set-theory monographs and original papers are candidate locators, but no edition or
passage is accepted at intake. The source audit must locate a passage that states the intended
property or characterization, record edition, theorem/definition and page, all assumptions and
directions, proof boundary, and errata, then obtain independent review. A general textbook
definition of weak compactness cannot by itself identify which unspecified combinatorial theorem
the repository intended.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "cardinal" | an infinite cardinal or carrier of that size | `Cardinal`, `Cardinal.mk`, universe lifts | pinned APIs probed; exact domain open |
| "weakly compact" | partition-property definition | colorings of unordered pairs and a full-size homogeneous set | candidate only |
| "weakly compact" | inaccessible cardinal with tree property | `Cardinal.IsInaccessible` plus a source-faithful cardinal-tree encoding | candidate only |
| "weakly compact" | infinitary compactness or indescribability | substantial syntax/semantics or set-theoretic encoding | candidate only |
| "combinatorial properties" | implication, equivalence, or characterization | one concrete proposition with all hypotheses | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.SetTheory.Cardinal.Regular` and checks cardinality, regularity, strong-limit
and inaccessible-cardinal declarations, sets, and pairwise predicates. These are encoding
ingredients only. A bounded name/content search found no declaration for weak compactness in pinned
mathlib. That negative search is not the immutable external anchor audit required by the later
phase, and no nearby inaccessible-cardinal theorem receives proof credit here.
