# Scope map

## Candidate core boundary

The repository gloss and the exact modern source lead point toward Hoffman's ratio bound, but the
following components remain candidates until an independently reviewed source-selection decision:

- a finite nonempty simple undirected graph `G` of order `n`;
- `k`-regularity and the real symmetric adjacency matrix `A`;
- adjacency eigenvalues ordered from largest to smallest, with `lambda_min` the least eigenvalue;
- the independence number `alpha(G)`, or alternatively the cardinality of each independent set;
- the inequality `alpha(G) <= n * (-lambda_min) / (k - lambda_min)`;
- exact casts, denominator/sign hypotheses, and whether the result is stated over real or rational
  quantities.

These bullets describe a likely statement family, not a frozen theorem.

## Proposition-changing choices

The statement phase must resolve all of the following:

1. Whether the graph is finite by a `Fintype` carrier or by a finite set, and whether nonemptiness
   is explicit.
2. Whether `n` is a separate natural number with a cardinality hypothesis or is definitionally the
   vertex-cardinality expression.
3. Whether regularity is expressed graph-theoretically or as the all-ones adjacency eigenvector.
4. Whether `lambda_min` is defined by an ordered Hermitian eigenvalue enumeration, by membership
   and minimality in the real spectrum, or is an assumed lower spectral bound.
5. Whether the conclusion bounds `SimpleGraph.indepNum`, every independent finset, or a selected
   maximum independent set.
6. Whether the denominator is proved positive from a nonempty-edge hypothesis, assumed nonzero,
   or avoided by a division-free inequality.
7. Whether equality conditions, such as the constant number of neighbors into an extremal
   independent set, are part of the target or a separate theorem.
8. Whether the target includes only regular unweighted simple graphs or a weighted, irregular,
   Laplacian, strongly regular, clique, or chromatic variant.

## Degenerate cases to resolve

- empty, singleton, and edgeless graphs, where degree and least-eigenvalue conventions may make the
  ratio denominator zero;
- complete graphs and graphs with isolated vertices;
- disconnected regular graphs and multiplicity of the top or bottom eigenvalue;
- the possibility `lambda_min = k`, `lambda_min = 0`, or a denominator with an unresolved sign;
- natural-number independence/cardinality values compared with real-valued spectral expressions;
- repeated least eigenvalues and the choice of an index witnessing the least value;
- empty versus nonempty independent sets and maximum versus merely maximal independent sets.

No degenerate case is silently excluded at intake.

## Explicit exclusions

- Hoffman's chromatic-number lower bound `chi >= 1 - lambda_max / lambda_min`;
- Wilf's neighboring spectral lower bound for chromatic number (`THM-M-0891`);
- Delsarte's clique/coclique bound restricted to strongly regular graphs;
- Lovasz theta, Cvetkovic inertia, Laplacian, normalized-Laplacian, weighted, or arbitrary-graph
  extensions unless the accepted source explicitly selects one;
- an equality characterization or application substituted for the inequality itself;
- a theorem that assumes the desired numerical bound, a positive-semidefinite certificate, or the
  desired extremal cardinality and then projects it;
- a floating-point eigenvalue computation, numerical experiment, unchecked certificate, or a
  finite example;
- generic independent-set, adjacency-matrix, Hermitian-spectrum, or regularity APIs treated as a
  formalization of the source result;
- the catalog's `verified` label, source year, API probe, or a theorem name treated as proof credit.

## Neighbor boundaries

- `THM-M-0888` Cheeger inequality and `THM-M-0889` Alon-Milman theorem concern expansion and
  spectral gaps, not the independence-number ratio bound.
- `THM-M-0891` Wilf theorem concerns a spectral chromatic-number lower bound and cannot replace this
  target.
- `THM-M-0895` strongly regular graphs may supply an application domain, but generic parameter
  constraints are not Hoffman's regular-graph inequality.
