# THM-M-1266 rev-5.6 intake

This is the `planned` dossier for Tonelli's variational existence theorem. The short source label
"existence for variational problems" names a family of results, not one assumption-complete
statement. Consequently this intake preserves the classical direct-method claim while leaving the
precise interval, admissible function space, growth exponents, and regularity convention for the
statement phase and primary-source audit. It does not inherit proof credit from `S1_M_162.lean`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | attainment of the action infimum by an admissible curve under Tonelli hypotheses | precise classical variant and source pinpoint remain open |
| Curves and boundary | a nonempty class of curves with fixed boundary data | Sobolev/absolutely-continuous space, interval, trace, and endpoint encoding unresolved |
| Integrand | time/state/velocity Lagrangian, convex in velocity, with regularity and coercive growth | exact measurability, continuity, exponent, and extended-real conventions unresolved |
| Direct method | minimizing sequence, coercive bound, compactness, closed boundary data, lower semicontinuity | each bridge remains a future typed obligation; no closure credited |
| Lean candidate | legacy `AwesomeTheorems.Stage1.S1_M_162.StatementShape` | discovery input only; several `Prop` fields do not encode usable mathematical implications |
| Checked subcase | lower-semicontinuous real function on a nonempty compact admissible set attains a minimum | useful anchor, but it is not the full Tonelli compactness/coercivity theorem |
| Foundations | Lean kernel, mathlib measure/integration, topology, convexity, derivative or weak derivative | exact pins, foundation dependencies, TCB, and computation profile remain open |

The preliminary proof architecture is: define the admissible space and action; select a minimizing
sequence; derive coercive bounds; extract a convergent or weakly convergent subsequence; preserve
boundary membership; prove lower semicontinuity from convexity and regularity; conclude attainment.
This is scope mapping only, not the frozen obligation registry required by the later phase.

## Intake verdict

Lifecycle is `planned` and the provisional root vector is `[H2, M3, R3]`. The first failed theorem
gate is exact-statement fidelity: the source metadata is too broad to select a unique Tonelli
variant, and the candidate Lean expression has neither a rev-5.6 environment fingerprint nor
checked transports. The theorem is not complete.

## Validation

The exact commands and results are recorded in `validation.md`. They validate target membership,
repository-standard consistency, JSON syntax, dossier references, and absence of forbidden proof
constructs. No Lean declaration was added in this intake phase.
