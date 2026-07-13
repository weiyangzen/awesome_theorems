# Scope map

## Preserved repository scope

The repository fixes only target `THM-M-0888`, the name `Cheeger inequality`, Jeff Cheeger, the
year 1970, the graph-theoretic gloss `the spectral gap and isoperimetric constant of a graph`, and
an untrusted `verified` label. Intake preserves that relationship as the subject boundary. It does
not choose a familiar textbook formula or import assumptions from memory.

Stage0 repeats the same wording and explicitly leaves precise definitions and premises, proof
route, dependencies, equivalent forms, axioms, machine status, and artifact links open. The
neighboring catalog entries `spectral graph theory` and `Alon-Milman theorem` provide subject
context only; they transfer no statement or proof credit.

## Candidate theorem families, not frozen claims

Common discrete Cheeger inequalities relate an isoperimetric quantity to a nonzero Laplacian or
random-walk spectral value. Depending on conventions, candidate shapes include a two-sided bound
for conductance and the second normalized-Laplacian eigenvalue, or a degree-dependent bound for an
edge-isoperimetric constant and a combinatorial-Laplacian eigenvalue. These are discovery shapes
only. The catalog does not choose either family, the constants, or even whether both directions
belong to the root.

The 1970 attribution needs separate source scrutiny. Cheeger's original result is geometric, while
the catalog explicitly states a graph relationship. A later discrete theorem, adaptation, or
modern source may be intended, but no such source is cited. Intake must not replace the graph target
with a Riemannian-manifold Cheeger inequality merely to match the attribution.

## Proposition-changing decisions

An approved source statement must freeze all of the following before Lean elaboration:

1. The graph category: finite, locally finite, or infinite; directed or undirected; simple,
   multiple-edge, or weighted; with the exact finiteness, nonemptiness, connectedness, loop,
   weight-symmetry, nonnegativity, and reversibility conventions.
2. The spectral operator: adjacency, combinatorial Laplacian, normalized Laplacian, transition
   matrix, or another operator; its coefficient field, sign, scaling, and self-adjoint realization.
3. The spectral value: second eigenvalue with multiplicity, first positive eigenvalue, gap from a
   trivial eigenvalue, or the bottom/infimum of an operator spectrum, including ordering,
   attainment, discrete-versus-essential spectrum, and repeated-zero conventions.
4. The isoperimetric object: edge boundary, edge expansion, conductance, vertex boundary, or a
   weighted boundary, with cardinality or volume denominator and all factor-of-two conventions.
5. The tested subsets: nonempty, proper, at most half the vertex cardinality or volume, and the
   treatment of equality and odd-size rounding.
6. Regularity, minimum-degree, positive-degree, or weighting hypotheses and whether the degree is a
   fixed parameter appearing in the constants.
7. The exact inequality direction or two-sided conjunction, all square roots, squares, factors,
   strictness, ordered binders, coercions, and conclusion packaging.
8. Whether the source owns only a discrete graph theorem, a geometric theorem, or an explicitly
   checked transport between them, and how the neighboring targets divide ownership.

## Boundary and degenerate cases

No case is excluded before a proposition is selected. Source review must decide empty and singleton
vertex types; edgeless, disconnected, or complete graphs; isolated and zero-degree vertices;
regular degree zero or one; empty and full tested subsets; exactly-half volume; zero total volume;
multiple connected components and repeated zero eigenvalues; zero isoperimetric constant; and
whether a square-root expression requires a separately proved nonnegativity premise.

These are semantic cases, not cosmetic details. For example, normalized Laplacians and conductance
need a convention for isolated vertices, while a disconnected graph typically has zero spectral
gap and zero expansion under some but not all definitions.

## Explicit exclusions and neighbor boundaries

- `THM-M-0881` (expander graphs) cannot be substituted by treating Cheeger's inequality as an
  expander existence or construction theorem.
- `THM-M-0880` (sparse cut) separately owns graph-partition sparsity. Conductance or edge-boundary
  definitions may overlap, but its optimization or approximation target cannot become this root.
- `THM-M-0887` (spectral graph theory) is a broad neighboring subject and cannot absorb this root.
- `THM-M-0889` (Alon-Milman theorem) separately owns a spectral-gap/expansion result family and may
  own one historical discrete Cheeger formulation; source review must distinguish its exact
  statement and provenance from this target.
- Cheeger's Riemannian-manifold inequality is not a substitute for the catalog's graph statement.
- A one-sided corollary is not the two-sided theorem, and a regular-graph specialization is not an
  unrestricted irregular or weighted theorem without a checked implication in the required direction.
- Generic graph, adjacency-matrix, Laplacian, positive-semidefinite, or connectivity APIs are
  substrate only. A structure or hypothesis storing the desired inequality is not a proof.
- Numerical eigenvalues, finite experiments, external URLs, title matches, and the untrusted
  `verified` label supply no human-source or machine-proof credit.

## Lean and retry boundary

Pinned mathlib provides adjacent finite-simple-graph degrees, adjacency and combinatorial Laplacian
matrices, quadratic-form identities, positive semidefiniteness, and a kernel/component theorem.
That available substrate does not select or narrow the catalog's unknown graph domain.
The bounded intake query found no literal graph Cheeger, conductance, isoperimetric-constant, or
spectral-gap declaration. This is not an exhaustive anchor audit and does not prove absence.

Statement work may proceed only after accountable reviewers admit one immutable source proposition,
reconcile graph versus geometric attribution and neighboring ownership, and freeze every definition,
binder, hypothesis, conclusion, normalization, constant, correction, and degenerate case. Only then
may a minimal Lean import and expression be selected and mutation-tested.
