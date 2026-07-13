# Scope map

## Received claim

The repository fixes only the title `Ore定理`, Oystein Ore, 1960, and the gloss
`Hamilton圈存在的度和条件`. The title, attribution, date, and graph-theory cluster identify the
classical Hamiltonicity criterion, but the catalog supplies no bibliography, graph model, vertex
bound, quantifier order, inequality, conclusion encoding, or boundary convention.

## Candidate mathematical scope

The standard candidate family is:

- `G` is a finite undirected simple graph on a vertex set `V`;
- the order is `n = |V|` and `n >= 3`;
- for every pair of distinct nonadjacent vertices `u` and `v`,
  `degree_G(u) + degree_G(v) >= n`; and
- `G` contains a Hamiltonian cycle.

This is an intake candidate, not a selected canonical proposition. A source-approved statement
must fix every component before the statement phase may elaborate and fingerprint it.

## Proposition-changing decisions

1. Select and preserve an immutable primary-source edition, pinpoint the statement and any
   incorporated definitions, transcribe its ordered assumptions and conclusion, inspect
   corrections or errata, and obtain independent source review.
2. Fix the graph model: finite, undirected, loopless, without parallel edges, and whether
   connectedness is an explicit hypothesis or a consequence.
3. Fix the order binder and lower bound. The familiar theorem uses at least three vertices; the
   catalog does not state this.
4. Fix whether the degree-sum premise ranges over unordered pairs, ordered pairs, or two explicit
   vertices, and make distinctness explicit rather than relying on prose.
5. Fix whether nonadjacency is strict nonadjacency (`u != v` and no edge) or merely `not Adj u v`.
   For a loopless Lean graph, the latter also holds when `u = v` and is a stronger premise.
6. Fix the exact natural-number inequality and cardinality representation.
7. Fix Hamiltonicity: existence of a spanning simple cycle, the source convention for a circuit,
   and its relationship to `SimpleGraph.IsHamiltonian`.
8. Decide whether a Bondy-Chvatal closure theorem or Dirac theorem is a proof dependency only;
   neither may replace the Ore root.

## Boundary cases

- Empty and one-vertex carriers require an explicit source decision. Mathlib treats singleton
  graphs as Hamiltonian by convention, but that convention must not rewrite a source theorem.
- Every two-vertex simple graph is non-Hamiltonian in pinned mathlib. For the complete graph on two
  vertices, the usual premise over distinct nonadjacent pairs is vacuous, so omitting `3 <= |V|`
  would make the candidate false under this convention.
- Quantifying only `not G.Adj u v` includes the diagonal because simple graphs have no loops. The
  resulting conditions `2 * degree_G(u) >= |V|` are not the usual Ore premise.
- Complete graphs have no distinct nonadjacent pair, so the degree-sum premise is vacuous; their
  Hamiltonicity still depends on the graph-order and cycle conventions.
- Natural-number addition and comparison have no coercion issue once the order and degrees are all
  encoded in `Nat`, but alternate integer/cardinal encodings require checked transports.

## Explicit exclusions

- Dirac's minimum-degree theorem (`THM-M-0853`) or the Chvatal-Erdos theorem (`THM-M-0855`) as a
  substituted root.
- The Bondy-Chvatal closure theorem as the target rather than a possible proof bridge.
- A degree-sum condition for adjacent pairs, all pairs including equal vertices, or average degree.
- Hamiltonian paths, Hamiltonian-connectedness, traceability, long-cycle bounds, or fault
  Hamiltonicity in place of a Hamiltonian cycle.
- A structure, hypothesis, axiom, or opaque predicate that stores the requested cycle or theorem.
- The catalog's untrusted verified label, an API check, a source-visible unvalidated branch body,
  or a theorem-name match as proof credit.

## Formal boundary

The intended Lean substrate is a universe-polymorphic finite type `V`, a `SimpleGraph V`,
`Fintype.card V`, `SimpleGraph.degree`, and `SimpleGraph.IsHamiltonian`. Intake does not choose the
canonical expression, minimal module, implicit instances, normalized expression, alternate
transport, or mutation suite. Those belong to `S56-M-0854-STATEMENT` after source and convention
review.
