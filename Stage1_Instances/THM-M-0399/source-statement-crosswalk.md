# Source-statement crosswalk

## Primary source anchor

K. F. Roth, "Rational approximations to algebraic numbers", *Mathematika* **2** (1955),
1-20, DOI `10.1112/S0025579300000644`. The paper is the primary anchor for the classical
exponent-`2 + epsilon` finiteness result. Exact printed theorem labeling, page-level wording,
assumption genealogy, and errata have not yet been independently audited, so this intake records
`H1`, not `H0`.

| Canonical component | Source-side role | Intake disposition |
|---|---|---|
| algebraic `alpha` | algebraic target number | included |
| irrational `alpha` | excludes the rational-target degeneracy | included |
| every `epsilon > 0` | exponent is strictly greater than two | included |
| rational approximant with positive reduced denominator | rational approximation and height normalization | included; exact encoding and transport open |
| strict error bound | approximation better than denominator exponent `2 + epsilon` | included; Lean real-power encoding open |
| finitely many approximants | the exceptional rational set is finite | included; exact carrier open |

Repository metadata provides only the name, attribution, year, topic, and an untrusted `已验证`
label. It neither establishes source fidelity nor machine closure. The near-duplicate
`THM-M-0398` is discovery context only and cannot lend statement or proof credit.

To reach `H0`, a later audit must inspect a stable scan, record the exact theorem/page and all
numerator, denominator, and coprimality conventions, investigate corrections or errata, map every
premise to the canonical target, and obtain independent review.
