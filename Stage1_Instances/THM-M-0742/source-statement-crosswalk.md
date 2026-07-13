# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5472-5477` supplies exactly the title `递归定理`, Stephen
Kleene, 1938, the gloss `递归函数的自指`, importance `高`, and status `已验证`. Git history places
all six lines at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no
bibliography, formula, definition, theorem locator, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:20272-20297` repeats those fields and explicitly leaves the formal system,
precise definitions and premises, proof route and dependencies, equivalent forms, axioms, machine
state, and artifact links open. Its generated proof-tree language and source `已验证` label provide
no `H`, `M`, or `R` credit under rev-5.6.

## Literal crosswalk

| Repository element | Mathematical possibilities | Pinned Lean lead | Intake result |
|---|---|---|---|
| `递归定理` | Kleene recursion theorem in an index-transformer or parameterized form | `Nat.Partrec.Code.fixed_point` or `fixed_point₂` | family identified; root not selected |
| `递归函数` | total computable code transformer or partial-computable binary family | `Computable f` versus `Partrec₂ f` | binder kind and arity unresolved |
| `自指` | a program whose behavior equals the behavior of a transformed or self-specialized program | `eval (f c) = eval c` versus `eval c = f c` | exact equality and conclusion unresolved |
| Stephen Kleene, 1938 | historical attribution and date | no source field in the Lean declarations | primary theorem passage and ownership review open |
| `已验证` | untrusted inventory metadata | exact checked dependency evidence would require statement mapping | no H0 or M0 credit |

## Historical source lead

S. C. Kleene, "On notation for ordinal numbers," *Journal of Symbolic Logic* 3(4) (1938),
pages 150-155, DOI `10.2307/2267778`, is a bibliographic lead matching the catalog's author and
date. Crossref metadata was retrieved and hashed. The worker did not obtain an accepted immutable
copy of the article text and inspected no primary theorem passage, incorporated definition,
assumption, proof transition, correction, or erratum. The citation is discovery evidence, not H0.

Walter Dean and Alberto Naibo, "Recursive Functions," *Stanford Encyclopedia of Philosophy*,
Spring 2024 archive, Section 3.4, was inspected at its immutable archive URL. Theorem 3.5 states:
for a total computable natural-index transformer `f`, there is an `n` such that `phi_n` and
`phi_(f n)` agree as partial functions. The article calls this the Recursion Theorem and sometimes
the Fixed Point Theorem, while explicitly warning that it does not assert literal equality
`f n = n`. Corollary 3.2 gives the parameterized form: for every partial computable `f(x,y)`, some
index `n` satisfies `phi_n(y) ~= f(n,y)`.

The archived HTML SHA-256 is
`7d856ecda491ab83814622f4a75d277552b8750816412bca215b4a461d0b0af1`.
This authoritative secondary account strongly identifies the family and explains the catalog's
self-reference gloss. It remains secondary discovery evidence rather than a primary H0 source or
an independent source-review receipt, and it does not decide ownership relative to `THM-M-0743`.

## Pinned formal source leads

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.PartrecCode` contains:

| Declaration | Exact candidate type | Upstream label | Boundary |
|---|---|---|---|
| `Nat.Partrec.Code.fixed_point` | `{f : Code -> Code} -> Computable f -> Exists c, eval (f c) = eval c` | Rogers' fixed-point theorem | total code transformer and extensional evaluation equality |
| `Nat.Partrec.Code.fixed_point₂` | `{f : Code -> Nat ->. Nat} -> Partrec₂ f -> Exists c, eval c = f c` | Kleene's second recursion theorem | parameterized partial family and self-specialization |

The module cites Mario M. Carneiro, "Formalizing Computability Theory via Partial Recursive
Functions," ITP 2019, DOI `10.4230/LIPIcs.ITP.2019.12`. Its theorem bodies use the encoded universal
evaluator, `exists_code`, currying/s-m-n infrastructure, and extensional equality. The intake probe
shows both declarations elaborate and report axioms `propext`, `Classical.choice`, and `Quot.sound`.
Those are discovery-only results: no exact source mapping, wrapper, expression fingerprint,
proof-provenance packet, or machine status is accepted here.

## Neighbor evidence

`THM-M-0743` immediately follows this catalog record as `不动点定理` / `递归函数的不动点`, and
`THM-M-0744` names the s-m-n theorem. Separately, `Docs/researches/cs_theorems.md:28` calls
Kleene's second recursion theorem a result that every computable function has a fixed point. That
computer-science record is outside the closed Stage1 set and demonstrates an unresolved naming and
ownership collision only.

## Source gate

Before statement acceptance or H0, accountable reviewers must preserve an immutable accepted source
edition, select one exact root and effective-numbering convention, map every definition, ordered
binder, hypothesis, and conclusion, distinguish index equality from extensional program equality,
resolve `THM-M-0742`/`THM-M-0743`/`THM-C-0006` ownership, inspect corrections and errata, and
approve the source-to-Lean crosswalk. Until then the canonical statement, formal target, expression
hash, and accepted proof state remain null.
