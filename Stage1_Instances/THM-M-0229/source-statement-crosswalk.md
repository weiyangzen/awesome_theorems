# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1654-1659` supplies exactly the title `皮卡大定理`, attribution to
Emile Picard, the year 1879, the gloss `本性奇点邻域内函数取遍所有复数值至多一个例外` ("in a
neighborhood of an essential singularity, the function takes all complex values with at most one
exception"), importance "high," and status `已验证`. All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
definition, ordered binder, hypothesis, proof boundary, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:6356-6384` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected source lead

The stable article revision "Picard theorem," *Encyclopedia of Mathematics*, revision 48178, was
inspected on 2026-07-13 at
`https://encyclopediaofmath.org/index.php?title=Picard_theorem&oldid=48178`. It states the big
theorem for a single-valued analytic function near an isolated essential singular point: every
finite complex value, with at most one exception, is assumed in an arbitrary neighborhood. It
separately states that the infinitely-often formulation follows directly, distinguishes the
meromorphic extended-plane variant with at most two exceptional sphere values, and identifies
Picard's 1879 and 1880 publications.

This article is an authoritative secondary disambiguation lead, not `H0`. It was not cited by the
repository; no lawful immutable local copy, incorporated definition chain, theorem-level proof
boundary, correction or errata audit, translation review, or independent source review is
accepted. The listed Picard papers are primary bibliographic leads only; their exact passages were
not inspected or credited.

## Clause crosswalk

| Repository phrase | Source-family component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "function" | single-valued analytic complex function | `f : Complex -> Complex` or a function on a source-selected domain | binder and partial-domain model absent |
| "essential singularity" | isolated essential singular point `a` | punctured analyticity plus a source-faithful exclusion of removable and pole cases | no pinned predicate located; exact definition open |
| "neighborhood" | arbitrary neighborhood of `a` | `Filter.nhdsWithin a {a}^c`, all sufficiently small punctured balls, or an equivalent encoding | quantifier and domain containment open |
| "all complex values" | every finite complex value | `w : Complex` and existence of `z` in the selected punctured neighborhood with `f z = w` | finite versus sphere-valued domain must be explicit |
| "at most one exception" | one possible omitted finite value | a subsingleton omitted-value set or an optional global exception | quantifier scope and cardinality encoding open |
| named Great Picard recurrence | every nonexceptional value is assumed infinitely often arbitrarily close to `a` | infinite preimage intersection, sequences converging to `a`, or repeated filter occurrence | absent from catalog; source lead treats it as a consequence; root ownership open |
| `已验证` | untrusted inventory label | source review plus kernel receipts would be required | no H or M credit |

## Neighbor and alternate-form boundary

`THM-M-0228` owns Picard's Little Theorem for entire functions. Deducing it from an accepted Great
Picard theorem would require a checked reduction and would not merge the two targets. The analytic
finite-plane form, meromorphic sphere-valued form, omitted-set cardinality form, every-neighborhood
form, arbitrarily-small-radius form, and infinitely-many-preimages form are not credited as
equivalent until their domains and quantifiers are frozen and Lean transports compile.

## Pinned Lean boundary

Pinned mathlib supplies the punctured-neighborhood notation `Filter.nhdsWithin a {a}^c`, analytic
predicates, removable-singularity theorems, `MeromorphicAt`, `meromorphicOrderAt`, and
`MapClusterPt`. These interfaces can express pieces of a future statement but do not themselves
define an essential singularity or prove the value-distribution conclusion. A bounded exact-topic
search found no terminal Great Picard declaration. These observations are discovery inputs only,
not the downstream immutable formal-candidate audit.

Before leaving `H1`, accountable reviewers must accept an immutable exact source proposition, map
every incorporated definition, binder, premise, conclusion, exception and recurrence clause,
inspect corrections and errata, and independently approve fidelity to `THM-M-0229`. Only then may
the statement phase select minimal imports, elaborate and fingerprint the target, check alternate
encodings, and run removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
