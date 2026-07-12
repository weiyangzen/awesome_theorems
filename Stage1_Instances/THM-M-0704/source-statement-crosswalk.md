# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `lambda calculus`, attributes it to
Alonzo Church, gives 1936, and states only `functional computation model`. Stage0 repeats those
fields while marking exact definitions, assumptions, proof path, equivalent formulations, axioms,
and existing formal artifacts as open. The rev-5.6 manifest preserves `verified` only in the
explicitly untrusted source-status field. No proposition, theorem number, page, hypotheses,
conclusion, proof source, edition, or formal artifact is supplied.

The adjacent repository item is the Church-Rosser theorem and explicitly states confluence. This
contrast is evidence that this target's topic gloss must not automatically be rewritten as
confluence, but adjacency does not determine a different theorem.

## Candidate source work

Church's 1936 paper *An Unsolvable Problem of Elementary Number Theory* is a historically plausible
locator for lambda-definability and effective calculability, not an accepted source anchor for an
unspecified theorem. A later textbook could supply modern syntax and operational semantics, but
choosing its substitution, confluence, normalization, or expressiveness result would still require
a repository scope decision. The source audit must identify an immutable edition and pinpoint
passage, record its definitions and theorem, assumptions, proof boundary and errata, and obtain
independent review. No `H0` source status is claimed here.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "lambda calculus" | raw terms with variables, abstraction, and application | an inductive syntax plus binding convention | topic component only |
| "functional" | abstraction/application and substitution | capture-avoiding substitution or an equivalent checked representation | convention absent |
| "computation" | beta reduction, conversion, normalization, or evaluation | a precisely oriented one-step relation and specified closure | relation absent |
| "model" | a formalism representing a class of computable functions | encoding, decoding, semantics, and an exact adequacy/completeness claim | proposition absent |
| 1936 / Church | historical attribution | immutable source revision and premise-to-binder mapping | locator only |
| `verified` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned Lean revision `98dc76e3c0a9b856c9b98726b713fb04fab16740`, the bounded intake
probe imports `Lean` and checks the kernel-expression constructors `Lean.Expr.bvar`,
`Lean.Expr.lam`, and `Lean.Expr.app`. They demonstrate only that the host system can represent
bound-variable expressions. Lean kernel expressions are not a selected object-language encoding,
and these checks do not establish substitution correctness, beta reduction, confluence,
normalization, expressiveness, or any other candidate theorem. A bounded repo/mathlib text search
found no dedicated untyped lambda-calculus target for this item; the later anchor audit remains
open and must use its own frozen discovery protocol.
