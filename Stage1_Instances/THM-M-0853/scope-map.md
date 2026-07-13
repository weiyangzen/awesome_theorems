# Scope map

## Preserved catalog scope

The received claim is exactly `Hamilton圈存在的度条件`, "a degree condition for the existence of a
Hamiltonian cycle." Together with the name, attribution, and date, it identifies the classical
graph-theoretic Dirac theorem family. It does not itself provide a binder-complete proposition.

The conventional candidate family, not yet credited as the canonical statement, contains:

- a finite simple undirected graph `G` on a finite vertex type `V`;
- graph order `n = Fintype.card V` with the usual lower bound `3 <= n`;
- a lower bound of one half of `n` on every vertex degree, or on `G.minDegree`; and
- the conclusion that `G` contains a Hamiltonian cycle.

## Proposition-changing decisions

An immutable source and independent review must settle these choices before statement execution:

1. Whether the graph is explicitly finite, simple, undirected, loopless, and labelled, and whether
   the source assumes an order `n` separately or uses the cardinality of the vertex carrier.
2. Whether the lower bound is written pointwise for every vertex or through minimum degree, and
   what decidability/typeclass assumptions the Lean encoding exposes.
3. How "at least half the order" is encoded over natural numbers. For odd `n`, `n / 2 <= d` is a
   floor bound and is weaker than the standard real-valued inequality. Candidate integral forms
   include `n <= 2 * d` and `(n + 1) / 2 <= d`; their equivalence must be checked rather than
   assumed.
4. Whether `n >= 3` is an explicit premise, incorporated in a definition, or handled by separate
   finite boundary cases.
5. Whether "Hamiltonian cycle" maps exactly to `SimpleGraph.IsHamiltonian`, to an explicit closed
   walk with `Walk.IsHamiltonianCycle`, or to another source-faithful encoding, including any
   checked transport between forms.
6. The ordered universes, types, instances, graph and vertex binders, hypotheses, conclusion,
   foundation profile, TCB policy, and computation policy.

## Boundary and mutation cases

The statement phase must explicitly resolve vertex-cardinality cases zero, one, two, and three;
odd and even graph orders; complete graphs at the lower boundary; strict versus non-strict degree
bounds; pointwise versus minimum-degree formulations; and removal of the order or degree premise.

Pinned mathlib defines a singleton graph to be Hamiltonian by convention, proves an empty graph is
not Hamiltonian, and proves a two-vertex simple graph is not Hamiltonian. The conventional
`3 <= n` premise excludes those cases, but the source crosswalk must still document rather than
silently inherit the library convention.

## Explicit non-substitutions

- Do not substitute Ore's degree-sum condition, the Chvatal-Erdos connectivity criterion, or a
  random-graph Hamiltonicity threshold; those are different catalog targets.
- Do not substitute a sufficient condition that assumes connectedness, regularity, completeness,
  bipartiteness, or another premise absent from the selected source.
- Do not use `n / 2 <= degree` as shorthand for a real half-order bound without proving the
  rounding relationship for odd `n`.
- Do not replace Hamiltonian-cycle existence with connectedness, a Hamiltonian path, a long cycle,
  or a cycle through only a selected vertex subset.
- Do not confuse graph-theoretic Dirac's theorem with the Dirac equation, Dirac operators,
  Hamiltonian mechanics, or Dirac measures.
- Do not encode the desired conclusion as an axiom, opaque premise, structure field, oracle,
  certificate, or hypothesis.
- Do not treat the catalog label `已验证`, a paper title, a DOI, a theorem name, or a successful API
  probe as source identity or proof credit.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the single import
`Mathlib.Combinatorics.SimpleGraph.Hamiltonian` exposes `SimpleGraph.minDegree`, pointwise degree
lemmas, `SimpleGraph.Walk.IsHamiltonianCycle`, and `SimpleGraph.IsHamiltonian`. The intake probe
checks these definitions and candidate proposition shapes only. It does not freeze a minimal import
certificate, normalized expression, environment fingerprint, transport, mutation result, formal
anchor, terminal proof body, or theorem proof.
