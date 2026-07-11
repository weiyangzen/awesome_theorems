# Source-statement crosswalk

Primary discovery source: M. Gubinelli, P. Imkeller, N. Perkowski,
*Paracontrolled distributions and singular PDEs*, arXiv:1210.2684v4
(2017-08-15). The inspected PDF has SHA-256
`d09790ea4e866e0e5c1a7fe2b419ea70308d5c638f63ca306641dbe62ed19fa3`.

| Claim component | Primary source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Theory-level repository wording | Abstract and Introduction, pp. 1-2 | none exact | Describes several problems, not one theorem; cannot be the kernel target |
| Generalized PAM existence and uniqueness | Corollary 5.9, pp. 38-39, relying on Theorem 5.4 | future `GIP-ROOT`/`GIP-FIX` | Leading target candidate; exact assumptions and uniqueness class still require premise tracing |
| Parameter regime | Corollary 5.9: `alpha in (2/3,1)`, `beta in (2-2 alpha, alpha]`, smoothness of `F`, `u0 in C^alpha` | future explicit binders | Must preserve endpoints, dimension, torus, and regularity conventions |
| Renormalized equation | Corollary 5.9 and Lemma 5.8: mollified noise and counterterm `c_epsilon F'(u_epsilon)F(u_epsilon)` | future `GIP-REN` | Counterterm and mollifier normalization are root-relevant, not implementation detail |
| Approximation convergence | Corollary 5.9: measurable `tau`, `P(tau>0)=1`, convergence in probability in stopped `C^alpha` | future `GIP-CONV` | Probability mode and random-time scope must be encoded exactly |
| Existing local statement shape | No source theorem has this bundled proposition-package form | `AwesomeTheorems.Stage1.S1_M_182.StatementShape` | Discovery scaffold only; it assumes the difficult SPDE propositions and receives no proof credit |

The paper also treats rough differential equations and a fractional
Burgers-type SPDE. Those are excluded from the candidate root unless a later
source-selection receipt explicitly chooses one; a theory name cannot license
their conjunction or interchange.

No `H0` or exact Lean statement claim is made. Remaining source work includes
the published-version/errata check, a line-by-line dependency crosswalk from
Theorem 5.4 and Lemma 5.8, notation normalization, and independent review.

Discovery URL: <https://arxiv.org/abs/1210.2684>
