# Scope map

## Included claim

- A stochastic differential equation with a fixed state space, driving noise, initial law, and a
  precisely selected weak/strong solution concept.
- Weak existence: a solution exists on some stochastic basis with the prescribed laws.
- Pathwise uniqueness: two solutions on the same stochastic basis with the same driving noise and
  initial datum are indistinguishable in the source-specified sense.
- Strong existence: a solution can be constructed as a measurable functional of the prescribed
  input/noise, using the exact filtration and completion conventions of the source.
- Uniqueness in law only with the assumptions and placement verified from the selected theorem.

## Decisions deferred to statement phase

The primary source must fix finite versus infinite horizon, Euclidean versus more general state
space, Brownian or broader noise, coefficient measurability and integrability, filtered-space usual
conditions, initial-data coupling, equality up to indistinguishability, and whether the theorem is
one implication or a collection of implications/equivalences. Degenerate time intervals, null-set
completion, explosion, and weak versus strong uniqueness must be made explicit. Binder order,
universes, and the concrete Lean encoding follow those decisions.

## Explicit exclusions

- Replacing pathwise uniqueness by uniqueness in law.
- Proving only a Lipschitz-coefficient existence-and-uniqueness theorem.
- Treating a finite/discrete stochastic recursion as the continuous-time theorem.
- Assuming the desired measurable solution functional or strong solution as structure data.
- Crediting `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_231.lean` as terminal closure.

The statement must eventually use concrete probability-space, filtration, stochastic-integral,
SDE-solution, law, and almost-sure equality interfaces, or identify a precise missing API.
