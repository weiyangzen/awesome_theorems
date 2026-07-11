# Source-statement crosswalk

Primary source: Markus Keel and Terence Tao, *Endpoint Strichartz Estimates*, American Journal of
Mathematics 120(5), 1998, pp. 955-980, DOI
<https://doi.org/10.1353/ajm.1998.0039>. The intended root is Theorem 1.2. The bibliographic identity
is firm enough for intake, but an immutable source-file hash and errata search are still required.

| Claim component | Primary-source anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Energy bound for `U(t)` | Equations (1) and surrounding definitions | bounded linear operators from a Hilbert space into the `B0*`/`L2` endpoint | Exact codomain notation must be checked against the paper |
| Dispersive decay for `U(t)U(s)^*` | Equation (2) | operator norm bound with kernel `|t-s|^(-sigma)` | Singular diagonal and almost-everywhere semantics are open |
| Sharp admissibility | Definition 1.1 | predicate on `(q,r,sigma)` | Exact inequalities, infinity conventions, and excluded triple must be transcribed |
| Homogeneous estimate | Theorem 1.2, estimate (7) | mixed-norm bound for `U(t)f` | No Lean declaration selected |
| Dual estimate | Theorem 1.2, estimate (8) | bound on the time integral of `U(s)^*F(s)` | Bochner integral and duality interfaces are open |
| Retarded inhomogeneous estimate | Theorem 1.2, estimate (9) | bound on `integral s in (-infinity,t), U(t)U(s)^*F(s)` | Measurability and truncated-domain encoding are open |

The source theorem is abstract and simultaneously packages three estimates. Replacing it with only
the familiar wave or Schrodinger endpoint corollary would narrow the theorem; dropping the source's
endpoint exception would broaden it. Neither substitution is allowed.

No existing Lean theorem is asserted here. The later statement phase must inspect the primary PDF,
freeze every ordered binder and constant convention, choose an exact Lean expression, elaborate it
under minimal pinned imports, and mutation-test the energy hypothesis, dispersive hypothesis,
admissibility boundaries, retarded integration region, and exceptional endpoint. Until then the
human classification is `H1` and the machine classification is `M4`.
