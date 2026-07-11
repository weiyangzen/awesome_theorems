# Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| PDE | `partial_t u + partial_x f(u) = 0` in one space dimension | Weak-solution definition and test-function API await statement work |
| Interface | Straight discontinuity `x = s*t` between constant real states `uL`, `uR` | Trace theory for curved or general discontinuities is excluded |
| Root condition | `s*(uR-uL) = f(uR)-f(uL)` iff the interface distribution has zero defect | Both directions must be represented; an algebra-only identity is not the root |
| Flux | Arbitrary scalar `f : Real -> Real` | Minimal regularity required by the chosen weak encoding remains to be determined |
| Degeneracies | Equal states, stationary interfaces, and arbitrary representative on the interface | Mutation probes are deferred to the statement phase |
| Foundations | Lean kernel plus mathlib real analysis, integration, and smooth compact-support infrastructure | Imports, axiom profile, and environment fingerprint are open |

Excluded from this root are systems of conservation laws, multidimensional normal-flux conditions,
moving curved hypersurfaces, balance laws with sources, entropy admissibility, Lax/Oleinik conditions,
existence or uniqueness of shocks, and the compressible Euler mass/momentum/energy specializations.
Those are related theorem families, not harmless alternate notations.

The intended proof architecture is only a scope forecast at intake: split spacetime along the line,
integrate by parts on each constant region, cancel exterior terms by compact support, compute the
interface coefficient, and prove its vanishing is equivalent to the algebraic jump condition. No
obligation registry or closure credit is created here.
