# THM-M-0887 scope map

## Received scope

The repository fixes only the title `谱图理论`, collective attribution `众多数学家`, period
`20世纪`, and gloss `图的谱性质`. It supplies no bibliography, graph class, matrix or operator,
spectrum convention, ordered binders, hypotheses, conclusion, theorem locator, proof, correction
history, or formal artifact. Stage0 repeats the same words and explicitly leaves exact definitions,
premises, proof route, equivalent formulations, axioms, machine status, and artifact links open.

The literal record is a subject heading. Intake preserves that field-level boundary and refuses to
turn a familiar theorem from spectral graph theory into the missing proposition.

## Candidate theorem families not credited

Spectral graph theory contains many non-interchangeable claims, including:

- adjacency-matrix symmetry, real eigenvalues, spectral decomposition, or eigenvalue bounds;
- trace and walk-count identities such as diagonal entries or traces of powers counting walks;
- Laplacian positive semidefiniteness, kernel dimension, and connectivity or component criteria;
- normalized-Laplacian or random-walk spectral statements under degree/nonisolation hypotheses;
- Perron-Frobenius results for connected nonnegative adjacency matrices and regular-graph
  characterizations of the top eigenvalue;
- interlacing under vertex deletion, induced subgraphs, quotients, lifts, or equitable partitions;
- Cheeger-type, expander-mixing, diameter, coloring, independence, or chromatic-number bounds;
- matrix-tree identities connecting Laplacian eigenvalues and spanning-tree counts;
- cospectrality, spectral determination, distance-regularity, strongly regular graphs, Ramanujan
  bounds, or graph reconstruction questions.

The catalog chooses none of these. Some have their own Stage1 IDs. A conjunction of several would
broaden the target; selecting just one would narrow it without authority.

## Proposition-changing choices

Before the statement phase may freeze a root, an accepted source and reviewers must resolve:

1. The graph model: finite/infinite, simple/multi, undirected/directed, weighted/unweighted,
   loopless or allowing loops, labeled/unlabeled, connected or arbitrary.
2. The operator: adjacency, degree, combinatorial Laplacian, normalized Laplacian, signless
   Laplacian, transition matrix, non-backtracking matrix, or another graph operator.
3. The scalar field and representation: real or complex matrices, self-adjoint operators, finite
   eigenvalue lists or set-valued algebraic spectrum.
4. Eigenvalue ordering, algebraic/geometric multiplicity, repeated values, zero eigenvalues,
   spectral radius, largest absolute nontrivial eigenvalue, and sign conventions.
5. Whether regularity, nonempty carrier, decidable adjacency, local finiteness, positive degrees,
   connectedness, bipartiteness, or another hypothesis is assumed or derived.
6. The exact claimed relationship between spectrum and graph structure, including every constant,
   normalization, strict/non-strict inequality, equality condition, and converse direction.
7. The ordered quantifiers over graphs, vertices, eigenvalue indices, subsets, parameters, and
   families, plus all universe and finiteness assumptions.
8. Which alternate adjacency/Laplacian, matrix/operator, quotient, complement, or scaling encodings
   are equivalent and which require checked one-way implications.
9. Whether the result is purely analytic/algebraic, constructive, computational, probabilistic, or
   certificate-based, and the permitted classical, quotient, numeric, and oracle boundaries.
10. The source edition, theorem/section/page, incorporated definitions, proof boundary, dependent
    results, corrections or errata, and independent approval.

## Boundary and degenerate cases

No case is excluded at intake because no proposition is selected. Source review must dispose of
empty and singleton vertex types; edgeless and complete graphs; disconnected graphs; isolated or
universal vertices; degree-zero normalization; loops and parallel edges; zero-by-zero matrices;
repeated eigenvalues; zero and negative eigenvalues; bipartite spectral symmetry; weighted zeros or
negative weights; infinite spectra; and equality at any proposed spectral bound.

These are not cosmetic. For example, normalized Laplacians require a convention at isolated
vertices, Laplacian kernel statements change with empty carriers and component conventions, and a
regular-graph eigenvalue statement can become false or vacuous when regularity or nonemptiness is
removed.

## Neighbor and substitution exclusions

- `THM-M-0884` separately owns Ramanujan graphs; `THM-M-0885` and `THM-M-0886` separately own two
  existence constructions. Their spectral bounds and proofs cannot select this root.
- `THM-M-0888` separately owns Cheeger's inequality and `THM-M-0889` the Alon-Milman spectral-gap
  result. Neither expansion theorem is a generic replacement for spectral graph theory.
- `THM-M-0890` and `THM-M-0891` separately own Hoffman's and Wilf's spectral bounds. Coloring or
  independence inequalities cannot be installed merely because they use graph eigenvalues.
- `THM-M-0894` and `THM-M-0895` separately own distance-regular and strongly regular graphs.
- A spectral theorem for arbitrary Hermitian matrices, Perron-Frobenius theorem, matrix-tree
  theorem, graph Laplacian definition, adjacency-matrix walk identity, or a finite numerical
  eigensolver run is not automatically the requested root.
- A structure field or hypothesis containing the desired spectral property is not a proof.
- The catalog label `已验证` and the discovery-only Lean probe provide no H or M credit.

## Lean boundary and retry condition

Pinned mathlib supplies finite simple graphs, adjacency and Laplacian matrices, Hermitian matrix
eigenvalues, walk-count and Laplacian-kernel results. These APIs demonstrate formalizability of
adjacent components; they neither select a root nor constitute a formal-candidate audit.

To unblock the statement phase, select one lawful immutable primary or authoritative proposition,
pinpoint its definitions and proof, map every binder, hypothesis, conclusion, convention, dependent
source, correction, neighboring-target boundary, and degenerate case, and obtain independent scope
and source review. Only then may the same claim be encoded with minimal pinned imports, expression
and environment fingerprints, checked transports, and statement mutations.
