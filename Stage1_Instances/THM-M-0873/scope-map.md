# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0873` | frozen |
| execution item | `S56-M-0873-INTAKE`, rank 1427 | frozen |
| catalog name | `图的同构问题` | frozen as source wording |
| catalog gloss | `图同构的复杂性` | frozen literally |
| catalog attribution | many mathematicians, twentieth century | untrusted metadata |
| catalog status | `准多项式时间解决` | untrusted metadata |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The catalog status and an inspected author source identify the intended family as the known
quasipolynomial upper bound for general graph isomorphism. They do not yet determine one exact
formal proposition.

## Candidate mathematical boundary

The source lead supplies the following planning scope. It is not the canonical statement.

| Component | Inspected source lead | Unresolved statement decision |
|---|---|---|
| problem | decide whether two given finite graphs are isomorphic | simple undirected graphs, labeled encodings, and vertex-domain representation |
| size | number `n` of graph vertices | graph size versus serialized input bit length and padding policy |
| encoding reduction | binary strings indexed by unordered vertex pairs under the symmetric-group action | exact bit ordering, malformed strings, and checked correspondence with `SimpleGraph.Iso` |
| algorithm | deterministic reduction to String Isomorphism followed by the source algorithm | executable machine, totality, halting, and uniformity semantics |
| cost | quasipolynomially bounded time | elementary operations, bit cost, constants, logarithm base, ceilings, and thresholds |
| bound | `exp(C (log n)^c)` for constants `c`, `C` and all sufficiently large `n` | exact existential binders, positivity constraints, and all-small-input extension |
| conclusion | Graph Isomorphism can be solved in quasipolynomial time | decision procedure existence, correctness, runtime, and their conjunction |

Babai version 2, page 4, defines quasipolynomial boundedness and states Corollary 1.1.2. Helfgott's
post-fix exposition, printed page 1125-02 (PDF page 2), defines the graph-to-string reduction,
states Theorem 1.1 and Corollary 1.2, and says the repaired proof is correct. Neither source is
silently promoted to a final source-fidelity packet at intake.

## Binder and boundary ledger

The statement phase must freeze at least:

- a finite simple undirected graph representation, common or distinct vertex types, and a canonical
  serialization of graph pairs;
- the relationship between `n`, vertex cardinality, adjacency-matrix length, and input bit length;
- the graph-isomorphism decision predicate and its checked relationship to
  `Nonempty (G ≃g H)`;
- deterministic machine, instruction, time, totality, and worst-case conventions;
- the ordered binders for the algorithm, constants, threshold, graphs, and input size;
- the exact quasipolynomial inequality, positivity assumptions, logarithm convention, and rounding;
- empty and singleton graphs, unequal vertex counts, malformed encodings, constant-size inputs,
  loops or parallel edges, and directed or colored inputs; and
- whether the root owns only the generic upper-bound theorem, while `THM-M-0874` owns the
  algorithm-specific construction and proof architecture.

No degenerate case is excluded at intake.

## Neighbor and duplicate boundaries

- `THM-M-0874` is the Babai algorithm record. It may later supply a typed dependency, but its
  statement, source audit, obligations, and proof credit remain independently owned.
- `THM-M-0875` is the Weisfeiler-Lehman heuristic/refinement record and cannot replace the general
  worst-case result.
- `THM-M-0876` concerns graph isomorphism's position relative to P and NP, including open or
  conditional branches; it is not this quasipolynomial upper-bound root.
- `THM-M-1567` repeats the generic graph-isomorphism gloss and status. Integration must choose one
  canonical owner or an explicit alias/transport policy before either record receives unique
  coverage; duplicate proof-body credit is forbidden.

## Explicit exclusions

- Bare decidability of `Nonempty (G ≃g H)` without a verified runtime bound.
- Membership of graph isomorphism in NP presented as the quasipolynomial upper bound.
- An assertion that graph isomorphism is in P, outside P, or NP-intermediate.
- A polynomial or quasipolynomial algorithm for only a special graph class.
- Weisfeiler-Lehman experiments, benchmarks, heuristics, or fixed finite computations.
- A structure, hypothesis, oracle, or certificate that assumes the required algorithm or bound.
- The catalog status, source title, or an adjacent Lean API probe used as proof evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks `SimpleGraph.Iso`, formal languages, and computable many-one and one-one reductions. These
are vocabulary only. They do not supply a graph serialization, bounded machine model, P/NP or
quasipolynomial-time definitions, the target algorithm, or a complexity proof.

A bounded pinned/repo-local search found no exact graph-isomorphism quasipolynomial declaration.
This is intake discovery, not the downstream immutable anchor audit or a global absence claim.

## Gate boundary

`S56-M-0873-STATEMENT` must admit and independently review the exact corrected source result,
resolve duplicate and algorithm-target ownership, freeze every representation and binder, elaborate
the canonical Lean target under minimal imports, and run required statement mutations. Anchor
audit, obligation tree, proof, validation, and release remain dependency-ordered and open.
