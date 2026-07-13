# Scope map

## Preserved theorem family

The catalog title and gloss select the Lovasz-Kneser chromatic-number theorem family. The standard
modern candidate uses a graph whose vertices are the `k`-element subsets of an `n`-element set and
whose adjacent vertices are disjoint. For positive `k` and `2 * k <= n`, its chromatic number is
usually stated as `n - 2 * k + 2`.

That formula is a discovery lead, not the canonical claim. The primary article's statement was not
inspected, and the catalog supplies neither parameters nor definitions. The dependent statement
phase must select and independently review one exact source proposition before fixing Lean binders.

## Decisions required at statement freeze

1. Inspect and preserve an immutable primary source passage, including its definitions, exact
   result locator, assumptions, proof boundary, corrections, and errata, and obtain independent
   review.
2. Fix whether parameters are positive integers with `2 * k <= n`, or whether the graph and formula
   are totalized outside the nonempty range. Do not infer `k > 0` or `n >= 2 * k` only from the
   familiar slogan.
3. Fix the ground set as `Fin n`, an arbitrary finite type of cardinality `n`, or a checked
   alternate, and fix vertices as finite subsets, sets with a cardinality proof, or another
   representation.
4. Fix adjacency as finite-set disjointness and prove that it gives the exact source graph,
   including symmetry and the absence of loops.
5. Fix chromatic number as mathlib's `SimpleGraph.chromaticNumber : ENat`, a natural minimum, or
   the equivalent conjunction of colorability at `n - 2 * k + 2` and non-colorability one lower.
6. Fix natural subtraction and coercions, binder order, universes, decidability instances, and all
   boundary conventions before generating an expression fingerprint.
7. Mutation-test a removed parameter hypothesis, a changed ground-set domain, changed binder scope,
   and at least one boundary case, as required by the rev-5.6 statement gate.

## Boundary cases to resolve

- `k = 0`, whose only vertex under one encoding is the empty set;
- `n < k`, where the fixed-cardinality vertex type is empty;
- `k > 0` but `n < 2 * k`, where no two vertices are adjacent;
- `n = 2 * k`, where the nontrivial graph is a matching under standard conventions;
- `k = 1`, which yields a complete graph when the ground set is nonempty;
- empty, singleton, disconnected, and edgeless graphs and mathlib's chromatic-number conventions;
- arithmetic at `n - 2 * k + 2`, including the order of truncated subtraction and addition;
- equality in `ENat` versus an equality or minimality statement in `Nat`.

## Explicit exclusions

- the additive-combinatorics Kneser theorem for sumsets (`THM-M-0938`);
- only the Petersen graph, odd graphs, or another fixed `(n,k)` special case;
- stable, generalized, bipartite, circular, fractional, or q-Kneser graphs;
- clique number, independence number, fractional chromatic number, or merely an upper bound;
- only the easy explicit coloring without the Lovasz lower bound;
- a graph or structure carrying the desired coloring or chromatic equality as a field;
- a finite computation, theorem name, citation, API probe, or untrusted `已验证` label used as proof
  evidence.

## Expected proof boundary

The standard route separates an explicit-coloring upper bound from the hard lower bound. The 1978
paper's title and abstract point to a topological connectivity argument and Kneser's conjecture;
the source and formal anchor audits must expose every topological bridge rather than treating
"Lovasz-Kneser" as a terminal leaf. No Borsuk-Ulam or exact Kneser theorem was located by the
bounded intake search, so none is credited.

## Formal boundary

Pinned mathlib provides `Finset.powersetCard`, the finite subtype cardinality theorem,
`SimpleGraph.fromRel`, `SimpleGraph.Colorable`, and `SimpleGraph.chromaticNumber`. The discovery-only
probe defines the disjointness graph over `{s : Finset (Fin n) // s.card = k}` and checks these
interfaces. It does not choose the canonical statement, certify minimal imports or expression
identity, run semantic mutations, or establish an exhaustive anchor audit.
