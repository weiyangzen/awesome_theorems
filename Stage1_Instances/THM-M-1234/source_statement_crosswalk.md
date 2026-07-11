# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Global existence for two-dimensional ideal incompressible flow in the bounded-vorticity regime | V. I. Yudovich, "Non-stationary flows of an ideal incompressible fluid", *USSR Computational Mathematics and Mathematical Physics* 3 (1963), pp. 1407-1456, translated from *Zhurnal Vychislitel'noi Matematiki i Matematicheskoi Fiziki* 3 (1963), pp. 1032-1066 | No declaration selected | Primary paper identified, but theorem/page pinpoint, edition reconciliation, assumptions, and errata are not yet audited: `H1` |
| Two-dimensional incompressible Euler system | Same paper; exact displayed problem and notation require inspection | Future velocity/pressure statement structure | Domain, boundary, forcing, regularity, and weak-solution conventions remain open |
| Bounded-vorticity data regime | Same paper; exact hypotheses require a primary-text premise crosswalk | Future `L∞` vorticity predicate and initial-data structure | "Yudovich regime" is a scope label, not an accepted formal hypothesis list |
| Vorticity transport and velocity recovery | Proof architecture expected from the source and modern presentations | Future curl/transport/Biot-Savart or elliptic bridge obligations | Architecture candidate only; no theorem name, equivalence, or proof credit |
| Uniqueness | Common modern statements call the result an existence-and-uniqueness theorem | Excluded from the present root unless source audit and manifest reconciliation authorize it | The generated target says global existence only; intake must not broaden it |

The source title and bibliographic coordinates are sufficient for discovery, not for `H0`. The
statement phase must obtain and hash an immutable edition, locate the exact theorem and displayed
equations, map every premise and conclusion, reconcile translation pagination, and check errata.
It must then choose one exact Lean representation and prove any credited velocity-vorticity
transport rather than treating the formulations as definitionally interchangeable.

Discovery identifier (not an immutable evidence receipt): DOI
<https://doi.org/10.1016/0041-5553(63)90293-6>.

No public Lean 4 closure is asserted or ruled out at intake. Repository-local mathlib and external
candidate searches belong to `S56-M-1234-ANCHOR_AUDIT`; the current machine classification remains
`M4` because an exact elaborable proposition has not been frozen.
