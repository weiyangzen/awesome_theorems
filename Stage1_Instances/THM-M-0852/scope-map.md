# Scope map

## Received Scope

The repository fixes the title `Hamilton圈阈值`, the gloss `随机图中Hamilton圈的存在性`, a
collective twentieth-century attribution, and the untrusted label `已验证`. This identifies a
random-graph Hamiltonicity threshold family, not a truth-valued proposition.

An eventual statement may concern the appearance of a spanning cycle in a random graph only after
a reviewed source fixes all of the following:

- the probability model: independent-edge `G(n,p)`, uniform fixed-edge `G(n,m)`, or the coupled
  random graph process;
- finite labelled simple undirected graphs and the precise vertex type;
- the convention for a Hamilton cycle, including graph orders zero, one, and two;
- the parameter regime and binder order among `n`, `p = p(n)`, `m = m(n)`, and any real window
  parameter;
- the conclusion strength: probability tending to zero or one, an explicit limiting probability,
  a sharp threshold, a critical-window law, or equality of stopping times;
- logarithm, rounding, strict-inequality, and small-`n` conventions;
- whether convergence is pointwise in a window parameter, uniform, or expressed through a filter;
- whether minimum degree, isolated vertices, connectivity, or another event is a proved bridge or
  part of the theorem statement.

These are candidate scope components, not a selected canonical claim.

## Material Ambiguities

1. `G(n,p)` and `G(n,m)` are different probability laws; a process hitting-time theorem carries
   still more coupling data.
2. A sufficient upper bound for Hamiltonicity with high probability is weaker than a two-sided or
   sharp threshold theorem.
3. A critical-window limit distribution is not interchangeable with a bare zero-one limit.
4. "Existence" may mean a positive-probability finite theorem, probability tending to one, or an
   almost-sure process statement.
5. Threshold formulas near `(log n + log log n) / n` depend on exact centering, parameterization,
   and rounding; none is present in the repository record.
6. Mathlib's `SimpleGraph.IsHamiltonian` treats a singleton graph as Hamiltonian by convention,
   while empty and two-vertex simple graphs behave differently. A source crosswalk must decide
   whether these finite boundary cases are included or excluded.

## Explicit Exclusions

- Dirac's, Ore's, Chvatal-Erdos's, or another deterministic degree/connectivity criterion used as
  a replacement root; these are different theorems and several have separate catalog IDs.
- The random-graph connectivity threshold, giant-component theorem, or general phase transition,
  which are separately cataloged.
- The definition of `G(n,p)` or of Hamiltonicity by itself.
- A coarse or one-sided sufficient estimate substituted for a source-selected sharp threshold,
  critical-window, or hitting-time result.
- A finite numerical experiment, simulation, asymptotic heuristic, or unchecked probability
  computation as theorem evidence.
- A structure, hypothesis, or axiom that assumes the desired Hamiltonicity probability statement.
- The catalog label `已验证` as human-source or machine-proof evidence.

## Formal Boundary

No canonical Lean expression, minimal import set, expression hash, or environment fingerprint is
frozen at intake. The two probed mathlib modules provide a graph event and an independent-edge
measure, but do not choose the probability model or asymptotic theorem. Measurability of the exact
event, threshold definitions, convergence encoding, transports, and statement mutations belong to
the dependent statement phase after a proposition-level source is selected.
