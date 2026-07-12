# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `统一算法`, attributes it to John Alan
Robinson in 1965, and states only `项的统一算法` ("an algorithm for unifying terms"). Stage0 repeats
that gloss. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`. No term
grammar, algorithm, theorem, hypotheses, conclusion, proof locator, edition/page, or formal artifact
is supplied.

## Candidate source work

Robinson's 1965 paper, *A Machine-Oriented Logic Based on the Resolution Principle*, is a plausible
primary-source discovery anchor because it introduces the unification algorithm in the resolution
setting. It is not accepted as `H0`: this intake has not bound an immutable edition, pinpointed the
algorithm and correctness assertion, mapped its conventions and premises, checked corrections or
errata, or obtained independent source review. Later textbook formulations can aid interpretation
but cannot silently replace the repository's attributed source.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "term" | first-order terms over variables and function symbols | `FirstOrder.Language.Term` | pinned API probed; exact signature open |
| "unify" | equality after applying one substitution | `FirstOrder.Language.Term.subst` plus a frozen predicate | substitution API probed; predicate open |
| "algorithm" | Robinson transformation or recursive implementation | executable definition and termination evidence | absent |
| algorithm success | returned substitution is a unifier | soundness theorem | candidate only |
| algorithm failure | input has no unifier | failure-correctness/completeness theorem | candidate only |
| "most general" | every unifier factors through the result | factorization theorem with fixed composition direction | absent from metadata |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.ModelTheory.Syntax` and checks first-order languages, terms, variables,
relabeling, substitution, and substitution of function symbols. These are encoding ingredients
only. A bounded name/content search did not identify a mathlib implementation of Robinson's
first-order unification algorithm or an MGU correctness theorem. That negative discovery is not the
later immutable anchor audit and gives no completeness claim.
