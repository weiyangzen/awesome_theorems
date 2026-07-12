# Scope map

## Included topic boundary

- A source-exact weighted inequality assumed at one fixed exponent for every weight in the
  corresponding Muckenhoupt class.
- The source's family of nonnegative function pairs or named operator, with its exact measurability
  and finiteness conditions.
- The precise extrapolated exponent range, weight classes, norm or integral inequality, and
  dependence of the resulting constant.
- The underlying Euclidean or source-specified measure space and the exact averaging convention.

## Decisions required at statement freeze

The phrase "extrapolation of weighted inequalities" leaves materially different propositions open:

1. the classical family-of-pairs formulation, extrapolating an `L^{p0}(w)` inequality valid for
   every `A_{p0}` weight to `L^p(w)` for every `1 < p < infinity` and `w` in `A_p`;
2. an operator formulation derived from such a family, whose linearity or sublinearity assumptions
   and admissible functions must be explicit;
3. a quantitative version tracking dependence on the Muckenhoupt characteristic;
4. vector-valued, off-diagonal, limited-range, variable-exponent, or endpoint extrapolation.

The statement phase must inspect an immutable source and fix the starting exponent, all ordered
quantifiers, the exact `A_p` definition, dimension and averaging sets, weight regularity and
positivity, function class, treatment of infinite integrals, target exponent range, and constant
dependencies. It must decide whether the result is qualitative or quantitative and whether the
pair family may depend on the weight.

## Explicit exclusions

- A proof of one weighted inequality at one exponent without the extrapolation conclusion.
- Muckenhoupt's maximal-operator characterization, reverse Holder self-improvement, or the Rubio de
  Francia iteration algorithm alone as a substitute for the extrapolation theorem.
- Vector-valued, endpoint, off-diagonal, limited-range, or variable-exponent extensions unless the
  selected source makes one the canonical claim.
- An arbitrary operator assumed bounded at every target exponent, which would make extrapolation
  tautological.
- Unweighted interpolation or density-change identities as the target theorem.
- The repository label `已验证` as human-source or kernel-proof evidence.

No canonical Lean target is frozen at intake because the supplied wording does not select one.
