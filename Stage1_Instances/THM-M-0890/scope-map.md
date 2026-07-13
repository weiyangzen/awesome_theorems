# Scope map

## Selected core boundary

The statement phase selects Haemers 2021, Section 2, Theorem 1 as the exact conventional result
matching the repository name and independent-set spectral-bound gloss:

- a finite nonempty simple undirected graph `G`, represented by `SimpleGraph V`;
- positive natural degree `k` and `G.IsRegularOfDegree k`;
- the real adjacency matrix and mathlib's descending Hermitian eigenvalue enumeration;
- `lambda_min` at index `Fintype.card V - 1`;
- the independence number `G.indepNum` cast to `Real`;
- the real inequality `alpha(G) <= |V| * (-lambda_min) / (k - lambda_min)`.

This is a frozen statement interface, not a theorem proof or H0 source packet.

## Resolved proposition choices

1. The carrier has explicit `Fintype`, `Nonempty`, `DecidableEq`, and decidable adjacency instances.
2. Graph order is definitionally `Fintype.card V`; no separate `n` binder is introduced.
3. Regularity is graph-theoretic `SimpleGraph.IsRegularOfDegree`.
4. The least eigenvalue uses `Matrix.IsHermitian.eigenvalues₀` at the last finite index.
5. The conclusion bounds `SimpleGraph.indepNum`, not a chosen independent finset.
6. Positive degree is explicit. It excludes the nonempty edgeless `k = lambda_min = 0` case where
   the paper's algebra divides by zero and Lean's totalized quotient would falsify the display.
7. Equality information is outside this root.
8. The target is the unweighted regular simple-graph result only.

The following remain downstream transport or audit questions rather than statement ambiguity:

- prove or check transports to a division-free form and to every-independent-set formulations;
- prove that the selected eigenvalue index has the intended minimality and denominator sign;
- independently review the positive-degree source boundary and historical attribution;
- decide whether equality consequences should become separate obligation nodes.

## Degenerate-case decisions and downstream checks

- Empty carriers are excluded by `Nonempty V`.
- Zero-degree regular graphs, including singleton and nonempty edgeless graphs, are excluded by
  `0 < k`; Lean boundary fixtures check this case.
- Degree-one, disconnected positive-degree regular, complete, and repeated-extreme-eigenvalue cases
  remain included.
- Natural independence number and graph order are explicitly cast to `Real`.
- The last descending eigenvalue index is explicit; its minimality and the denominator sign are
  downstream proof/transport obligations, not extra statement premises.
- The conclusion uses the independence number, so empty versus nonempty chosen-set and merely
  maximal versus maximum-set conventions do not enter the canonical root.

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
