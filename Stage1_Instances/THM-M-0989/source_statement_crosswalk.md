# Source-statement crosswalk

| Claim component | Human source anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Independent triangular array, centered variables, variance normalization, Lindeberg condition, Gaussian limit | Patrick Billingsley, *Probability and Measure*, 3rd ed. (Wiley, 1995), Section 27, Theorem 27.2, pp. 359-360 | finite row index, row-wise `iIndepFun`, expectation and variance sums, convergence in distribution | Pinpoint modern statement located; edition scan/hash and premise-by-premise verification remain open |
| Lindeberg condition via truncated second moments | Billingsley, 3rd ed., equation (27.8), p. 359 | real integral of `X^2` times the strict-threshold indicator, summed over `Fin (n+1)` and tending to zero | Lean notation is frozen and elaborated; premise-level source verification remains open |
| Classical Lindeberg theorem and converse/Feller refinement | W. Feller, *An Introduction to Probability Theory and Its Applications*, Vol. II, 2nd ed. (Wiley, 1971), Chapter XVI, Section 5, "The Lindeberg Conditions" | forward theorem plus a separately gated converse under uniform negligibility | Candidate genealogy/reference; exact theorem numbering, assumptions, and errata require primary audit |
| Standard Gaussian weak limit | Billingsley, Theorem 27.2 conclusion | `TendstoInDistribution` to `id` under `gaussianReal 0 1` | Lean interface selected and elaborated; source fidelity remains subject to the later primary-source audit |
| Source metadata phrase `独立不同分布的中心极限定理` | `Docs/Stage1_Blueprint.md`, `THM-M-0989` | no formal declaration yet | Compatible with the forward result, but too broad to resolve triangular-array normalization or converse scope |

The frozen root chooses the forward normalized triangular-array theorem because it is a precise
standard formulation matching the repository description. `Statement.lean` fixes row `n` as
`Fin (n + 1)`, unit row variance, strict positive-threshold truncation, and the standard Gaussian
limit; `statement_receipt.json` records its elaboration evidence. The later source phase must still
check the cited pages and premise-by-premise fidelity. The anchor-audit phase must search
the pinned mathlib revision and external Lean 4 projects rather than infer machine support from the
repository's untrusted `已验证` label.

No `H0` or machine-closure claim is made. Historical attribution to Lindeberg and Feller, the exact
scope of the converse, source errata, and immutable source fingerprints remain open.
