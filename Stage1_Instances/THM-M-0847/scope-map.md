# THM-M-0847 scope map

## Received scope

The authoritative target inventory names `图on理论` in combinatorics and graph theory. Its only
mathematical gloss is "limit theory of large graphs." The attribution and year point to László
Lovász's 2012 graph-limit monograph, but the wording names a mathematical theory rather than a
specific theorem. Intake preserves that subject boundary and refuses to choose missing
mathematics.

## Candidate theorem families not credited

Graphon theory contains many non-interchangeable propositions, including:

- representation of a convergent dense graph sequence by a symmetric measurable kernel;
- the converse construction of graph sequences sampled from a graphon;
- equivalence of left convergence, homomorphism-density convergence, and cut-metric convergence
  under specified hypotheses;
- compactness of a graphon quotient under cut distance;
- uniqueness or weak isomorphism characterized by equality of homomorphism densities;
- counting, inverse-counting, regularity, approximation, sampling, concentration, and testability
  results;
- extremal optimization or finite forcibility statements over graphons.

The catalog selects none of these. A definition of graphon is not itself a theorem, and wrapping a
desired conclusion into a structure or hypothesis would be circular rather than proof.

## Proposition-changing choices

An exact downstream statement must freeze at least the following:

| Dimension | Choices that remain open |
|---|---|
| root result | definition, existence/representation, converse sampling, compactness, uniqueness, convergence equivalence, counting, approximation, or another numbered theorem |
| base space | canonical unit interval with Lebesgue probability measure or a general atomless/standard probability space |
| graphon object | pointwise measurable versus almost-everywhere measurable, symmetric pointwise versus almost everywhere, codomain `[0,1]` versus bounded real kernels |
| equality | pointwise equality, almost-everywhere equality, relabeling, weak isomorphism, or zero cut distance |
| finite graphs | simple, loopless, labeled/unlabeled, weighted, directed, or decorated graphs; whether isolated vertices are allowed |
| densities | homomorphism, injective homomorphism, induced, labeled, or unlabeled subgraph density and normalization |
| convergence | left convergence, density-wise convergence, cut norm/distance, sampling, or another topology |
| transformations | measurable maps, measure-preserving maps, invertible transformations, couplings, or common pullbacks |
| limits and quantifiers | sequences versus nets, vertex counts tending to infinity, every finite test graph, subsequences, and existence versus uniqueness |
| analytic conventions | representatives modulo null sets, product measure, integrability, separability, infima, and attainment |
| computation/trust | exact analytic proof, finite approximation, certified computation, randomized sampling, or oracle boundary |

The prospective core "every convergent dense graph sequence has a graphon limit" is only one
plausible member of the subject. It is especially unsafe to install silently because `THM-M-0846`
already owns the neighboring graph-limit label and the 2006 Lovász-Szegedy attribution.

## Cases to resolve

- Empty or singleton finite graphs and graph sequences whose vertex counts do not tend to infinity.
- Constant-zero and constant-one graphons, diagonal values, loops, and isolated vertices.
- Null-set changes and pointwise failures of symmetry or range bounds.
- Atomic probability spaces, zero-measure components, nonstandard spaces, and noninvertible maps.
- Pseudometric zero between distinct representatives and whether a quotient is required.
- Infima in cut distance that are not attained under a selected relabeling convention.
- Normalization when a test graph has no vertices or edges.
- Deterministic versus almost-sure conclusions for graphon sampling.

No case is excluded at intake because no proposition has been selected.

## Neighbor and substitution exclusions

- `THM-M-0845` separately owns graph-homomorphism counting. Its prospective density definitions or
  theorems cannot select this root or transfer proof credit.
- `THM-M-0846` separately owns graph limit theory and cites Lovász/Szegedy, 2006. The dense-graph
  representation theorem cannot be assigned here merely because graphons serve as limit objects.
- `THM-M-0843` separately owns Szemerédi's regularity lemma. Regularity infrastructure alone is
  not graphon theory or a graphon limit theorem.
- A finite simple-graph density theorem, measure-theory API, graphon datatype, example kernel,
  numerical approximation, random sample, or assumed convergence witness is not a substitute.
- The catalog's `已验证` label and discovery-only probe supply no H or M credit.

## Formal boundary

Pinned mathlib supplies finite simple-graph edge density, product measures, a canonical probability
measure on the unit interval, and measure-preserving maps. It does not thereby choose or define the
graphon object, its equivalence relation or metric, homomorphism densities, a convergence notion,
or a root theorem. The probe authenticates only that adjacent substrate. Exact target selection,
formal-anchor discovery, obligation freezing, proof bodies, composition, trust, readability, and
release evidence belong to later open phases.
