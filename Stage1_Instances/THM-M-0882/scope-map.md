# Scope map

## Catalog scope preserved

- Identity: `THM-M-0882`, named `Margulis构造` (Margulis construction).
- Attribution and date: Grigory Margulis, 1973.
- Literal gloss: `扩展图的显式构造` ("explicit construction of expander graphs").
- Category: combinatorics / graph theory.

This identifies a named result family, not a binder-complete proposition. Intake does not infer a
specific graph formula, expansion theorem, or constant from the name.

## Decisions required before statement freeze

| Surface | Unresolved choice | Why it changes the proposition |
|---|---|---|
| Source identity | original 1973 concentrator result, a later expander reformulation, or another Margulis construction | the objects, definitions, and conclusions need not coincide |
| Graph model | simple graph, directed/bipartite graph, multigraph, or Markov operator | loops, duplicate generators, degree, and adjacency semantics differ |
| Carrier | `(Z/nZ)^2`, another finite quotient, a bipartite pair, or a group quotient | modulus restrictions and cardinality laws differ |
| Generators | exact affine maps, inverses, symmetrization, and duplicate-edge policy | these determine the construction and regularity |
| Expansion | concentrator, vertex, edge, conductance, or spectral expansion | the predicates and constants are not definitionally interchangeable |
| Parameters | admissible moduli, degree, tested subset range, expansion constant, and normalization | changing any one changes the quantified claim |
| Family claim | one graph, infinitely many graphs, an unbounded uniform family, or every admissible modulus | quantifier order and uniformity differ |
| Explicitness | closed formula, uniform algorithm, effective computation, or merely nonprobabilistic existence | these are distinct construction guarantees |
| Boundary cases | small moduli, empty/singleton carriers, generator collisions, loops, and vacuous subset ranges | they can invalidate regularity or make expansion vacuous |

An admitted source must freeze all domains and universes, ordered binders, hypotheses, construction
data, conclusion, constants, exceptional cases, and any checked relationship between concentrator
and expander formulations before the statement phase encodes Lean.

## Candidate families not credited

- The degree-eight undirected Margulis graph on `(ZMod n) × (ZMod n)` using a remembered family of
  affine maps and their inverses.
- A Margulis-Gabber-Galil graph family with a positive uniform spectral, edge, or vertex expansion
  bound.
- The original 1973 explicit bounded concentrator construction.
- A Cayley or Schreier graph construction derived from property (T).

These are discovery candidates only. None is selected, stated, or credited at intake.

## Neighbor and substitution exclusions

- `THM-M-0881` owns the general existence/construction topic for expander graphs.
- `THM-M-0883` owns the Lubotzky-Phillips-Sarnak construction; `THM-M-0884` owns the general
  Ramanujan-graph topic; `THM-M-0885` and `THM-M-0886` own later named Ramanujan existence results.
- `THM-M-0887` spectral graph theory, `THM-M-0888` Cheeger inequality, and `THM-M-0100` property
  (T) may supply ingredients or consequences, but do not replace this construction.
- A graph structure whose fields assume the desired expansion conclusion, one finite computed
  example, random sampling, or a numerical eigenvalue check cannot close the root.
- The 1982 paper "Explicit constructions of graphs without short cycles and low density codes" is
  a distinct later work and cannot be substituted merely because author and terminology overlap.
- The catalog's `已验证` label, a title match, or the API probe supplies no source or proof credit.

## Formal boundary

Pinned mathlib exposes finite simple graphs, relation-based graph construction, neighborhoods,
degree and regularity, adjacency matrices, and `ZMod`. A bounded exact-topic search found no
Margulis, graph-expander, or concentrator target declaration. These are substrate and intake
discovery facts only, not a complete anchor audit, exact target, or proof.
