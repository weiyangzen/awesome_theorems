# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5479-5484` supplies exactly the title `不动点定理`, Stephen
Kleene, 1938, the gloss `递归函数的不动点`, importance "high," and status `已验证`. All six lines
originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no
bibliography, formula, definition, theorem locator, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:20299-20324` repeats those fields and explicitly leaves the formal system,
precise definitions and premises, proof history and dependencies, equivalent forms, axioms, machine
state, and artifact links open. Its generic theorem-tree language and source `已验证` label provide
no `H`, `M`, or `R` credit under rev-5.6.

## Literal crosswalk

| Repository element | Mathematical possibilities | Pinned Lean candidate | Intake result |
|---|---|---|---|
| `不动点定理` | Rogers fixed point, Kleene second recursion theorem, or an equivalent index theorem | `Nat.Partrec.Code.fixed_point` or `fixed_point₂` | theorem family identified; root not selected |
| `递归函数` | total recursive code transformer or partial-recursive parameterized family | `Computable f` versus `Partrec₂ f` | binder kind and arity unresolved |
| `不动点` | semantic equality of computed partial functions, not necessarily equality of codes | `eval (f c) = eval c` versus `eval c = f c` | equivalence convention unresolved |
| Stephen Kleene, 1938 | historical attribution/date | no source field in the Lean declaration | primary theorem passage and ownership review open |
| `已验证` | untrusted inventory metadata | an exact checked dependency could be evidence only after statement mapping | no H0 or M0 credit |

## Historical source lead

S. C. Kleene, "On notation for ordinal numbers," *Journal of Symbolic Logic* 3(4) (1938),
pages 150-155, DOI `10.2307/2267778`, is a bibliographic lead consistent with the catalog's author
and date. Crossref metadata was inspected and hashed, but the article text was not available in the
worker evidence. No theorem passage, incorporated definition, assumption, proof transition, or
erratum was inspected. This metadata is therefore discovery evidence only, not an H0 source.

Walter Dean and Alberto Naibo, "Recursive Functions," *Stanford Encyclopedia of Philosophy*,
Spring 2024 archive, Section 3.4, Theorem 3.5, was inspected at its immutable archive URL. It states
the 1938 theorem for a total computable natural-index transformer `f`: there is an `n` for which
`phi_n` and `phi_(f n)` agree as partial functions. It explicitly says the Recursion Theorem is also
called the Fixed Point Theorem and warns that the conclusion is not literal index equality
`f n = n`. The archived HTML SHA-256 is
`7d856ecda491ab83814622f4a75d277552b8750816412bca215b4a461d0b0af1`.

This authoritative secondary account aligns closely with mathlib's `fixed_point` and strengthens
the family crosswalk, but it remains secondary discovery evidence rather than H0. The statement
phase must still inspect a lawful immutable primary copy or another accepted source that pinpoints
the intended theorem, reconcile its terminology with the catalog and neighboring targets, and map
every premise and conclusion. A modern source may clarify notation, but it cannot silently replace
the historical claim.

## Pinned formal source lead

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.PartrecCode` contains:

| Declaration | Exact candidate type | Upstream label | Boundary |
|---|---|---|---|
| `Nat.Partrec.Code.fixed_point` | `{f : Code -> Code} -> Computable f -> Exists c, eval (f c) = eval c` | Rogers' fixed-point theorem | total code transformer; extensional evaluation equality |
| `Nat.Partrec.Code.fixed_point₂` | `{f : Code -> Nat ->. Nat} -> Partrec₂ f -> Exists c, eval c = f c` | Kleene's second recursion theorem | parameterized partial family; likely overlaps `THM-M-0742` |

The pinned source is a complete Lean theorem-body lead and its module cites Mario M. Carneiro,
"Formalizing Computability Theory via Partial Recursive Functions," ITP 2019, DOI
`10.4230/LIPIcs.ITP.2019.12`. That reference explains the formalization family but does not resolve
which catalog theorem owns which declaration. The intake probe shows that both declarations
elaborate and report axioms `propext`, `Classical.choice`, and `Quot.sound`. Those checks are
discovery-only; no wrapper, statement fingerprint, proof provenance packet, or machine status is
accepted here.

## Neighbor evidence

`THM-M-0742` immediately precedes this record as `递归定理` / `递归函数的自指`, and `THM-M-0744`
immediately follows it as the s-m-n theorem. Separately, `Docs/researches/cs_theorems.md:28` calls
Kleene's second recursion theorem a result that every computable function has a fixed point. That
computer-science record is outside the closed 1546-target Stage1 set and is used only to demonstrate
the unresolved naming collision.

## Source gate

Before statement acceptance or H0, accountable reviewers must preserve an immutable source edition,
select the exact root and numbering convention, map all ordered binders and hypotheses, distinguish
code equality from extensional program equality, resolve `THM-M-0742`/`THM-C-0006` overlap, inspect
corrections and errata, and approve the source-to-Lean crosswalk. Until then the canonical statement,
formal target, expression hash, and accepted proof state remain null.
