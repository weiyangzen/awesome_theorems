# Source-statement crosswalk

## Available repository record

`Docs/researches/math_theorems.md` supplies the Chinese name "Fernique theorem", Xavier Fernique,
1975, and the sentence "an upper bound for a stationary Gaussian process". `Docs/Stage0_Blueprint.md`
repeats these fields while leaving definitions, hypotheses, proof path, axioms, and machine status
open. Its `已验证` label is explicitly untrusted under rev-5.6.

No primary publication, edition, theorem number, page, or errata record is attached. The pinned
mathlib bibliography instead cites Xavier Fernique, *Intégrabilité des vecteurs gaussiens*, C. R.
Acad. Sci. Paris 270 (1970), A1698-A1699. This date and exponential-integrability subject do not
match the repository's 1975 stationary-process wording closely enough to identify the exact source
theorem. The citation is therefore a candidate for downstream inspection, not `H0` evidence.

## Crosswalk

| Source element | Mathematical information fixed | Required Lean component | Intake result |
|---|---|---|---|
| "stationary Gaussian process" | Gaussian finite-dimensional laws and shift-invariant law/covariance | process type, law, index action, stationarity predicate | exact conventions unresolved |
| "upper bound" | some quantity is controlled | bounded expression, comparison, constants and quantifiers | unresolved |
| Xavier Fernique | attribution to a theorem family | none by itself | insufficient for identity |
| 1975 | claimed historical date | immutable edition and theorem locator | publication unidentified |
| `已验证` | untrusted inventory status | accepted human proof or kernel receipt | no credit |

## Pinned Lean candidate boundary

The module `Mathlib.Probability.Distributions.Gaussian.Fernique` exposes
`ProbabilityTheory.IsGaussian.exists_integrable_exp_sq`. It states that for a Gaussian measure on
a second-countable complete real normed space there is `C > 0` for which
`x |-> exp (C * ||x||^2)` is integrable. `IntakeProbe.lean` elaborates that exact declaration using
the pinned import. This establishes a concrete `M3` candidate interface, not closure of the
repository target: the source speaks about a stationary Gaussian process and an unspecified upper
bound, while the candidate speaks about exponential norm integrability of a Gaussian measure.

The statement phase must first select a primary theorem and conduct a row-by-row hypothesis and
conclusion comparison. Any claimed equivalence or implication then requires a kernel-checked
transport. Before `H0`, an independent reviewer must verify the edition, theorem/page, definitions,
assumptions, proof boundary, and errata.
