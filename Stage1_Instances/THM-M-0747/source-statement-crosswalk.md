# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5507-5512` supplies the title `单纯集`, attribution Emil Post,
year 1944, and the complete gloss `单纯集的存在性` (existence of simple sets). Git history places
all six uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no
definition, quantifiers, hypotheses, proof boundary, bibliography, correction history, or formal
artifact.

`Docs/Stage0_Blueprint.md:20407-20432` repeats that gloss while explicitly leaving exact definitions
and premises, proof route, dependency graph, equivalent formulations, axioms, machine state, and
artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted source metadata and
resets this target to `L0 / rework_required`.

The context disambiguates the title. The record lies in the recursion-theory section between
creative sets and Post's problem; its category is `数理逻辑 / 递归论`; and a separate computer-science
row groups creative and simple sets under computability. It therefore denotes a simple set from
recursion theory, not a simplicial set from topology.

## Primary-source lead

The identified primary publication is Emil L. Post, *Recursively enumerable sets of positive
integers and their decision problems*, *Bulletin of the American Mathematical Society* 50(5)
(1944), 284-316, DOI `10.1090/S0002-9904-1944-08111-1`. Crossref metadata confirms the author,
title, journal, volume, issue, year, page range, DOI, and AMS version-of-record link.

The AMS full text and its Project Euclid mirror were blocked by automated-access challenges in this
worker environment. Consequently the exact Post definition/result page, original positive-integer
conventions, assumptions, proof transitions, and correction or errata status were not inspected.
This bibliographic identification is a source lead, not `H0`. A modern Stanford Encyclopedia of
Philosophy account confirms the standard definition and attributes existence to Post (1944), but it
is a secondary source and cannot replace the required primary-source crosswalk.

## Component crosswalk

| Repository/source-family component | Prospective mathematical meaning | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| `单纯集` | a c.e. set with immune complement | predicate `A : Nat -> Prop`, `REPred A` | theorem family identified; exact source encoding open |
| existence | there is at least one such `A` | existential quantifier over predicates or sets | exact ordered binders not frozen |
| complement infinite | infinitely many naturals are outside `A` | `Set.Infinite {n : Nat | not A n}` | candidate expression elaborates |
| no infinite c.e. subset of the complement | every infinite c.e. `W` intersects `A` | `forall W, REPred W -> Set.Infinite {n | W n} -> exists n, W n /\ A n` | prospective equivalent form; source match and transport open |
| noncomputability | a simple set cannot be computable | negation of `ComputablePred A` | consequence, not a substitute for the root |
| computer-science gloss | existence of a nonrecursive c.e. set | same consequence without immunity | strictly weaker; excluded as the canonical statement |
| `已验证` | untrusted catalog label | no expression or proof object | no H or M credit |

## Lean and source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Computability.Halting` provides `REPred`, `ComputablePred`, the implication from computable
to recursively enumerable predicates, and the c.e./co-c.e. characterization of computability. A
bounded name search found no definition or theorem named for simple or immune sets in pinned
mathlib or repo-local Lean. These are intake discovery observations, not an exhaustive anchor audit
or a global absence claim.

Before leaving `H1`, accountable reviewers must inspect and hash an immutable primary edition,
pinpoint every incorporated definition and the existence result, map assumptions and conclusions,
audit errata, and independently approve the crosswalk. Only then may the statement phase select
minimal imports, freeze and hash an exact elaborated expression, check alternate transports, and
run the required semantic mutations.
