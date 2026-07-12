# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Anand Pillay and Charles Steinhorn, gives 1988, and says
only "cell decomposition in o-minimal structures". Stage0 repeats the gloss and leaves the
definitions, assumptions, axioms, and formal system open. The manifest deliberately records
`已验证` as untrusted source metadata. None of these records supplies a theorem number, page,
verbatim statement, proof, errata check, or machine artifact.

## Primary-source discovery boundary

The attribution points toward the Pillay-Steinhorn ordered-structure literature, but this intake
has not identified and inspected an immutable primary-source item whose exact bibliographic year
and theorem wording justify the repository row. A standard later reference is Lou van den Dries,
*Tame Topology and O-minimal Structures* (Cambridge University Press, 1998), whose cell-decomposition
chapter is a candidate locator for the modern theorem family. It has not been adopted as the
repository row's primary source, and no theorem/page or H0 credit is asserted here.

The source audit must resolve the apparent attribution/year locator, select an exact theorem,
record edition, theorem, page, wording, definitions, assumptions, dependencies, corrections and
errata, and obtain independent row-by-row review.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| o-minimal structure | ordered first-order expansion whose unary definable sets are finite unions of points and intervals | language/order expansion interface, definability, finite union and interval predicate | family identified; encoding open |
| cell | recursively, a point/base cell in dimension one and a graph or open strip over a lower-dimensional cell | inductive cell predicate with definable continuous boundary functions | definition and boundary conventions open |
| decomposition | finite pairwise-disjoint cell cover of the ambient Cartesian power | finite indexed family, coverage, disjointness, and cell witnesses | representation open |
| compatible | each cell is contained in or disjoint from each member of the input family | `C ⊆ X ∨ Disjoint C X`, or a checked equivalent | exact orientation/encoding open |
| finite definable family | finitely many definable subsets handled simultaneously | finite index type or `Finset` plus per-member definability | source quantifier convention open |
| all dimensions | induction from unary o-minimality to `M^n` | tuple model and dimension-recursive decomposition | provisional; source confirmation required |
| Pillay/Steinhorn, 1988 | bibliographic discovery locator | no machine component | unresolved; no source credit |

## Pinned Lean boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides generic
first-order definability, ordered-language semantics, intervals, finite families, set partitions,
and disjointness ingredients checked by `IntakeProbe.lean`. The scoped local search found no named
o-minimality or cell-decomposition root declaration. Nearby legacy o-minimal/Pila-Wilkie artifacts
contain discovery notes or assumed slots and receive no proof credit. This is a local intake search,
not the later immutable external anchor audit.
