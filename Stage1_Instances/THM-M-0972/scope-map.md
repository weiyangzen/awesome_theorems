# THM-M-0972 scope map

## Received record

| Field | Frozen intake value | Authority boundary |
|---|---|---|
| ID | `THM-M-0972` | rev-5.6 target manifest |
| Name | Janson inequality | catalog title only |
| Attribution and date | Svante Janson, 1990 | uncited catalog metadata |
| Catalog gloss | probability of the union of rare events | not an exact proposition |
| Catalog status | verified | untrusted; no `H`, `M`, or `R` credit |
| Lane | `hard_statement_first_partial_verification` | scheduling metadata only |

The title and 1990 date identify a classical theorem family, but the gloss omits every binder,
definition, hypothesis, formula, and boundary convention. It also reverses the natural event in the
standard nonoccurrence form: `X = 0` says no indexed occurrence happens, hence is the complement of
their union.

## Candidate roots not yet selected

With an independently sampled random subset of a finite base set, a finite family of configurations,
indicators `I_A`, count `X`, mean `lambda`, overlap sum `Delta`, and
`DeltaBar = lambda + 2 * Delta`, the immutable secondary reference distinguishes:

1. the nonoccurrence form `P(X = 0) <= exp (-lambda + Delta)`;
2. the second nonoccurrence form `P(X = 0) <= exp (-lambda^2 / DeltaBar)`;
3. a Boppana-Spencer product refinement involving `max_A E[I_A]`;
4. Janson's 1990 lower-tail estimate for `0 <= t <= lambda`, with both an entropy-function bound
   and its quadratic weakening;
5. a possible conjunction of some or all source-selected bounds.

The statement phase must choose one source-defined proposition or an explicit conjunction. None of
these candidate formulas is the canonical statement in this intake.

## Proposition-changing choices

- homogeneous selection probability versus a coordinate-dependent probability family;
- a finite base type versus an ambient type with finite support;
- whether the configuration collection is a set, finset, indexed family, or multiset, and whether
  duplicate configurations are meaningful;
- subset-occurrence indicators versus arbitrary increasing events or arbitrary dependent events;
- whether empty configurations are allowed and how their deterministic indicator contributes;
- ordered overlap pairs with a factor `1/2` versus unordered pairs, and whether diagonal terms enter;
- overlap by nonempty intersection versus a separately supplied dependency relation;
- `ENNReal` measure versus real-valued probability and expectation;
- the exact definitions and codomains of `lambda`, `Delta`, `DeltaBar`, `epsilon`, and `phi`;
- nonoccurrence only, the full lower tail, a quadratic corollary, or a conjunction;
- treatment of zero denominators, zero mean, endpoint probabilities, and equality at thresholds;
- finite theorem versus an asymptotic corollary or a random-graph specialization.

## Boundary cases to resolve

- empty base set and empty configuration family;
- an empty configuration, repeated configurations, or a singleton configuration family;
- selection probabilities `0` and `1`;
- pairwise disjoint configurations, where `Delta = 0` and the count is independent;
- `lambda = 0`, `Delta = 0`, or `DeltaBar = 0`, especially in quotient forms;
- `t = 0`, `t = lambda`, and values outside the lower-tail range;
- configurations with full overlap or identical support under different indices;
- nonmeasurable generic-event encodings if the random-subset specialization is not selected.

No degenerate case is excluded until an exact source proposition is selected.

## Excluded substitutions

The following do not close this target unless an accepted source map proves exact identity:

- the elementary union bound for arbitrary rare events;
- a lower bound for the union probability obtained by complementing a nonoccurrence upper bound;
- the independent Chernoff or Hoeffding bound;
- the Lovasz local lemma, FKG inequality, or second-moment method;
- Suen's dependency-graph inequality for arbitrary indicators;
- a theorem only about `G(n,p)`, triangle counts, or another single application;
- construction of a Bernoulli random set or binomial random graph without a Janson bound;
- a definition or structure storing the desired inequality as a field;
- numerical estimates, simulation, or the catalog's untrusted `verified` label.

## Neighbor boundaries

`THM-M-0969` owns the Lovasz local lemma, `THM-M-0971` the Shearer bound, `THM-M-0975` the
Azuma-Hoeffding inequality, `THM-M-0977` the Chernoff bound, and `THM-M-0978` the Hoeffding
inequality. Those targets are related tools, not interchangeable roots. Suen's general
dependency-graph result is also explicitly separated by the inspected reference.

## Formal scope

Pinned mathlib contains useful substrate in:

- `Mathlib.Probability.Distributions.SetBernoulli`;
- `Mathlib.Probability.Independence.Basic`;
- `Mathlib.Probability.Moments.Basic`;
- `Mathlib.MeasureTheory.OuterMeasure.Basic`;
- `Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs`.

The probe checks representative declarations. They provide probability spaces, independence,
indicators, generic Chernoff bounds, union bounds, and a random-graph law; none is credited as a
Janson statement or proof. The binomial-random-graph module's unrelated `proof_wanted` for an edge
count also receives no credit. Minimal imports, exact expression, profiles, checked transports, and
all four required mutation classes remain statement-phase work.

An immutable `facebookresearch/atlas-lean` source snapshot contains exact-topic Janson I, II, and
III declarations at the same Lean and mathlib pins, but their root-relevant chains contain explicit
`sorry`. This is a placeholder-blocked `M5` candidate, not a usable formal artifact or root proof;
its CC BY-NC 4.0 plus no-training license is also an integration boundary. The downstream anchor
audit must recheck the complete project, statement relationship, provenance, trust, and license.
