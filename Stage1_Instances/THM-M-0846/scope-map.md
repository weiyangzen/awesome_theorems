# THM-M-0846 scope map

## Received scope

The authoritative target inventory names `图极限理论` in combinatorics/graph theory and gives only
`图序列的极限`. The attribution and year strongly identify Lovasz-Szegedy dense graph limits, but
the wording does not select one theorem from that theory. Intake preserves this family and refuses
to fill the missing proposition from memory.

## Candidate roots not selected

The inspected primary source exposes at least these materially different candidates:

- every convergent dense simple-graph sequence has a symmetric measurable `[0,1]^2 -> [0,1]`
  limit object reproducing all homomorphism-density limits;
- conversely, every such symmetric measurable function is the limit object of an appropriate
  simple-graph sequence;
- the full five-way Theorem 2.2 characterization by limit sequences, measurable limit objects,
  reflection positivity, positive-semidefinite connection matrices, and nonnegative Mobius
  transform; and
- almost-sure convergence of the source-defined random graphs `G(n,W)` to `W` (Corollary 2.6).

The catalog does not say whether the target is one implication, the equivalence, all five
characterizations, the random construction, or a larger body of theory. None is canonical here.

## Proposition-changing choices

An exact downstream statement must freeze:

| Dimension | Choices that remain open |
|---|---|
| graph sequence | simple or weighted graphs, finite vertex types, loops, and whether vertex counts tend to infinity |
| density | homomorphism, injective, induced-subgraph, or unlabeled copy density, including normalization |
| convergence | pointwise convergence over every finite simple graph, connected test graphs only, or a metric topology |
| limit object | a symmetric measurable representative on `[0,1]^2`, a general probability space, or an equivalence class modulo measure-preserving transformations |
| equality | pointwise, almost-everywhere, weak isomorphism, equality of all densities, or cut-distance zero |
| conclusion | existence only, converse realization, uniqueness, five-way characterization, or random approximation |
| algebraic branch | exact normalization, multiplicativity, reflection positivity, connection matrices, and `f dagger` definitions |
| formal boundary | real-valued versus nonnegative extended-real integrals, measurability/integrability premises, classical choice, and quotient machinery |

The exact source edition, theorem locator, incorporated definitions, quantifier order, assumptions,
proof boundary, correction history, and independent review must also be fixed.

## Cases to resolve

- Empty graphs, singleton graphs, zero denominators, bounded-size sequences, and repeated blow-ups.
- Sparse sequences, for which the dense normalization collapses edge-containing test graphs to zero.
- Weighted graphs, loops, zero edge weights, and node weights whose sum is not normalized.
- Representatives differing on null sets or by measure-preserving relabeling.
- Nonmeasurable, nonsymmetric, or out-of-range functions and incomplete probability spaces.
- Whether graphons are raw functions or quotient objects, and what uniqueness statement is intended.

No case is excluded at intake. A structure field or hypothesis storing the desired limit object or
the full target conclusion would be circular.

## Neighbor and substitution exclusions

- `THM-M-0845` separately owns graph-homomorphism counting. Counting infrastructure alone is not a
  convergence or representation theorem.
- `THM-M-0847` separately owns `图on理论` (`graphon theory`). No definition, result, or evidence is
  shared until an accountable scope reviewer resolves the boundary.
- Szemeredi regularity, edge-density bounds, a single quasirandom example, or convergence of one
  scalar statistic is not the graph-limit representation theorem.
- A generic compactness theorem, Fubini theorem, measurable-function definition, or probability
  limit theorem is substrate only.
- The untrusted catalog label and discovery-only Lean probe supply no source or proof credit.

## Formal boundary

Pinned mathlib provides simple graphs, graph homomorphisms, finite edge density, Szemeredi
regularity, product measures, and Fubini integration. A bounded exact-topic search found no named
graphon or dense-graph-limit terminal declaration. This is intake discovery, not an exhaustive
anchor audit or an absence proof. Exact target selection, formal definitions, imports, transports,
mutations, candidate audit, obligation freezing, proof, composition, trust, readability, and
release evidence remain downstream work.
