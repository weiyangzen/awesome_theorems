# Scope map

## Included theorem family

- A concrete size-indexed finite-dimensional random-matrix ensemble with a fully specified law.
- A concrete observable: preferably a normalized partition function, or alternatively one exact
  eigenvalue correlation/gap observable selected by the primary source.
- Explicit deformation parameters and the source's normalization conventions.
- An equality, differential identity, or recurrence identifying that observable with a named
  integrable object such as a Toda-hierarchy tau function or a Painleve solution.
- All finite-size, regularity, convergence, and boundary/initial conditions needed by the selected
  theorem.

## Decisions required by the statement phase

The source must select the ensemble (for example Hermitian/unitary rather than an unspecified
"random matrix"), potential and admissibility assumptions, matrix size, base measure, partition-
function normalization, deformation times, and whether the claim is finite-dimensional or
asymptotic. It must also select the integrable hierarchy/equation, dependent variable, derivative or
recurrence convention, and initial or boundary data. If the target instead uses a gap probability,
the interval, kernel/determinant representation, scaling regime, and Painleve branch must all be
fixed. These choices alter the proposition and cannot be supplied from convention alone.

## Explicit exclusions

- The bare assertion that random matrices are "related to" integrable systems.
- Substitution of the Wigner semicircle law, random-matrix universality, or a Tracy-Widom limit
  without a checked source mapping; those have separate repository targets.
- A universal claim covering every random-matrix ensemble or every integrable system.
- Defining an abstract package that stores the desired equality, differential equation, or tau
  property as an assumption.
- Numerical agreement, physical evidence, or a source citation as Lean kernel closure.

The later Lean target must expose the actual matrix-valued probability law, observable,
normalization, integrable equation/hierarchy, and source hypotheses, or record a precise API blocker
for each missing component.
