# Scope map

## Included claim family

- A centered, real-valued Gaussian process `(X_t)_(t in T)` on a probability space.
- A measurable, almost surely finite supremum `S = sup_(t in T) X_t`, obtained under the precise
  separability or countable-reduction hypotheses of the selected source.
- The variance proxy `sigma^2 = sup_(t in T) E[X_t^2]` (equivalently the supremum of pointwise
  variances for a centered process).
- Finiteness of `E[S]` under the theorem's hypotheses and a Gaussian upper-tail bound for
  `S - E[S]`, with exponent normalized as `-u^2/(2 sigma^2)` in the standard formulation.

This freezes a named claim family rather than an exact proposition. The repository source says only
"concentration of Gaussian processes" and does not select among standard one-sided, two-sided, or
absolute-supremum variants.

## Statement-phase decisions

The selected primary source must fix whether `T` is countable or the process is separable, and
whether the starting assumption is almost-sure boundedness of `sup X_t`, finiteness of
`E sup X_t`, or boundedness of `sup |X_t|`. It must also determine whether the conclusion is the
one-sided upper tail, a matching lower tail, a two-sided bound with factor `2`, or a statement for
`sup |X_t|`; none of these may silently substitute for another.

The formal target must expose the probability space, joint Gaussian predicate, centeredness,
measurability and integrability of the supremum, real versus extended-real supremum, binder order,
and all finiteness assumptions. It must explicitly handle the empty and singleton index sets,
`sigma^2 = 0`, `u = 0`, indistinguishable indices, and infinite variance suprema. A division by zero
may not be hidden by a convenient real-number convention.

## Explicit exclusions

- Gaussian concentration for a single Lipschitz function in finite-dimensional Euclidean space
  without the checked process-supremum specialization and limiting bridge.
- Dudley's entropy bound, Sudakov minoration, Slepian comparison, Fernique integrability, or a
  generic sub-Gaussian tail estimate as a substitute for Borell-TIS.
- A finite-index maximum inequality presented as the full separable-process theorem without a
  checked approximation and measurability argument.
- Assuming the desired concentration inequality as a field of an abstract structure or hypothesis.
- Treating the metadata label `已验证`, a theorem name, or a bibliography entry as Lean evidence.

A stronger general concentration theorem may be used downstream only through a checked
specialization whose hypotheses and exact conclusion crosswalk to the selected source statement.
