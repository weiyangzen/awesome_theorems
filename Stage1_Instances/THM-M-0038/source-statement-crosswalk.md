# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records only:

- title: `莫林定理`;
- attribution: `Sigmund Morill`;
- year: 1937;
- gloss: `关于中心单代数的指数与次数`;
- importance: medium;
- untrusted formalization label: `已验证`.

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md` repeats them while
explicitly leaving exact definitions and premises, proof route, equivalent statements, axioms,
machine status, and artifact links open. That generated projection is not an independent source.

## Identity search boundary

The repository has no other occurrence supporting `Sigmund Morill`, no primary citation, and no
legacy Lean artifact for `THM-M-0038`. Exact-phrase queries for `Sigmund Morill` and `Morill
theorem` in Crossref and Bing's indexed results returned no matching algebraist, theorem, or 1937
paper during the 2026-07-13 intake. Crossref's top results were unrelated works containing either
`Sigmund` or the surname `Morill`; Bing returned unrelated pages. These bounded, mutable search
results do not prove nonexistence. They establish only that the received attribution could not be
verified and must not authorize an invented statement.

## Clause crosswalk

| Repository component | Mathematical data required | Pinned Lean surface | Intake status |
|---|---|---|---|
| "central simple algebra" | field, unital associative algebra, centrality, simplicity, finite dimensionality | `CSA K`; separately `Algebra.IsCentral`, `IsSimpleRing`, `FiniteDimensional` | adjacent definitions elaborate; exact source convention open |
| "degree" | exact invariant, codomain, square-dimension relation and positivity/existence assumptions | no candidate in the bounded Brauer/Central modules | undefined |
| "index" | exact invariant, division representative or alternative definition, choice and invariance proof | no candidate in the bounded Brauer/Central modules | undefined |
| "and" | actual theorem relation between the invariants | no declaration can be selected without a proposition | entirely missing |
| `Sigmund Morill`, 1937 | author identity, work title, theorem/page, chronology and spelling | not applicable | unresolved metadata conflict |
| `已验证` | an exact immutable formal artifact, declaration, proof body and validation receipt | none supplied | untrusted; no proof credit |

## Adjacent formal candidates

The discovery-only probe imports `Mathlib.Algebra.BrauerGroup.Defs` and checks `CSA`,
`IsBrauerEquivalent`, `Brauer.CSA_Setoid`, and `BrauerGroup`. These authenticate a plausible data
substrate, not an index-degree theorem. In particular, the quotient definition does not itself
construct the division representative, define its degree as an index, or prove any requested
relation.

The separately owned Brauer classification targets `THM-M-0037` and `THM-M-0424`, and the
Artin-Wedderburn target `THM-M-0036`, are discovery boundaries only. Their statements, evidence,
and state cannot transfer to this target. A later source audit may model an explicit dependency,
but intake grants no proof credit.

## First failed source gate

The exact source-statement identity gate fails before H0: the received phrase contains no
predicate, its eponym/author could not be verified, and no pinpoint source defines the two
invariants or their hypotheses. Retry requires an independently reviewed immutable source passage
that resolves the author metadata and supplies a complete proposition. Only then can every source
row be mapped to ordered Lean binders, hypotheses, definitions, conclusion, and boundary cases.
