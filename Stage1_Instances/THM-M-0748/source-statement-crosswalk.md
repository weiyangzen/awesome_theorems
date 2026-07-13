# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5514-5519` supplies the title `Post问题`, Emil Post, 1944, and the
complete gloss `是否存在严格介于可计算与完全之间的度` (whether there exists a degree strictly
between computable and complete). Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no reducibility relation, c.e.
restriction, degree representatives, definitions of the endpoints, quantifiers, proof source,
solution year, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:20434-20459` repeats the gloss while leaving exact definitions and
premises, proof route, dependency graph, equivalent formulations, axioms, machine status, and
artifact links open. The rev-5.6 manifest preserves `已解决` only as untrusted metadata and resets
the target to `L0 / rework_required`.

The surrounding catalog resolves part, but not all, of the ambiguity. The entry occurs in recursion
theory after creative/simple sets and immediately before `Friedberg-Muchnik定理`, whose gloss is
`Post问题的肯定解`. Separate neighboring entries own Turing degrees and c.e. degrees. This strongly
identifies the classical c.e. Turing-degree question but does not authorize importing those
neighbors' definitions or proof credit.

## Source leads

The identified primary question source is Emil L. Post, *Recursively enumerable sets of positive
integers and their decision problems*, *Bulletin of the American Mathematical Society* 50(5)
(1944), 284-316, DOI `10.1090/S0002-9904-1944-08111-1`. Crossref metadata confirms the bibliographic
record and official version-of-record link. Attempts to retrieve the AMS and Project Euclid text
returned HTML access pages rather than the paper, so no primary page, exact wording, premise,
proof-boundary, or errata claim is made.

A modern secondary account, the Stanford Encyclopedia of Philosophy entry *Recursive Functions*,
states Question 3.1 as whether a c.e. degree `a` satisfies `0 <_T a <_T 0'`. It reports independent
positive answers by Muchnik (1956) and Friedberg (1957), and states a stronger theorem producing
two Turing-incomparable c.e. sets. This pins down a credible standard reading and source trail, but
it is secondary discovery evidence, not `H0` and not permission to conflate the direct and stronger
statements.

## Component crosswalk

| Repository/source-family component | Prospective meaning | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| `度` / degree | Turing-equivalence class | `TuringEquivalent`, `TuringDegree` | family supported; representative transport open |
| computable endpoint | least Turing degree `0` | `Nat.Partrec`, `partrec_iff_forall_turingReducible` | adjacent API only; canonical bottom not frozen |
| complete endpoint | c.e.-complete halting degree `0'` | no admitted endpoint declaration | missing from inspected surface |
| strictly between | `0 < a` and `a < 0'` | partial order on `TuringDegree` | order substrate only |
| omitted c.e. restriction | witness degree has a c.e. representative | `REPred` is available in another encoding | no checked set/oracle/partial-function bridge |
| solved question | positive existence theorem | no admitted declaration | source and formal proof audit open |
| Friedberg-Muchnik neighbor | two incomparable c.e. degrees imply intermediate degrees | no admitted declaration | stronger alternate route; implications must be checked |
| `已解决` | untrusted catalog status | no expression or proof object | no H or M credit |

## Lean and source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Computability.TuringDegree` defines oracle reducibility between partial functions,
Turing equivalence, their antisymmetrization quotient, and its partial order. A bounded local search
found no Post-problem, intermediate-degree, or Friedberg-Muchnik declaration. This is intake
discovery only, not the immutable, precommitted anchor audit required by the next phases and not a
global absence claim.

The mathlib representation uses partial functions `Nat ->. Nat`; the usual statement uses c.e.
sets and their characteristic-function oracles. Before a formal target can be frozen, the statement
phase must construct or locate checked bridges, define the bottom and complete c.e. degrees, and
prove that the selected strict-order expression matches every source component. Until primary and
solution sources are pinpointed, their assumptions and relationship are independently reviewed,
and these encoding choices are approved, the truthful source status is `H1` rather than `H0`.
