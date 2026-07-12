# Source-statement crosswalk

## Available repository source record

`Docs/researches/math_theorems.md` supplies the title "Gibbs sampling", attribution to Stuart Geman
and Donald Geman, year 1984, and the phrase "MCMC by conditional sampling". The same inventory row
appears twice. `Docs/Stage0_Blueprint.md` repeats that metadata while leaving the exact definitions,
hypotheses, proof process, dependencies, axioms, and machine artifacts open. Neither record gives a
bibliography, theorem number, page, exact conclusion, or errata history.

The label `已验证` is explicitly untrusted in the rev-5.6 target manifest. It is not evidence of a
human proof or Lean kernel closure.

## Historical source candidate

Stuart Geman and Donald Geman, "Stochastic Relaxation, Gibbs Distributions, and the Bayesian
Restoration of Images", *IEEE Transactions on Pattern Analysis and Machine Intelligence*,
PAMI-6(6), 721-741 (1984), is the natural historical source candidate matching the repository's
authors and year. At intake it is only a bibliographic discovery anchor: its exact theorem wording,
page, assumptions, relation to the later generic term "Gibbs sampler", and errata have not been
inspected from a stable edition. It therefore cannot support `H0` or select the canonical target.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "Gibbs sampling" | an update method based on conditional laws | exact transition kernel on a product measurable space | family identified; proposition open |
| "conditional sampling" | coordinates or blocks are resampled conditionally | regular conditional probability kernels and their measurability | included; hypotheses open |
| "MCMC" | repeated updates form a Markov chain intended for sampling | kernel iteration, initial law, and target measure | included; conclusion open |
| Geman/Geman, 1984 | historical attribution and candidate paper | immutable edition and theorem/page crosswalk | candidate only |
| `已验证` | repository screening metadata | accepted source review or kernel receipt | no credit |

## Non-equivalent candidate statements

Several useful results could fit the topic label but are not interchangeable: a coordinate-update
kernel preserves the joint target; a complete sweep preserves it; random-scan updates may be
reversible; a chain under additional support and recurrence hypotheses converges to the target; or
ergodic averages converge. Each requires different binders and assumptions. Choosing any one before
the source identifies it would broaden or substitute the target.

The first downstream gate is therefore source-statement identity. Before `H0`, an independent
reviewer must verify a stable edition, exact theorem/page, definitions, assumptions, conclusion,
and errata, and approve a row-by-row mapping to the canonical Lean expression. Before any `M0`
claim, that expression and its imports must elaborate in the pinned environment and its proof body,
axioms, provenance, and composition must be checked separately.
