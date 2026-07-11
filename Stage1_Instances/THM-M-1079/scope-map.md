# Scope map

## Frozen object family

The target concerns a discrete-time martingale difference sequence on a probability space with a
filtration. Under the common forward convention, a sequence `D n` is integrable and measurable at
time `n + 1`, and its conditional expectation given information at time `n` vanishes almost
everywhere. An alternative same-index convention shifts these indices. The statement phase must
select one convention from an exact source and exhibit any transport to another encoding.

The codomain is not silently fixed. A real-valued formulation is the conservative first candidate;
a Banach-valued conditional-expectation formulation is stronger and may require additional
measurability and integrability assumptions.

## Candidate theorem roots

The source phrase "properties" does not select among these distinct claims:

1. Partial sums of a martingale difference sequence form a martingale.
2. Successive increments of a martingale form a martingale difference sequence.
3. Distinct square-integrable differences are orthogonal in `L2`.
4. A square-integrable partial sum satisfies the variance/isometry identity.
5. Limit, convergence, or concentration results under additional hypotheses.

The first two form a natural characterization pair, but intake does not promote that preference to
the canonical theorem. The statement phase must recover an exact source proposition or record a
hard source-identification blocker rather than combine several properties into a stronger root.

## Required statement decisions

- Exact property, source edition and location, and whether one direction or an equivalence is named.
- Index type, initial value, predecessor/current sigma-algebra convention, and partial-sum bounds.
- Scalar or Banach codomain; strong measurability, integrability, and almost-everywhere equality.
- Filtration direction and completion convention; probability versus sigma-finite measure.
- Boundary behavior at index zero and the empty sum.
- Lean binders, universes, minimal imports, foundation profile, and checked transports.

## Explicit exclusions

- Azuma, Azuma-Hoeffding, or another concentration inequality; those require boundedness or tail
  hypotheses and are separately represented by neighboring targets.
- A generic independent mean-zero sequence unless adaptedness and the conditional-mean condition
  required by the selected martingale-difference definition are proved.
- A continuous-time local-martingale increment statement.
- A structure whose field assumes the desired partial-sum or increment theorem.
- Any theorem obtained by adding square integrability, bounded increments, independence, or a real
  codomain unless those restrictions occur in the selected exact source statement.
