# Scope map

## Repository claim boundary

The repository supplies only the Chinese title "Gaussian comparison inequality," the description
"comparison theorem for Gaussian processes," a twentieth-century date, and an attribution to
"many mathematicians." That metadata identifies a theorem family, not a proposition. In
particular, it does not determine:

- whether the input is a finite Gaussian vector, a separable Gaussian process, a Gaussian measure
  on a Banach space, or a Gaussian min-max array;
- whether the hypothesis orders coordinate covariances, increment variances, covariance
  operators, or mixed min-max covariances;
- whether the conclusion compares threshold probabilities, expected suprema, convex-set
  probabilities, or expected min-max functionals;
- centering, equal-variance, separability, measurability, finiteness, compactness, or degeneracy
  assumptions; or
- the direction and strictness of either inequality.

The intake therefore freezes the ambiguity rather than silently choosing a familiar variant.

## Candidate root families requiring selection

| Family | Characteristic hypothesis | Characteristic conclusion | Intake disposition |
|---|---|---|---|
| Slepian comparison | equal coordinate variances plus an order on off-diagonal covariances | threshold distribution comparison for a finite maximum | candidate only; separately named as `THM-M-1085` in this repository |
| Sudakov-Fernique comparison | order on expected squared increments | order on expected suprema | candidate only; no source selection |
| Gordon comparison | row/column covariance inequalities for Gaussian arrays | expected or probabilistic min-max comparison | candidate only; materially different binder structure |
| Anderson inequality | centered Gaussian measure plus a symmetric convex set and translation/covariance comparison | comparison of Gaussian set probabilities | candidate only; not process-supremum syntax |

These families are not interchangeable. A stronger-looking result may have different hypotheses
and does not count as the root without a source-checked implication to the selected statement.

## Statement-phase requirements and exclusions

The statement phase must inspect a stable primary source, select one exact numbered theorem, and
transcribe every ordered binder, domain, hypothesis, conclusion, normalization, constant, and
boundary case. It must explain why that theorem, rather than the separately listed Slepian item or
another comparison family, matches the repository record. Only then may it choose Lean objects for
joint Gaussianity, covariance or increment variance, finite/uncountable suprema, expectation, and
event probability.

Excluded substitutions include a scalar normal-tail bound, an independent-coordinate lemma, a
concentration inequality such as Borell-TIS, an entropy bound, and any structure that assumes the
desired comparison as a field. Empty index sets, singleton processes, singular covariance, and
zero-variance coordinates must be resolved by the selected source, not discarded for API
convenience.
