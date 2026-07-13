# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5584-5589` supplies exactly the title `可计算枚举度`, attribution
to many mathematicians, the time `20世纪`, the gloss `c.e.度的结构`, importance "high," and status
`已验证`. Git provenance places all six uncited lines in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no definition, formula,
ordered binder, hypothesis, conclusion, theorem locator, proof, correction, or formal artifact.

`Docs/Stage0_Blueprint.md:20704-20729` repeats those fields while explicitly leaving the formal
system, logical foundation, background, exact definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine status, and artifact links open. Its generic planning
sentence about a known closed result is not evidence. The rev-5.6 manifest preserves `已验证` only
as `source_status_untrusted` and resets this target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| computably enumerable | a predicate/set that is the domain or range of an effective process | `REPred`, a chosen set/enumerator/index representation, and checked equivalences | no representation selected |
| degree | equivalence class under a selected reducibility | exact reduction relation, quotient, representative map, equality and order | reducibility not stated |
| c.e. degree | usually a Turing degree containing a c.e. set | predicate connecting c.e. representatives to `TuringDegree`, with quotient well-definedness | no such target frozen |
| structure | order, join, density, splitting, jump, definability, automorphisms, or another result | one exact truth-valued conclusion and all hypotheses | umbrella phrase, not a proposition |
| many mathematicians / twentieth century | historical topic marker | immutable source, theorem/page, definitions, proof boundary, errata, reviewer | no locator supplied |
| `已验证` | untrusted catalog status | kernel and source receipts for one exact target | no H or M credit |

## Source-family leads

Pinned mathlib itself cites Robert I. Soare, *Recursively Enumerable Sets and Degrees*, Springer,
1987, in `Mathlib.Computability.Reduce`, and Piergiorgio Odifreddi, *Classical Recursion Theory:
The Theory of Functions and Sets of Natural Numbers*, Vol. I, 1989, in
`Mathlib.Computability.TuringDegree`. These are credible authoritative monograph leads for the
subject vocabulary. They do not reveal which result the repository intended, and neither has been
selected, pinpointed, crosswalked, or independently reviewed for this target. They therefore carry
discovery value only, not `H0` or canonical-statement credit.

## Neighbor and substitution boundary

The surrounding catalog independently schedules recursive enumerability (`THM-M-0745`), Post's
problem (`THM-M-0748`), Friedberg-Muchnik (`THM-M-0749`), Turing degrees (`THM-M-0750`), joins of
Turing degrees (`THM-M-0751`), and the jump operator (`THM-M-0752`). Those rows show that the broad
word "structure" cannot silently be resolved to one of these named neighboring results. No source,
state, receipt, or proof credit is shared across their owned paths.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.Computability.Halting` defines `REPred` as the domain of a computable partial function;
- `Mathlib.Computability.TuringDegree` defines Turing reducibility, equivalence, the quotient-like
  `TuringDegree`, and its partial order;
- `Mathlib.Computability.Reduce` defines many-one and one-one reductions and gives
  `ManyOneDegree` a partial order and upper-semilattice structure.

These are adjacent ingredients, not an exact match. In particular, `ManyOneDegree` uses the wrong
reducibility for ordinary c.e. Turing degrees, while the inspected Turing-degree file does not
define a c.e.-degree subtype or connect `REPred` representatives to a structural theorem. The
bounded search is intake discovery only, not a complete external anchor audit or a global absence
claim.

Before leaving `H5`, accountable reviewers must turn the topic into one stable repository target
by selecting and lawfully preserving an immutable authoritative proposition, pinpointing all
incorporated definitions and assumptions, fixing neighbor ownership, auditing corrections and
errata, and independently approving the crosswalk. Only then may the statement phase freeze a
source-identical Lean expression and execute the rev-5.6 statement gate. Under rev-5.6, `H5` blocks
ordinary theorem-proof execution, so an explicit accountable target decision must redirect this
record to that corrected stable proposition; the present intake does not make that decision.
