# THM-M-0396 source-statement crosswalk

| ID | Source record | Contribution | Intake status |
|---|---|---|---|
| SRC-REPO-1 | `Docs/researches/math_theorems.md`, entry `贝克定理` | Gives Alan Baker, 1966, and only `对数线性形式的下界`; its `已验证` label is untrusted by the manifest. | Located; insufficient for H0 |
| SRC-STAGE0-1 | `Docs/Stage0_Blueprint.md`, THM-M-0396 | Repeats the broad claim and explicitly leaves definitions, assumptions, dependencies, axioms, and machine evidence pending. | Located; confirms underspecification |
| SRC-LEGACY-1 | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_009.lean` | Supplies a conservative object model and candidate variants, while explicitly recording that no terminal Baker lower-bound proof is imported. | Legacy discovery only; zero accepted proof credit |
| SRC-PRI-1 | Alan Baker, "Linear forms in the logarithms of algebraic numbers. I", *Mathematika* 13 (1966), 204-216, DOI `10.1112/S0025579300003971` | Historical primary anchor for the 1966 series. Exact theorem number, hypotheses, normalization, and match to the repository's word "lower bound" require primary-text audit. | Candidate; not yet H0 |

## Claim decomposition

| Repository phrase | Required exact-statement field | Current resolution |
|---|---|---|
| "linear forms" | Number of terms, coefficient domain, and formula | Open |
| "logarithms" | Algebraic inputs, embeddings, and complex-log branch witnesses | Open |
| "lower bound" | Nonvanishing premise, norm/absolute value, parameters, height convention, constant, and effectiveness | Open |
| "Baker's theorem" | Exact historical or later explicit variant and bibliographic theorem/page | Open |

`SRC-GAP-1` is resolved for the formal statement boundary by selecting the
standard real, multiplicative Matveev variant recorded in `Statement.lean`:
`Lambda = alpha_1^b_1 * ... * alpha_n^b_n - 1`, with `n >= 1`, a number field
`K`, a chosen real embedding, positive algebraic inputs, integer coefficients,
the normalized number-field logarithmic height, explicit `A_i` and `B`
majorants, and `Lambda != 0`. The conclusion uses the explicit constant shape
`1.4 * 30^(n+3) * n^(9/2) * D^2 * (1 + log D) * (1 + log(nB)) * prod A_i`.

This resolves exact Lean target selection, not H0. Pinpoint primary-source
theorem/page wording, errata, and an independent assumption crosswalk remain
for `S56-M-0396-ANCHOR_AUDIT`; source fidelity therefore remains open and no
proof credit is granted.
