# Scope map

## Repository boundary

The repository record names Jean Bourgain, gives the year 2003, and says only that the theorem
concerns a relationship between the sizes of a sumset and a product set. At intake, this supports
the following common subject vocabulary only:

- a set `A` in an ambient additive and multiplicative structure;
- the sumset `A + A` and product set `A * A`;
- a quantitative assertion that at least one of these sets is large;
- hypotheses preventing degenerate subring or concentration behavior.

These bullets are not a canonical statement.

## Required source decision

The statement phase must select and independently inspect one immutable primary-source theorem.
In particular, it must distinguish at least these materially different readings:

1. a discretized sum-product estimate for a finite or scale-separated subset of the real line;
2. the Bourgain-Katz-Tao finite-field estimate for `A` in a prime field under a cardinality range;
3. the Erdős-Volkmann/Katz-Tao ring-conjecture result for subsets of the reals with Hausdorff
   dimension, rather than finite cardinality, as the size notion;
4. a later or specialized inequality customarily called a Bourgain sum-product theorem.

The selected passage must freeze the ambient domain, finite/compact/measurable assumptions,
sumset and product-set conventions, size notion, constants and their dependencies, quantifier
order, epsilon or scale ranges, non-concentration assumptions, and exact lower-bound conclusion.
It must also decide empty/singleton sets, whether zero may occur, small characteristics, endpoint
exponents, and any sufficiently-large threshold.

## Explicit exclusions

- The general Erdős-Szemerédi sum-product conjecture as a substitute for a proved Bourgain result.
- The Bourgain-Katz-Tao finite-field theorem as a substitute for a real/fractal theorem, or the
  reverse, without a source selection establishing that reading.
- Elekes's or Solymosi's later bounds merely because the repository contains adjacent entries for
  them.
- A weak tautology such as `max |A+A| |A*A| >= |A|`, or an abstract hypothesis that assumes the
  desired lower bound.
- `IntakeProbe.lean` pointwise-set syntax as a theorem statement or proof.
- The repository label `\u5df2\u9a8c\u8bc1` as human-proof, formal-proof, or release evidence.
