# Source-statement crosswalk

## Primary source

A. Roth, "Rational approximations to algebraic numbers", *Mathematika* **2** (1955), 1-20, DOI `10.1112/S0025579300000644`. The paper's main theorem is the source anchor for the exponent `2 + epsilon` finiteness claim. Exact theorem numbering, printed-page statement, assumptions, and errata remain subject to page-level inspection and independent review; consequently this intake records `H1`, not `H0`.

## Crosswalk

| Intake component | Source-side meaning | Current disposition |
|---|---|---|
| `alpha` algebraic | algebraic target number | included |
| `alpha` irrational | excludes trivial rational target | included |
| `epsilon > 0` | exponent is strictly larger than two | included |
| rational `p/q`, `q > 0` | rational approximants | included; representation transport open |
| strict approximation inequality | `|alpha - p/q| < q^(-(2+epsilon))` | included; Lean power encoding open |
| finiteness | only finitely many approximants satisfy the inequality | included; exact Lean finiteness carrier open |

## Provenance boundary

Repository metadata supplies only the Chinese name, topic, attribution, year, and an untrusted `已验证` label. Those fields do not establish source fidelity or machine closure. The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_011.lean` may help later discovery but receives no proof, statement, or validation credit in this intake.

## Open H-gate work

Inspect a stable scan/edition page by page; record the exact printed theorem label and wording, all restrictions on numerator/denominator and equivalence of rational representations, cited prerequisites, and any published errata. A second reviewer must then attest the source-to-canonical-statement mapping before `H0` is possible.
