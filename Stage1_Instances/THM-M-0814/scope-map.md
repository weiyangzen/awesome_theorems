# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0814` | frozen |
| execution item | `S56-M-0814-INTAKE`, rank 1373 | frozen |
| catalog name | `最大流最小割定理` | frozen as source wording |
| catalog claim | `网络流的最大值等于最小割容量` | frozen literally |
| attribution | L. R. Ford / D. R. Fulkerson, 1956 | frozen as untrusted metadata |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

`THM-C-0096` repeats a shorter max-flow/min-cut gloss in the Stage0 computer-science catalog, but
it is outside the 1546-target rev-5.6 manifest. It is duplicate provenance only and supplies no
second statement, slot, or evidence to this target.

## Candidate mathematical boundary

This table records choices exposed by the catalog and inspected primary source. It is planning
scope, not a canonical proposition.

| Component | Primary-paper candidate | Unresolved decision |
|---|---|---|
| graph | finite undirected one-dimensional complex with vertices and arcs | graph versus multigraph, loops/parallel arcs, directed versus undirected encoding |
| terminals | two distinguished vertices `a` and `b`, source and sink | explicit distinctness and membership binders |
| capacities | a strictly positive number on every arc | `Real` versus `NNReal`, positive versus nonnegative, finite versus infinite values |
| chain | a non-self-intersecting source-to-sink sequence of distinct arcs and vertices | exact path representation and orientation of traversed undirected arcs |
| flow | a finite collection of nonnegative weighted source-to-sink chains | collection/multiplicity encoding versus edge flow with conservation and skew symmetry |
| feasibility | sum of weights of chain flows using each arc does not exceed its capacity | finite sum/index type and treatment of zero-weight chains |
| flow value | sum of all chain-flow weights | maximum existence versus supremum formulation |
| disconnecting set | arc set meeting every source-to-sink chain | equivalence to a vertex-partition cut and orientation conventions |
| cut capacity | sum of capacities of arcs in the disconnecting set | minimum existence and whether only inclusion-minimal cuts are ranged over |
| conclusion | maximal flow value equals the minimum disconnecting-set capacity | equality of values versus existence of an optimizing flow/cut pair |

The familiar directed formulation with edge capacities and flow conservation may be equivalent to
a suitable translation, but it is not definitionally the 1956 paper's chain-flow proposition. It
requires an explicit, checked source and representation transport before it can be credited.

## Binder and boundary ledger

The exact domains, ordered binders, hypotheses, conclusion expression, and alternate encodings in
`instance.json` remain empty or null because the statement gate has not selected a representation.
It must resolve at least:

- empty vertex or edge types, no source-to-sink chain, and zero-edge networks;
- source equal to sink and terminals outside the graph's vertex set;
- loops, parallel arcs, and disconnected or isolated vertices;
- zero capacities versus the paper's strictly positive capacities;
- real, rational, natural, or extended-nonnegative capacity codomains;
- finite chain collections with repeated chains and zero-weight components;
- circulations, dead-end flow, and antiparallel edge flows omitted by the paper's encoding;
- disconnecting sets versus vertex-partition cuts and inclusion-minimal cuts;
- attainment of maximum/minimum rather than equality of suprema/infima;
- integral-capacity integrality and Ford-Fulkerson algorithm termination, which are not in the
  catalog gloss or Theorem 1.

No degenerate case is excluded at intake.

## Non-substitution boundary

The following cannot close this target without a checked equivalence or implication that covers
the exact selected claim:

- weak duality alone, namely that every feasible flow value is at most every cut capacity;
- existence or correctness of Ford-Fulkerson, Edmonds-Karp, Dinic, or push-relabel alone;
- the integral-flow theorem or an integer-capacity special case;
- Menger's theorem, Hall's marriage theorem, Konig's theorem, or linear-programming duality alone;
- planar-network duality or the paper's Theorem 2 special case;
- a fixed finite network computation or executable solver result;
- a structure or hypothesis storing an optimal flow and cut;
- generic graph, sum, or maximum APIs checked by the intake probe;
- the catalog's `已验证` label or the excluded `THM-C-0096` record.

## Formal boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe authenticates
`Graph`, `Graph.IsLink`, `Graph.Inc`, `Graph.banana`, `Finset.sum`, and `Finset.max'`. These support
undirected multigraph incidence and finite aggregation. They do not supply a directed network,
capacity/flow/cut definitions, or max-flow min-cut theorem.

A bounded exact-topic search over repo-local Lean and pinned mathlib found no declaration matching
network flow or max-flow min-cut. This is intake discovery only, not a global absence claim or the
downstream immutable anchor audit.

## Gate boundary

`S56-M-0814-STATEMENT` must independently approve a primary-source interpretation, freeze the
network, flow, cut, capacity, binder, and boundary definitions, elaborate one exact Lean target
under minimal imports, and run the required mutations. The anchor audit, obligation tree, proof,
validation, and release tasks remain dependency-ordered and open. Intake grants none of their
state.
