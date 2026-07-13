# THM-M-0870 scope map

## Preserved repository scope

The intake preserves target `THM-M-0870`, the label `树宽`, the Robertson/Seymour attribution, the
year 1984, and the literal gloss `图的树分解`. This identifies the treewidth/tree-decomposition
subject area but supplies no theorem-grade formula. It is not promoted to a definition or theorem.

## Candidate roots not credited

The catalog wording is compatible with materially different roots:

1. A definition of a tree decomposition by a tree-indexed family of vertex bags satisfying vertex
   coverage, edge coverage, and connected occurrence of each graph vertex.
2. A definition of the width of one decomposition and treewidth as the minimum possible width.
3. An existence theorem for a tree decomposition of every graph, which is too weak and can become
   trivial depending on whether a one-bag decomposition is allowed.
4. A characterization of graphs of treewidth at most `k`, minor monotonicity, a forbidden-minor or
   chordal-completion theorem, a grid theorem, or another structural result.
5. An algorithmic theorem about recognizing, computing, or approximating treewidth.

None is selected or credited at intake. A definition, invariant, property, and theorem about that
property are not interchangeable truth-valued targets.

## Proposition-changing decisions

Before statement elaboration, an approved source review must freeze:

- one authoritative edition, exact definition/theorem/page locator, incorporated definitions,
  assumptions, conclusion, proof boundary, corrections or errata, and independent review;
- finite simple undirected graphs versus multigraphs or directed graphs, labelled versus
  isomorphism-invariant treatment, vertex universes, and all finiteness/typeclass assumptions;
- the decomposition tree as a finite nonempty simple tree, abstract tree, forest, or other index,
  including whether redundant or empty bags are allowed;
- bags as sets, finite sets, or subobjects, and the exact vertex-cover and edge-cover conditions;
- the running-intersection condition as connected occurrence sets, path convexity, or an
  equivalent encoding, together with checked transports for any credited alternate;
- width as `max |bag| - 1`, maximum bag size, or another convention, and treewidth as a minimum,
  infimum, or existence-bounded predicate with an attainment proof where required;
- every ordered binder, hypothesis, conclusion, equality/inequality direction, and computation or
  foundation policy.

## Boundary and degenerate cases

No case is excluded because no proposition is selected. The statement phase must decide empty and
singleton input graphs, an empty versus nonempty index tree, empty bags, a one-bag decomposition,
edgeless and disconnected graphs, infinite carriers, the maximum of an empty bag family, and
whether the empty graph has treewidth `-1`, `0`, or a separately typed value. Natural-number width
cannot silently encode a source convention using `-1`.

## Neighbor and substitution exclusions

- `THM-M-0867` and `THM-M-0868` separately own Robertson-Seymour/graph-minor theorem claims. Their
  structural results and evidence do not transfer to this target.
- `THM-M-0869` separately owns the forbidden-subgraph characterization topic.
- `THM-M-0871` separately owns Courcelle's bounded-treewidth MSO decidability theorem.
- `THM-M-0872` separately owns Bodlaender's treewidth algorithm topic.
- Pathwidth, branchwidth, carving width, clique-width, chordal completions, brambles, grid-minor
  characterizations, and forbidden-minor theorems cannot replace an unspecified treewidth root.
- A structure that stores bags together with proofs of the decomposition conditions is an
  interface, not evidence for an additional theorem. A one-bag witness cannot be substituted for a
  width bound or characterization.
- The untrusted catalog label `已验证` and the adjacent Lean API probe supply no source or proof
  credit.

## Formal discovery boundary

Pinned mathlib provides `SimpleGraph`, `SimpleGraph.IsTree`, induced graphs, graph isomorphisms,
spanning-tree existence, and finite-set cardinality. A bounded literal search found no declaration
for treewidth or tree decomposition in repo-local Lean or pinned mathlib. This is intake discovery,
not the exhaustive immutable anchor audit. No canonical module, declaration, expression,
fingerprint, wrapper, or proof body is selected.
