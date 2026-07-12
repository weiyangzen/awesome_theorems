# Source-statement crosswalk

## Available repository record

`Docs/researches/math_theorems.md` supplies the title "上同调群", the attribution "众多数学家",
the period "20世纪", and the statement "拓扑空间的上同调不变量". `Docs/Stage0_Blueprint.md`
repeats that record but leaves definitions, premises, equivalent formulations, axioms, and formal
artifacts open. Under rev-5.6 its `已验证` label is explicitly untrusted. This is secondary metadata,
not a pinpoint primary theorem.

## Candidate primary sources

- Samuel Eilenberg and Norman Steenrod, *Foundations of Algebraic Topology*, Princeton University
  Press (1952), as a candidate source for the axiomatic functoriality and homotopy-invariance
  characterization of homology/cohomology theories.
- Edwin H. Spanier, *Algebraic Topology*, McGraw-Hill (1966), as a candidate source for a classical
  singular-cohomology construction and its invariance properties.

These bibliographic records are discovery anchors only. No edition-specific theorem number, page,
wording, assumptions, definitions, corrections, or errata was inspected and independently reviewed
in this intake; therefore neither candidate is `H0` evidence.

## Crosswalk

| Repository phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "topological spaces" | a space `X`, possibly with no separation assumptions | concrete `TopologicalSpace X` context | domain family identified; restrictions open |
| "cohomology groups" | graded ordinary singular cohomology `H^n(X; G)` | singular cochains, differential, cycles/boundaries quotient or homology object | theory, coefficients, and grading open |
| "invariants" | homeomorphic spaces have corresponding isomorphic groups | induced contravariant maps and an isomorphism theorem | weakest reading identified; exact conclusion open |
| possible homotopy invariance | homotopic maps induce the same map, hence homotopy-equivalent spaces have isomorphic groups | homotopy-to-cochain-homotopy bridge and induced-map equality | plausible strengthening, not selected |
| `已验证` | repository status label | no proof credit | untrusted by rev-5.6 |

## Source and machine boundary

Repository search found adjacent Lean material for sheaf cohomology and abstract cohomology
interfaces, plus historical audits reporting no selected ordinary topological singular-cohomology
functor in their pinned snapshots. None is a source-frozen proposition or accepted proof for this
target. This observation is discovery input only, not the required immutable anchor audit.

Before `H0`, an accountable reviewer must select an immutable primary edition and pinpoint theorem,
verify all definitions, premises, coefficient and grading conventions, and errata, and approve a
row-by-row source map. Before statement credit, that approved map must be tied to one elaborated
Lean expression and checked transports for every credited alternate encoding.
