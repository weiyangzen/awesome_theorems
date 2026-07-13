# THM-M-0871 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6383-6388` supplies exactly the title `Courcelle定理`, attribution
Bruno Courcelle, year 1990, gloss `有界树宽图的MSO可判定性`, importance `高`, and status `已验证`.
All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, graph or logic
definition, ordered binder, premise, conclusion, algorithm, cost model, correction record,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23765-23790` repeats the gloss while leaving the formal system, precise
definitions and premises, proof route, dependencies, alternate statements, axioms, machine status,
and artifact links open. Its generic `已验证` and leaf-audit prose is planning metadata, not
evidence. Rev-5.6 retains that label only as untrusted metadata and resets the target to
`L0 / rework_required`.

## 1990 primary source lead

Bruno Courcelle, *The Monadic Second-Order Logic of Graphs. I. Recognizable Sets of Finite Graphs*,
*Information and Computation* 85(1), 1990, pages 12-75, DOI
`10.1016/0890-5401(90)90043-H`, matches the catalog author and year. The complete author-hosted
published scan has 64 pages, 3,341,918 bytes, and SHA-256
`e5989841626dc08c5acea6fd6bfb8c2413ff86d9c5b16f80aba5c6cfb7f42acd`.

Definitions 3.1-3.2 on printed pages 37-39 model finite labeled graphs with separate vertex and
edge domains. Object variables range over vertices or edges and set variables over vertex sets or
edge sets. The broader counting logic also has cardinality-modulo atoms. Thus the source is
MSO2-like and, in its main generality, CMSO; it is not silently identical to MSO1 over ordinary
simple graphs.

Theorem 4.4 (page 45) makes definable bounded-type graph sets recognizable. Corollary 4.8 (page 51)
gives decision procedures for a fixed formula over a context-free graph set. Corollary 4.10 (page
52) states that fixed bounded-expression-width graph classes and every context-free graph set have
decidable monadic theory. Proposition 4.14 (pages 54-55) gives linear evaluation for a fixed formula
from a supplied bounded-width graph expression, or from a derivation sequence for a fixed grammar.
It does not by itself give linear time from a bare adjacency graph.

## 1992 treewidth bridge

Bruno Courcelle, *The Monadic Second-Order Logic of Graphs III: Tree-Decompositions, Minors and
Complexity Issues*, *RAIRO-Theoretical Informatics and Applications* 26(3), 1992, pages 257-286,
DOI `10.1051/ita/1992260302571`, is the primary source lead tying this family directly to treewidth.
The complete official published scan has 31 PDF pages, 2,737,945 bytes, and SHA-256
`b73c2e11a5311f6f69ced7815d72ccc1b65cb476c24b4e3b4ac0f58acef08774`.

The abstract on printed page 257 advertises quadratic algorithms for deciding monadic properties
of bounded-treewidth hypergraphs. Printed page 263 again permits variables over edges, vertices,
edge sets, and vertex sets. Definition 2.1 (page 264) defines tree decompositions and treewidth.
Section 3 (pages 273-274) distinguishes linear evaluation of a supplied bounded-width expression
from constructing such an expression from a bare hypergraph. Proposition 3.1 (pages 274-276) gives
a quadratic algorithm for fixed formula and width parameter, with a decomposition/approximation
boundary. This is not a unique modern finite-simple-graph linear-time statement.

Courcelle's author publication index was inspected and no explicit correction link was located for
either article. That bounded observation is not evidence that no erratum exists. The full
correction history, exact proof-node mapping, lawful source admission, and independent review remain
open, so neither source is H0 evidence at intake.

## Literal crosswalk

| Repository component | Primary-source possibilities | Prospective Lean component | Intake result |
|---|---|---|---|
| bounded treewidth | 1992 tree decompositions; 1990 bounded expression width | decomposition structure, width predicate, and checked bridge | no encoding or transport selected |
| graphs | finite labeled graphs or hypergraphs with vertex and edge domains | finite simple graph, hypergraph, or relational structure | model and boundary cases open |
| MSO | edge/vertex objects and edge/vertex sets; optional counting atoms | explicit MSO2/CMSO syntax and semantics | mathlib probe exposes first-order syntax only |
| decidability | theory decidability or formula evaluation | `Decidable`, computable evaluator, or algorithm correctness | exact conclusion and uniformity open |
| complexity | linear on supplied expressions/derivations; quadratic bare-hypergraph route | cost semantics and proven bound | catalog does not select a bound or input model |
| 1990 / Courcelle | primary family provenance | source/provenance metadata | family identified; exact root not selected |
| `已验证` | untrusted catalog field | accepted H and kernel receipts | no H0 or M credit |

## Candidate-meaning boundary

Decidability of all sentences over a fixed graph class is not the same proposition as model checking
one input graph. A fixed formula and fixed width bound differ from a uniform formula or bound input.
MSO1, MSO2, and CMSO differ in expressive power. A graph expression, tree decomposition, or grammar
derivation supplied as input changes both the statement and runtime. Expression width must not be
renamed treewidth without a checked bridge. Decidable, polynomial, quadratic, fixed-parameter, and
linear conclusions are different claims.

## Pinned Lean crosswalk

| Declaration | What it supplies | Why it is not the target |
|---|---|---|
| `FirstOrder.Language.graph` | one binary adjacency relation | first-order language only; no set quantification |
| `SimpleGraph.structure` | a first-order structure for a simple graph | no MSO/CMSO syntax, decomposition, or algorithm |
| `FirstOrder.Language.simpleGraphOfStructure` | transport from simple-graph models | representation substrate only |
| `SimpleGraph.IsTree` | connected acyclic graph predicate | not a tree decomposition or treewidth measure |
| `SimpleGraph.Iso` | adjacency-preserving equivalence | no logical decision or complexity result |

`IntakeProbe.lean` authenticates these declarations at the pinned revision. A bounded exact-topic
search found no Courcelle, treewidth, tree-decomposition, monadic-second-order graph, or matching
model-checking declaration in repo-local or pinned mathlib Lean sources. This is not a complete
external audit or a global absence proof.

## Source gate

Before the statement phase can close, accountable reviewers must select one immutable proposition
and map every graph/hypergraph, formula, set-quantification, counting, width/decomposition,
uniformity, encoding, machine/cost, binder, premise, conclusion, boundary case, proof passage, and
correction. They must reconcile `THM-M-0870` and `THM-M-0872`. A formal reviewer must then map only
that claim to a minimal-import Lean expression and checked transports.

Until then, `H1` records a published primary theorem family whose exact source statement mapping is
incomplete, `M4` records that no exact usable formal artifact is credited, and `R4` records the lack
of an anchorable proof reconstruction. These classifications do not say that Courcelle's published
results are open or false.
