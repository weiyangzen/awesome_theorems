# Scope map

## Included topic boundary

- A source-exact definition of a Muckenhoupt `A_p` weight, including averaging sets and base
  measure.
- The source-named operator and its exact domain and codomain.
- The precise weighted norm assertion, exponent range, and dependence of the bound.
- Necessity, sufficiency, or equivalence only as stated by the selected source.

## Decisions required at statement freeze

The phrase "A_p weights and operator boundedness" leaves materially different propositions open:

1. strong `(p,p)` boundedness of the Hardy-Littlewood maximal operator characterized by `A_p` for
   `1 < p < infinity`;
2. an endpoint weak-type assertion for `A_1`;
3. sufficiency of `A_p` for a singular integral or another operator;
4. a qualitative existence of a constant versus a quantitative or sharp dependence on the `A_p`
   characteristic.

The statement phase must fix Euclidean dimension or the axioms of a metric measure space, balls or
cubes (and centered or uncentered maximal operator), real or complex functions, the weight's
measurability/local integrability/positivity assumptions, the weighted measure convention, and all
ordered quantifiers. It must decide the zero weight, null averaging sets, infinite averages,
`p = 1`, and `p = infinity` from the source rather than by convenience.

## Explicit exclusions

- Rubio de Francia extrapolation, reverse Holder results, and self-improvement as substitutes.
- A weighted bound for an unnamed generic operator assumed to be bounded; that would be tautological.
- An unweighted `L^p` maximal inequality or a measure-with-density identity as the target theorem.
- Sharp constants or endpoint estimates not present in the selected source.
- The repository label `已验证` as human-source or kernel-proof evidence.

No canonical Lean target is frozen at intake because the supplied wording does not select one.
