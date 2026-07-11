# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository source claim | `Docs/researches/math_theorems.md`, entry "伯恩斯坦不等式": Sergei Bernstein, 1924, "随机变量和的尾概率" | none | Metadata establishes identity and topic, but not hypotheses, constants, or tail convention |
| Bounded independent centered summands | Classical bounded-summand Bernstein formulation; a primary edition and pinpoint remain to be audited | fields of legacy `BernsteinBoundedProblem` | Selected scope is consistent with the legacy candidate, but human-source fidelity is not accepted |
| Variance-sensitive upper tail | `P(S_n >= t) <= exp(-t^2/(2(v+bt/3)))` | legacy `BernsteinTailConclusion` and `bernsteinUpperBound` | Exact constant and convention need a primary-source/modern-reference genealogy and Lean elaboration |
| Finite sum and variance budget | `S_n = sum_(i<n) X_i`, `sum Var(X_i) <= v` | legacy `partialSum` and `variance_sum_le` | Candidate encoding only; no rev-5.6 statement credit |
| Independence, centering, boundedness | Mutual independence, zero means, and `|X_i| <= b` almost surely | legacy structure fields | Binder scope and almost-everywhere semantics must be mutation-tested |
| Other Bernstein families | Lower/two-sided, moment-condition, martingale, vector, and matrix forms | none in the canonical target | Explicitly excluded to prevent theorem substitution or silent broadening |

The repository's source record is too short to identify a unique mathematical proposition. The
chosen root is therefore a conservative scope decision grounded in the existing bounded-summand
artifact, not evidence that Bernstein's 1924 text states this modern normalized form verbatim.
The source audit must locate and hash an accessible primary edition, record exact theorem/page and
notation, trace the modern constants and assumptions, inspect corrections or translation issues,
and obtain independent review. Until then the human status is `H2`, not `H0`.

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_275.lean` explicitly describes its
`StatementShape` as a candidate and says that no terminal Bernstein proof is claimed. Its names are
discovery anchors only. The dependent statement phase must inspect the actual declaration type,
pin minimal imports and toolchain, serialize the normalized expression, check any transports, and
mutation-test domains, ordered binders, all hypotheses, constants, inequality directions, and the
listed boundary cases before proof evidence is considered.
