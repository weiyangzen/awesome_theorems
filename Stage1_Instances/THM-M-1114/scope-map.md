# Scope map

## Included theorem family

- The classical Erdos-Renyi random graph on finitely many labeled vertices, not an arbitrary
  deterministic graph.
- A sparse asymptotic regime customarily parameterized by edge probability of order `1/n`.
- A component whose vertex count is linear in the total vertex count in the supercritical regime.
- Quantified probability tending to one (or an exact source-equivalent asymptotic formulation),
  including existence, size, and uniqueness only to the extent stated by the selected source.
- The threshold contrast with non-giant components if that contrast belongs to the selected root.

This identifies a theorem family rather than an exact proposition. The later statement must not
infer omitted constants, error rates, or probability modes from this map.

## Decisions required before exact statement credit

The statement phase must freeze:

- `G(n,p)` versus the random graph process, and whether graphs are simple, undirected, and labeled;
- the parameterization (`p = c/n`, mean degree, or process time) and the precise ranges of `c`;
- whether the root includes both `c < 1` and `c > 1`, only supercritical appearance, or a critical
  window result;
- the exact largest-component bounds, the positive density equation if present, uniqueness, and
  bounds on all remaining components;
- the limiting mode and quantifier order, including fixed `c`, epsilon/delta binders, and the
  meaning of "with high probability";
- boundary cases such as `c = 1`, small `n`, empty graphs, rounding conventions, and ties between
  largest components.

Universes, finite graph types, probability measures, connected-component cardinality, asymptotic
filters, measurability, imports, and all typeclass assumptions must then be fixed in Lean.

## Explicit exclusions

- The connectivity threshold near `p = log(n)/n`, which is a neighboring but different theorem.
- Merely proving that some deterministic graph has a large connected component.
- Replacing a linear-size conclusion with a weaker unbounded-size or positive-probability claim.
- A branching-process survival theorem without checked transport to the random-graph statement.
- A finite computation, Monte Carlo observation, expected-size estimate, or concentration bound
  that does not imply the selected asymptotic theorem.
- Treating the repository's untrusted `已验证` label as source or machine-proof evidence.

## Mutation obligations for the statement phase

At minimum, mutation checks must cover removing the regime hypothesis, changing `G(n,c/n)` to a
deterministic graph or a different edge scale, moving the probability limit across quantifiers,
replacing linear size by nonemptiness, and testing the critical boundary `c = 1`. Non-equivalent
mutations must not receive statement identity or proof credit.
