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

## Frozen mathematical boundary

The statement phase selects the inspected paper's Theorem 1 rather than a modern directed-flow
substitute. These choices are represented in `Statement.lean`.

| Component | Frozen statement decision | Remaining review boundary |
|---|---|---|
| graph | `Graph V E` over finite ambient vertex and arc types | graph-complex equivalence; loops are inert but historical convention review remains open |
| terminals | distinct `source` and `sink`, both in `G.vertexSet` | none inside the selected encoding |
| capacities | strictly positive `NNReal` on every graph arc | source word "number" to nonnegative-real-subtype review |
| chain | positive-length injective vertex and arc arrays with consecutive `Graph.IsLink` witnesses | historical sequence-notation transport review |
| flow | `Finsupp` from source-to-sink chains to `NNReal` | repeated equal components normalize by addition |
| feasibility | each graph-arc load is at most its capacity | none inside the selected encoding |
| flow value | finite sum of component weights | none inside the selected encoding |
| disconnecting set | graph-arc set meeting every source-to-sink chain | no partition-cut equivalence is credited |
| cut capacity | sum of member capacities | all disconnecting sets are ranged over, as in Theorem 1 |
| conclusion | witnesses both extrema, universally compares them, and equates their values | proof and source acceptance remain downstream |

The familiar directed formulation with edge capacities and flow conservation may be equivalent to
a suitable translation, but it is not definitionally the 1956 paper's chain-flow proposition. It
requires an explicit, checked source and representation transport before it can be credited.

## Binder and boundary ledger

`statement.json` freezes the exact domains, ordered binders, hypotheses, conclusion, direct imports,
environment, and expression fingerprints. The boundary decisions are:

- empty and no-path networks are included; the selected definitions make zero flow and the empty
  disconnecting set the intended witnesses, though this statement phase adds no boundary proof;
- equal terminals and terminals outside the graph are excluded by `HasTerminals`;
- loops, parallel arcs, disconnected vertices, and finite ambient nonvertices/nonedges are allowed;
  loops cannot occur in injective-vertex chains and their historical-source transport stays open;
- capacities are `NNReal` and strictly positive on graph arcs; component weights may be zero;
- repeated equal chain components combine in `Finsupp`, preserving total loads and value;
- circulations and dead-end flow are absent, as the paper explicitly notes;
- all disconnecting sets are ranged over, not only inclusion-minimal cuts;
- actual maximum and minimum witnesses are required;
- integrality and algorithm termination are excluded from this target.

The boundary mutation adds a source-to-sink-chain premise and is rejected as a different target.

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

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the statement imports only
`Mathlib.Algebra.BigOperators.Finsupp.Basic`, `Mathlib.Combinatorics.Graph.Basic`, and
`Mathlib.Data.NNReal.Defs`. Removing any one makes the module fail. All target-specific definitions
are local, and no max-flow/min-cut proof declaration is imported.

A bounded exact-topic search over repo-local Lean and pinned mathlib found no declaration matching
network flow or max-flow min-cut. This is intake discovery only, not a global absence claim or the
downstream immutable anchor audit.

## Gate boundary

`S56-M-0814-STATEMENT` now has a worker-self-tested canonical target, definition bundle, minimal
imports, direct respelling, and four mutation classes. Master acceptance remains pending. The
anchor audit, obligation tree, proof, validation, and release tasks remain dependency-ordered and
open; no downstream state is claimed.
