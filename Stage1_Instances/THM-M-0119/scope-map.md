# THM-M-0119 Scope Map

## Canonical Claim

For a normal projective variety `X` over a characteristic-zero field, an effective rational
divisor `Delta` making `(X, Delta)` klt, and a Cartier divisor `D`, the condition

`D - (K_X + Delta)` is nef and big

implies `H^i(X, O_X(D)) = 0` for every `i > 0`. The requirement that `K_X + Delta` is Q-Cartier is
explicit rather than hidden inside notation.

## Binder And Boundary Map

| Surface | Included | Not silently substituted |
|---|---|---|
| Base | arbitrary characteristic-zero field | only complex numbers, or positive characteristic |
| Space | normal projective variety | smooth-only, proper nonprojective, analytic, or relative family |
| Singularities | klt pair with effective Q-boundary | log-canonical pair or unspecified "log canonical singularities" |
| Positivity | `D - (K_X + Delta)` nef and big | ample-only, nef-only, or big-only hypothesis |
| Coefficient/output | Cartier `D`; coherent cohomology of `O_X(D)` | Q-Cartier output without a defined sheaf, or numerical vanishing |
| Degrees | every integer `i > 0` | `H^0`, Euler characteristic, or one fixed degree |

The zero-dimensional case is not excluded and is harmless, but does not replace the general root.
The commonly named smooth simple-normal-crossings formulation may later be registered only through
a checked equivalence or implication; it is not interchangeable at intake.

## Formal Surface Needed Next

The statement phase must locate or define compatible Lean representations of projective normal
varieties, Weil/Cartier/Q-divisors, canonical divisor, effective boundaries, klt singularities,
nefness, bigness, divisorial sheaves, and sheaf cohomology. It must also decide how the
characteristic-zero base and positive-degree binder are represented and mutation-test every
hypothesis. Until one expression elaborates as a whole, the formal target remains null and machine
debt remains `M5`.

No source completeness, Lean theorem, proof body, or machine closure is claimed by this intake.
