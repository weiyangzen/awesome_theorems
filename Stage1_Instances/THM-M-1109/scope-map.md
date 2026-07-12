# Scope map

## Repository claim boundary

The repository phrase "universality phenomena of random matrices" names a research program, not a
single proposition. It leaves open all choices that determine a theorem:

- the ensemble (real symmetric or complex Hermitian Wigner, generalized Wigner, invariant,
  covariance, sparse, or another model) and the scalar field;
- entry independence, centering, variance profile, symmetry class, moment or tail assumptions, and
  any comparison or matching conditions;
- the observable (bulk gaps, correlation functions, edge eigenvalues, eigenvectors, or another
  statistic), its ordering and multiplicity conventions, and its rescaling;
- bulk energy, spectral edge, or crossover regime, including uniformity and averaging windows;
- the reference law or comparison ensemble, dimension limit, quantifier order, and convergence
  mode; and
- whether the result is fixed-energy, energy-averaged, vague/weak convergence, convergence of
  correlation functions, or convergence in distribution of a finite statistic.

These choices change both hypotheses and conclusion. The intake does not infer them from the word
"universality."

## Candidate root families requiring source selection

| Family | Typical observable and conclusion | Intake disposition |
|---|---|---|
| bulk local statistics | rescaled gaps or correlation functions converge to the GOE/GUE bulk law | candidate only; fixed-energy versus averaged variants differ |
| edge universality | rescaled extreme eigenvalues converge to an Airy/Tracy-Widom law | candidate only; must not substitute the separate Tracy-Widom target |
| comparison universality | two ensembles have asymptotically matching local statistics under moment or flow hypotheses | candidate only; the Tao-Vu four-moment target is separate |
| eigenvector universality | suitably normalized eigenvector coordinates have a universal limiting distribution | candidate only; not implied by eigenvalue universality |
| global spectral convergence | empirical measures converge to a macroscopic law | excluded by default; Wigner and Marchenko-Pastur laws have separate targets |

## Statement-phase gate

The statement phase must inspect a stable primary source and select one exact numbered theorem or
precisely located displayed result. It must justify why the proposition belongs to this umbrella
item rather than `THM-M-1105` (semicircle), `THM-M-1106` (Marchenko-Pastur), `THM-M-1107`
(Tracy-Widom), `THM-M-1110` (Erdos-Schlein-Yau), or `THM-M-1111` (Tao-Vu four moment).

It must then freeze ordered binders, universes, probability spaces or matrix laws, symmetry class,
entry and regularity assumptions, eigenvalue ordering, normalization, energy/edge regime,
observable, reference law, test-function class, convergence predicate, rates and uniformity,
degenerate dimensions, and all boundary cases. Only afterward may it select Lean matrix,
probability-measure, spectrum, point-process, and asymptotic interfaces.

Forbidden substitutions include a deterministic spectral theorem, a global empirical law, a
finite numerical experiment, a structure that stores the desired convergence as a field, or a
neighboring named theorem without a checked equivalence to the selected source proposition.
