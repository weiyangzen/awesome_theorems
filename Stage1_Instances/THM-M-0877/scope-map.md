# Scope map

## Preserved catalog identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0877` | frozen |
| execution item | `S56-M-0877-INTAKE`, rank 1430 | frozen |
| catalog name | `网络流` | frozen literally |
| catalog gloss | `最大流与最小割理论` | frozen literally |
| attribution and date | many mathematicians, twentieth century | untrusted metadata |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The gloss is preserved as a family label. It is not normalized to the equality theorem, because
the catalog separately assigns that claim to `THM-M-0814`.

## Candidate roots not credited

The received wording could refer to materially different propositions:

1. Weak duality: every feasible source-to-sink flow value is at most every source-sink cut capacity.
2. Max-flow/min-cut equality for one exact finite capacitated-network model.
3. Existence of an optimizing flow and cut, rather than equality of suprema and infima.
4. Integrality of an optimum under integral capacities.
5. Characterization by absence of an augmenting path.
6. Correctness or complexity of Ford-Fulkerson, Edmonds-Karp, Dinic, or push-relabel.
7. A source-reviewed theorem-family ledger separating these results.

None is selected or credited at intake. A conjunction of convenient branches would broaden the
source, while selecting equality alone would collapse this record into the separately owned
`THM-M-0814` target.

## Proposition-changing decisions

Before statement elaboration, an accountable source decision must freeze:

- one immutable source edition and exact theorem or family-ledger boundary, with incorporated
  definitions, corrections, errata, proof boundary, and independent review;
- finite graph, multigraph, or incidence structure; directed versus undirected arcs; loops,
  parallel arcs, antiparallel arcs, and the representation of absent edges;
- distinct source and sink, their membership in the network, single versus multiple terminal
  pairs, and the treatment of source equal to sink;
- capacity codomain (`Nat`, `Rat`, `Real`, `NNReal`, or another ordered algebraic structure),
  positivity versus nonnegativity, and finite versus extended values;
- weighted path/chain decomposition versus edge flows with conservation, skew symmetry,
  circulations, and the exact definition of flow value;
- disconnecting arc sets versus vertex-partition cuts, crossing-edge orientation, inclusion
  minimality, and the exact cut-capacity sum;
- maximum/minimum attainment versus supremum/infimum, finiteness and decidability assumptions,
  binder order, and every coercion or typeclass assumption;
- empty graphs, no source-to-sink path, zero capacities and zero flow, isolated vertices, empty or
  repeated paths, and other degenerate cases; and
- whether integrality, algorithms, termination, runtime, certificates, or only the min-max theorem
  belongs to the selected root.

Each choice can change the proposition, so none may be inferred from the title or status label.

## Neighbor boundaries

- `THM-M-0814` separately owns the explicit gloss "the maximum value of a network flow equals the
  minimum cut capacity" and the Ford/Fulkerson 1956 attribution.
- `THM-C-0096` repeats a short max-flow/min-cut algorithm gloss in the computer-science catalog but
  is outside the 1546-target rev-5.6 manifest.
- `THM-M-0878` and `THM-M-0879` separately own minimum-cost and multicommodity flow topics.

These records help detect duplicate or adjacent scope. Their statements, source grades, Lean
artifacts, and proof credit do not transfer to this target.

## Explicit exclusions

- Weak duality, integrality, or one algorithmic special case presented as the entire family.
- The `THM-M-0814` equality theorem copied here without an approved duplicate-resolution decision.
- A structure field or hypothesis that stores the desired optimal flow, cut, or equality.
- A fixed-network computation, solver output, benchmark, oracle result, or unchecked certificate.
- Generic graph, digraph, sum, or maximum APIs used as if they define or prove network flow.
- The catalog label `已验证` used as human-source or kernel evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks undirected multigraph,
directed relation, finite-sum, and finite-maximum substrate. A bounded repo-local and pinned-mathlib
search found no max-flow, min-cut, network-flow, Ford-Fulkerson, or cut-capacity declaration. This
is an intake observation, not a complete immutable anchor audit or a global absence claim.
