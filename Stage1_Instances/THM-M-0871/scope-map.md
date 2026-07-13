# THM-M-0871 scope map

## Received scope

The repository names Courcelle's theorem and gives only `有界树宽图的MSO可判定性`. The author and
year identify Courcelle's finite-graph monadic-second-order theorem family. The wording does not
select one theorem, logical language, graph representation, input model, uniformity regime, or
complexity conclusion. Intake preserves that family and does not fill the missing proposition from
mathematical memory.

## Source-backed candidate roots not selected

The inspected 1990 and 1992 primary articles expose materially different claims:

- the monadic theory of every fixed class of bounded expression-width graphs is decidable;
- the monadic theory of every context-free graph set is decidable;
- for fixed formula and width, evaluation is linear in a supplied bounded-width expression;
- for a fixed grammar and formula, evaluation is linear in a supplied derivation sequence;
- for fixed formula and treewidth parameter, a bare finite hypergraph can be evaluated by a
  quadratic algorithm that also finds or approximates a decomposition; and
- later presentations commonly state linear-time or fixed-parameter model checking for finite
  graphs, but that modern formulation is not selected by the catalog or by the two inspected
  passages alone.

None is the canonical root here. In particular, theory decidability, per-instance model checking,
and a runtime bound are not interchangeable conclusions.

## Proposition-changing choices

| Dimension | Choices that remain open |
|---|---|
| structures | finite simple graphs, labeled graphs, hypergraphs, incidence graphs, or finite relational structures |
| logic | MSO1 over vertex sets, MSO2 over vertex and edge sets, CMSO with cardinality-modulo atoms, or another extension |
| target form | decidability of an entire theory, truth of one fixed sentence, or a uniform model-checking function |
| uniformity | fixed or input formula, treewidth bound, signature, grammar, expression, and decomposition |
| width | Courcelle expression width, Robertson-Seymour treewidth, incidence-graph width, or a checked transport |
| input | bare graph, graph plus tree decomposition, bounded-width algebraic expression, or grammar derivation |
| output | Boolean satisfaction, validity over a class, witness/certificate, or a decomposition-or-rejection result |
| complexity | computable/decidable only, polynomial, quadratic, linear, or fixed-parameter time under a fixed cost model |
| encoding | graph, formula, labels, hyperedges, bags, and malformed inputs, including the size measure |

The exact source edition and result, incorporated definitions, quantifier order, premises,
conclusion, proof boundary, correction history, and independent review must be frozen with these
choices.

## Boundary and degenerate cases

Statement review must explicitly cover empty and singleton graphs, edgeless graphs, forests,
disconnected graphs, width-zero and width-one conventions, empty decompositions, maximum bag size
minus one, labels and source vertices, loops and repeated hyperedges, formulas with no free
variables, empty or singleton set assignments, counting moduli, and formulas outside the supported
signature. For algorithmic versions it must also resolve malformed encodings, an incorrect or
missing decomposition, graphs whose width exceeds the supplied bound, zero-length expressions,
hidden formula-dependent constants, totality, halting, and the precise input-size and cost model.

## Neighbor boundaries

- `THM-M-0870` separately owns treewidth and graph tree-decomposition scope. A definition or
  decomposition theorem is substrate, not Courcelle's logical decision result.
- `THM-M-0872` separately owns Bodlaender's treewidth algorithm or approximation scope. Combining a
  decomposition constructor with a logical evaluator requires explicit checked composition.
- `THM-M-0867` separately owns the Robertson-Seymour graph-minor theorem. Structural graph theory
  does not transfer statement or proof credit to this target.

## Explicit exclusions

- First-order graph satisfiability or first-order model checking in place of MSO.
- MSO1 in place of source passages allowing edge and edge-set quantification, or plain MSO in place
  of CMSO without recording the restriction.
- Linear evaluation from a supplied expression or decomposition presented as a linear algorithm on
  a bare adjacency encoding.
- A special graph class, one fixed property, or a small-width enumeration presented as the full
  theorem without a checked source transport.
- A structure or hypothesis that assumes the decision procedure, correctness, or runtime result.
- The catalog status `已验证`, a DOI, an API name, or successful elaboration of adjacent substrate
  used as H or M evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks the first-order graph
language and its transport to `SimpleGraph`, the simple-tree predicate, and graph isomorphisms. A
bounded repository and pinned-mathlib search found no exact Courcelle, treewidth,
tree-decomposition, graph MSO, or bounded-treewidth model-checking declaration. The probe is
adjacent interface evidence only; it does not establish MSO syntax, a decomposition, treewidth, a
model checker, a complexity theorem, or a complete anchor audit.
