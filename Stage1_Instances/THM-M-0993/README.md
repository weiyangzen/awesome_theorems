# THM-M-0993 rev-5.6 intake

This is the rev-5.6 `planned` instance for the Chernoff bound. It inherits no proof credit from the
source label `已验证` or from any library theorem located later.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | Exponential-moment upper-tail bound for a finite sum of independent real random variables | Exact Lean expression and imports belong to the statement phase |
| Variables | A finite family `X i : Omega -> Real` on one probability space | Measurability, independence, and exponential integrability must be explicit |
| Parameters | Real threshold `a` and tilt `t > 0` | Bound before factorization is `P(sum X i >= a) <= exp (-t*a) * E[exp (t*sum X i)]` |
| Independence | Factor the exponential moment into individual moments | Candidate architecture only; no machine credit |
| Corollaries | Bernoulli/binomial multiplicative and additive bounds | Outside the root; never substitutes |
| Foundations | Lean 4 kernel and pinned mathlib measure/integration APIs | Toolchain, imports, axioms, and TCB remain open |

The exact human scope and exclusions are in `intake.json`; source fidelity is mapped in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the statement gate: no elaborated expression, hash, environment fingerprint, or mutation evidence
exists. This intake is self-tested, but the theorem is not complete.

Open DAG: `INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Only `INTAKE` is addressed here.

