# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0811` | frozen |
| execution item | `S56-M-0811-INTAKE`, rank 1370 | frozen |
| catalog name | `欧拉路径定理` | frozen as source wording |
| catalog claim | `欧拉路径存在的充要条件` | frozen literally |
| English identity | necessary and sufficient conditions for an Eulerian path/trail | theorem family only |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The intake preserves a genuine characterization of Eulerian-trail existence. It does not replace
that root with the definition of an Eulerian trail or with only a necessary parity result.

## Candidate theorem variants

The catalog is compatible with several materially different standard propositions. The statement
phase must choose one only after source review.

1. A finite connected undirected graph has a closed Eulerian trail iff every vertex has even
   degree.
2. A finite connected undirected graph has an open Eulerian trail iff exactly two vertices have
   odd degree, with those vertices as the endpoints.
3. A finite undirected graph has an Eulerian trail, allowing a circuit, iff its non-isolated
   vertices lie in one connected component and it has zero or two odd-degree vertices.
4. A fixed-endpoint version characterizes existence of an Eulerian trail from `u` to `v` by the
   parity of every vertex together with an appropriate connectivity condition.

These forms are related but not identical at empty graphs, edgeless graphs, graphs with isolated
vertices, and the case `u = v`. No equivalence is credited at intake.

## Decisions required at statement freeze

1. Choose finite simple graphs, finite multigraphs, or directed graphs. Euler's bridge problem has
   parallel bridges, while mathlib's probed `SimpleGraph` model has no loops or parallel edges.
2. Decide whether "path" means a trail using every edge exactly once, whether circuits count as
   paths, and whether vertex-simple paths are explicitly excluded from the intended terminology.
3. Select an existential-endpoint or fixed-endpoint formulation and state the endpoint order.
4. State the exact connectivity premise: connected graph, preconnected graph, connectivity of the
   support/non-isolated induced subgraph, or an equivalent edge-support condition.
5. Fix the finiteness representation and decide whether finiteness of vertices, edges, or both is
   assumed or derived.
6. Freeze the parity condition: all degrees even, exactly two odd degrees, zero-or-two odd degrees,
   or pointwise parity relative to fixed endpoints.
7. Specify universes, ordered binders, typeclass assumptions, decidability, and all checked
   transports between accepted encodings.
8. Select the foundation, TCB, computation, and freshness profiles for the exact target.

## Boundary cases

No case is excluded at intake. Source and statement review must settle:

- empty and singleton vertex types;
- the edgeless graph and a graph consisting only of isolated vertices;
- one nontrivial edge component plus arbitrary isolated vertices;
- zero versus two odd-degree vertices;
- equal versus distinct endpoints;
- a single edge, cycles, paths, and disconnected unions of edge-bearing components;
- simple-graph encodings of historically parallel edges;
- loops or directed edges if a broader graph model is selected.

## Explicit exclusions

- `THM-M-0810`, Euler's planar-graph formula, and other unrelated Euler theorems.
- The handshaking lemma or even cardinality of odd-degree vertices as a substitute for Eulerian
  trail existence.
- `SimpleGraph.Walk.isEulerian_iff`, which characterizes when an already supplied walk is
  Eulerian; it does not construct a walk from graph-level degree and connectivity conditions.
- Only the implication from Eulerian trail to parity, without the converse demanded by an iff.
- Hamiltonian paths or cycles, Chinese-postman problems, route algorithms, or directed variants
  substituted without a source-approved transport.
- A structure, walk, connectivity fact, or Eulerian witness assumed as input and then projected.
- The catalog's untrusted `已验证` label, a theorem name, `#check`, source URL, or historical
  attribution treated as source fidelity or kernel-proof evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.SimpleGraph.Trails` defines `SimpleGraph.Walk.IsEulerian`, proves its trail
and edge-coverage characterizations, and derives endpoint parity and the zero-or-two odd-degree
condition. Its module TODO explicitly requests the converse from that condition. Connectivity APIs
exist in `Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected`, but no composition with the
missing converse is credited.

This is bounded intake discovery, not an exhaustive anchor audit or a proof of global absence. The
next task must independently select and review an exact modern source proposition, freeze a
binder-complete Lean target with minimal imports, and run the required statement mutations.
