# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0884`, the title `Ramanujan graphs`, broad twentieth-century
attribution, and the gloss `optimal spectral expander graphs`. Intake preserves this general
Ramanujan-graph/optimality topic boundary. It does not import the untrusted `verified` status or
silently turn a class name into an existence or construction theorem.

## Root decision required

An accountable source review must choose exactly one truth-valued boundary before Lean statement
work begins:

1. A definition/classification proposition for when a finite regular graph is Ramanujan.
2. A theorem connecting the Ramanujan eigenvalue bound to an explicit expansion or mixing optimum.
3. An Alon-Boppana theorem saying the bound is asymptotically best possible for an infinite family.
4. An existence theorem for Ramanujan graphs under specified degree and size quantifiers.
5. A conjunction that explicitly owns and composes more than one of these claims.

The source lead supports the first three as related mathematics but does not show which one the
catalog intended. A predicate definition alone is not a theorem that optimal expanders exist. An
existence or construction result is not the asymptotic lower bound that explains optimality.

## Proposition-changing decisions

The selected root must freeze:

- finite simple undirected graphs versus multigraphs, loops, weighted graphs, digraphs, or Cayley
  graphs, together with the vertex index type and decidable adjacency;
- connectedness and nonemptiness, degree `k`, the lower bound on `k`, and the treatment of degrees
  `0`, `1`, and `2`;
- the adjacency matrix or operator, coefficient field, eigenvalue occurrence and multiplicity
  representation, ordering, and equivalence to a multiset or characteristic-polynomial encoding;
- which eigenvalues are trivial: `k`, `-k` in the bipartite case, or all eigenvalues whose absolute
  value is `k`, including the effect of disconnectedness and multiplicity;
- the exact closed boundary `<= 2 * sqrt(k - 1)`, natural-number subtraction and coercions, and
  whether an equivalent squared inequality is credited;
- whether `optimal spectral expander` means the Ramanujan predicate itself, Cheeger expansion,
  spectral gap, mixing rate, universal-cover spectrum, or Alon-Boppana asymptotics;
- for an asymptotic result, fixed degree, an infinite sequence or family, graph sizes tending to
  infinity, liminf/epsilon conventions, repeated members, and bipartite restrictions;
- for an existence result, the degree range, one graph versus infinitely many, size constraints,
  effectiveness, and any construction data;
- empty and singleton vertex types, complete or cycle graphs, disconnected regular graphs,
  bipartite graphs, repeated eigenvalues, equality at the spectral boundary, and every exceptional
  small case;
- ordered binders, universes, typeclasses, hypotheses, conclusion, foundation, TCB, and computation
  profiles.

## Neighbor ownership

- `THM-M-0881` owns the broad existence/construction family for expander graphs.
- `THM-M-0883` owns the Lubotzky-Phillips-Sarnak construction of Ramanujan graphs.
- `THM-M-0885` owns Morgenstern's existence and explicit-construction result family.
- `THM-M-0886` owns the Marcus-Spielman-Srivastava bipartite Ramanujan existence result.
- `THM-M-0887` owns general spectral graph theory, and `THM-M-0888` owns Cheeger's inequality.

Those targets may later provide typed source, proof, or bridge edges, but proximity transfers no
statement, proof body, or status. In particular, the 1988 LPS paper cannot make this item a duplicate
construction target.

## Excluded substitutions

- an arbitrary regular graph without the nontrivial spectral bound;
- a structure, typeclass, hypothesis, or axiom that stores the desired Ramanujan property;
- one computed finite example, a numerical eigenspectrum, or a random-graph experiment;
- only the upper bound on a second-largest eigenvalue while silently ignoring negative nontrivial
  eigenvalues or bipartite trivial eigenvalues;
- a normalized-Laplacian or singular-value bound without checked equivalence to the selected
  adjacency-spectrum convention;
- Cheeger's inequality, a generic spectral-gap lemma, or an Alon-Boppana slogan presented as the
  definition, existence, or construction of Ramanujan graphs;
- the LPS, Morgenstern, or MSS theorem used as inherited closure for this target;
- the catalog label `verified`, a theorem name, URL, source abstract, API probe, or unchecked
  numerical certificate used as human or machine proof evidence.

## Formal boundary

No canonical Lean expression, alternate encoding, or excluded-case list is frozen. Pinned mathlib
contains useful finite-simple-graph and Hermitian-matrix interfaces but no source-selected
Ramanujan predicate in this dossier. The intake probe is deliberately theorem-free. Exact target
elaboration, mutation tests, formal-anchor provenance, obligation freeze, and proof work belong to
dependent phases.
