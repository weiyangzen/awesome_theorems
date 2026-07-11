# THM-M-1184 rev-5.6 intake

This is the `planned` rev-5.6 dossier for Kantorovich duality. Historical slot
`S1-M-169` and its Lean module are discovery inputs only and carry no accepted proof credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | Compact metric Borel probability spaces, continuous real cost, equality of coupling infimum and signed continuous-potential supremum | Lean expression and fingerprints belong to the statement phase |
| Primal objects | Probability couplings, fixed marginals, real cost integral, infimum | Nonemptiness, integrability, and order encoding must be checked |
| Dual objects | Real continuous potentials with `phi x + psi y <= c (x,y)`, integral objective, supremum | Quotient-by-constants and boundedness choices remain open |
| Weak duality | Marginal push-forward identities and monotonicity of integration | Architecture only; no proof credit |
| Strong duality | Separation/minimax or c-transform argument giving the reverse inequality | Open formalization frontier |
| Broader source form | Polish spaces and lower-semicontinuous extended costs under integrable bounds | Candidate transport, not part of the frozen root |
| Foundations | Lean 4 kernel and pinned mathlib measure/topology APIs | Exact environment and axiom closure remain open |

The historical `CompactMetricStatementShape` uses `ENNReal` costs, nonnegative `ENNReal`
potentials, and concludes existence of a data package containing the reverse inequality. It is not
silently adopted: those choices are not definitionally the standard signed-potential dual and the
data-package conclusion is not itself the source statement. The dependent statement task must
construct a fresh exact target or prove explicit transports.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Within later proof architecture, the anticipated cut is: coupling/object model; marginal integral
transport; weak duality; compactness and lower semicontinuity of the primal; signed-potential
normalization; separation/minimax or c-transform reverse inequality; equality wrapper. This is only
a scope map, not a frozen obligation registry.

## Intake verdict

Lifecycle is `planned`, root vector is `[H1, M3, R3]`, and theorem completion is false. The first
failed theorem gate is exact statement elaboration: there is no normalized expression hash,
environment fingerprint, checked source transport, or mutation record. Source pinning, errata
review, and independent review are also open.

## Validation

The exact commands and results in `validation.md` validate manifest membership, repository
consistency, dossier JSON syntax, and local reference hygiene only.
