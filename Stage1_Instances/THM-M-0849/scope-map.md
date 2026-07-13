# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-0849`, the title `相变现象`, the literal gloss
`随机图的相变` (phase transition in random graphs), the Erdos/Renyi attribution, and the year
1960. Importance and `已验证` are untrusted catalog metadata. The source phrase identifies a
phenomenon family, not a binder-complete proposition.

The inspected 1960 source gives a concrete candidate family. It fixes labelled simple graphs with
exactly `N` edges, sampled uniformly, and calls a property typical when its probability tends to one
as `n` tends to infinity. Its Section 9 synopsis concerns the order of the largest connected
component when `N(n)/n -> c`:

- subcritical `c < 1/2`: logarithmic order;
- critical `c = 1/2`: order `n^(2/3)`;
- supercritical `c > 1/2`: linear order, with a single giant component described there.

These are source-family candidates, not a selected canonical root. In this parameterization the
critical average degree is one but the critical edge-density ratio is `c = 1/2`.

## Decisions required at statement freeze

An approved source decision must fix all of the following:

- the entire three-regime Section 9 synthesis versus a selected numbered theorem such as 7a, 7c,
  9a, or 9b, including every incorporated earlier theorem;
- the historical uniform `Gamma(n,N)` law, a coupled graph process, or a modern independent-edge
  `G(n,p)` law, together with a checked transport if the source model changes;
- whether `N(n) ~ cn`, `N(n)/n -> c`, or another asymptotic premise is canonical, and the order of
  all binders over `c`, `eta`, auxiliary sequences, and `n`;
- the exact largest-component observable, tie convention, probability space, measurability, and
  meaning of asymptotic order;
- whether the conclusion is only an order classification, quantitative convergence, uniqueness of
  the giant component, component-type structure outside it, or a conjunction of these;
- constants, logarithm and rounding conventions, little-oh terms, strict inequalities, and the
  treatment of the critical boundary;
- every referenced definition and theorem, source proof boundary, correction or erratum, and
  independent review.

## Boundary and degenerate cases

Later statement mutations must cover at least empty and singleton vertex sets, `N = 0`, maximal
`N`, invalid `N > choose(n,2)`, `c = 0`, `c = 1/2`, finite `n` for which rounding or logarithms
matter, and ties between components of greatest size. No such case is excluded at intake because no
canonical proposition has been selected.

## Explicit exclusions

- The mere definition of a random graph, which is separately cataloged as `THM-M-0848`.
- Only the appearance of a giant component, separately cataloged as `THM-M-0850`.
- Connectivity near `N` of order `(n/2) log n`, separately cataloged as `THM-M-0851`.
- Hamiltonicity, planarity, fixed-subgraph, or other thresholds in the same paper.
- A `G(n,p)` theorem treated as notation for the historical `Gamma(n,N)` theorem without a checked
  probabilistic transport.
- A deterministic graph theorem, simulation, numerical observation, assumed structure field,
  axiom, placeholder, or the untrusted catalog label used as proof evidence.

## Neighbor-target ownership

`THM-M-1113` is a semantic near-duplicate: it has the same attribution and year and reverses the
title/gloss wording (`随机图相变` / `随机图的相变现象`). The generator retained both IDs, so
this worker does not merge them or import status, receipts, scope decisions, or proof credit. The
integration lane must decide their eventual relationship. Likewise, duplicate-looking giant-
component and connectivity records under other IDs remain separately owned.

## Formal boundary

No canonical Lean expression, minimal imports, expression hash, environment fingerprint, checked
alternate encoding, mutation result, obligation registry, or discovery protocol is frozen here.
The checked pinned APIs provide only an independent-edge measure and finite component substrate.
They do not encode the historical fixed-edge distribution or prove a phase transition.
