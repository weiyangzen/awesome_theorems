# Scope map

## Repository claim boundary

The repository supplies the title "random matrix theory," attributes it to Eugene Wigner in 1955,
and describes it only as "eigenvalue distributions of random matrices." Those fields determine a
subject and historical lead, not a proposition. In particular, they leave open:

- the ensemble: real symmetric, complex Hermitian, Gaussian, Wigner, covariance, or another class;
- finite matrix size, an indexed sequence of sizes, entry independence, centering, variance, and
  moment or tail hypotheses;
- the spectral observable: joint eigenvalue law, empirical spectral measure, extreme eigenvalue,
  spacing statistic, or expected density of states;
- normalization and eigenvalue ordering conventions; and
- whether the conclusion is an exact finite-dimensional density or an asymptotic result, and if
  asymptotic, its limiting measure and mode of convergence.

The intake freezes these missing choices. It does not infer a theorem from the generic title.

## Candidate root families requiring source selection

| Family | Typical object | Typical conclusion | Intake disposition |
|---|---|---|---|
| finite Gaussian-ensemble eigenvalue law | GOE/GUE matrix of fixed size | a joint eigenvalue density, including the Vandermonde factor | candidate only |
| global empirical spectral law | normalized Wigner-type matrices as dimension tends to infinity | convergence of empirical spectral measures | candidate only; the Wigner semicircle law is separately `THM-M-1105` |
| local or extreme spectral statistics | rescaled eigenvalue gaps or largest eigenvalue | a limiting point process or edge distribution | excluded absent a source; neighboring targets cover Tracy-Widom and universality |
| sample-covariance spectrum | rectangular data matrices and covariance eigenvalues | a Marchenko-Pastur limit | excluded as the separately listed `THM-M-1106` |

## Statement-phase gate

The next phase must inspect a stable primary source and select one exact numbered proposition whose
scope is justified against the neighboring target IDs. It must freeze ordered binders, scalar
field, matrix symmetry, probability space or law, entry assumptions, scaling, eigenvalue encoding,
spectral measure, convergence mode, normalization, all boundary cases, and the conclusion. Only
then may it choose Lean matrix, probability-measure, eigenvalue, and weak-convergence interfaces.

Explicitly forbidden substitutions are: the spectral theorem for a deterministic matrix; a result
about expected trace with no checked implication to the selected eigenvalue distribution; a
structure that stores the desired law as a field; or the Wigner semicircle, Marchenko-Pastur,
Tracy-Widom, or universality theorem merely because it is a familiar random-matrix result.
