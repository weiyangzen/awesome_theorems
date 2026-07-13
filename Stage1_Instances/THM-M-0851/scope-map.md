# THM-M-0851 scope map

## Received Scope

The repository fixes the title `连通性阈值`, the gloss `随机图连通的阈值`, the attribution
Erdos/Renyi, the year 1959, and the untrusted label `已验证`. This identifies a random-graph
connectivity-threshold family, not a binder-complete proposition.

An eventual exact statement must freeze all of the following:

| Dimension | Choices still open |
|---|---|
| graph law | uniform fixed-edge `G(n,m)`, independent-edge `G(n,p)`, or a coupled graph process |
| carrier | labelled finite simple graphs on `n` vertices, including the precise finite type and relabelling convention |
| event | connected versus preconnected, treatment of isolated vertices, and nonempty-carrier convention |
| parameters | edge count or edge probability, centering/scaling, integer rounding, and any real or extended-real window variable |
| binders | order and dependence among `n`, `m(n)`, `p(n)`, window parameters, and error sequences |
| strength | a one-sided high-probability result, zero-one threshold, sharp threshold, explicit critical-window law, or hitting-time law |
| convergence | pointwise limit, convergence in probability/distribution, filter formulation, or uniformity claim |
| boundary | `n = 0, 1, 2`, endpoint probabilities, impossible edge counts, logarithms, and strict versus nonstrict inequalities |

These are scope components, not selected binders or hypotheses.

## Material Ambiguities

1. The fixed-edge law used in the historical 1959 paper is not definitionally the independent-edge
   `G(n,p)` law available in pinned mathlib.
2. A coarse sufficient or necessary bound is weaker than a two-sided threshold and different from
   an explicit critical-window limiting probability.
3. A statement about a graph sampled at a fixed edge count differs from a stopping-time theorem for
   successively sampled edges, even when their scales are related.
4. "Threshold" may refer to connectivity itself, absence of isolated vertices, or a proved
   equivalence between their limiting behavior; none is selected in the catalog.
5. Mathlib defines `Connected` as `Preconnected` plus a nonempty vertex type. Thus the empty graph,
   singleton graph, and complete graph conventions must be crosswalked rather than assumed.
6. The conventional `log n` scale is not enough to determine constants, rounding, binder order, or
   whether the result is a zero-one law or a limiting distribution.

## Explicit Exclusions

- The giant-component and general random-graph phase-transition results, which have separate
  catalog targets.
- A Hamilton-cycle, minimum-degree, edge-connectivity, or deterministic graph-connectivity theorem
  used as the root.
- The definition of a random-graph law or connectivity predicate by itself.
- A `G(n,p)` theorem silently substituted for a fixed-edge or graph-process source statement, or
  conversely, without a checked transport.
- A one-sided estimate substituted for a source-selected sharp threshold or critical-window law.
- A simulation, finite enumeration, numerical approximation, assumed conclusion, axiom, or
  untrusted catalog status used as theorem evidence.

## Formal Boundary

No canonical Lean expression, minimal import set, elaborated-expression hash, environment
fingerprint, checked alternate encoding, or mutation certificate is frozen at intake. Pinned
mathlib supplies an independent-edge measure and a connectivity predicate only. It does not select
the historical probability model, threshold theorem, asymptotic encoding, event measurability
lemma, or model transport. Those decisions belong to the dependent statement phase after an exact
primary-source proposition is selected and independently reviewed.
