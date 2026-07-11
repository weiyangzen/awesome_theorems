# Source-statement crosswalk

The repository source record says only "chain rule for stochastic processes" and attributes the
result to Kiyosi Ito in 1951. That wording is not an exact theorem: hypotheses and the selected
version are missing. This intake therefore freezes a provisional classical multidimensional
continuous-semimartingale scope while leaving exact-statement selection fail-closed.

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Historical stochastic differential formula | K. Ito, "On stochastic differential equations," *Memoirs of the American Mathematical Society* 4 (1951), pp. 1-51 | no accepted target yet | Primary historical monograph identified bibliographically; theorem/page, edition scan, assumptions, and errata have not been audited: no `H0` |
| Repo source phrase | `Docs/researches/math_theorems.md`: "随机过程的链式法则" | legacy `ItoFormulaConclusion` / `ItoFormulaIdentity` candidates | Metadata is discovery provenance, not a mathematically sufficient statement or formal-proof source |
| Semimartingale and regularity hypotheses | Required by the provisional modern formulation | legacy `ItoFormulaData`, `ItoFormulaHypotheses` candidates | Exact continuity, filtration, measurability, integrability, and `C^2` encodings remain statement obligations |
| First-order term | coordinate stochastic integrals of derivatives of `f` against `X` | legacy stochastic-integral boundary | Candidate interface only; terminal stochastic-integral construction and semantics are not credited |
| Second-order correction | half the Hessian integrated against coordinate quadratic covariations | legacy quadratic-covariation boundary | Candidate interface only; convention for diagonal/cross terms must be frozen |
| Brownian formula | set bracket matrix to elapsed time times the identity | legacy one-dimensional Brownian candidates | Specialization, not an acceptable replacement for the provisional root |

The bibliographic anchor is deliberately not presented as an accepted edition/page crosswalk. The
anchor-audit phase must obtain an immutable copy, hash it, locate the exact formula and assumptions,
check corrections or errata, and map each premise to a frozen node. The statement phase must first
decide whether the historical target or a standard modern semimartingale theorem is authoritative;
it must then elaborate that exact proposition, serialize its normalized expression, and
mutation-test domains, binders, hypotheses, initial time, regularity, and boundary cases.

Discovery references (not immutable evidence receipts):

- Ito monograph catalog/DOI: <https://doi.org/10.1090/memo/0004>
- Legacy candidate module: `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_225.lean`

Current source status is `H2`: a primary work and a plausible modern scope are identified, but no
accepted pinpoint premise crosswalk or independent review exists.
