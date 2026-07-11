# Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Domain | Arbitrary bounded open `Omega subset R^2` | Nonempty is unnecessary; measurability and finite measure follow but must be represented explicitly in Lean if APIs require them |
| Functions | Real-valued `u in W_0^{1,2}(Omega)` | Zero trace is essential; smooth compactly supported functions may be used only through a checked density/equivalence bridge |
| Normalization | `integral_Omega |grad u|^2 <= 1` | Replacing it by an `L^2` norm bound is allowed only by checked transport |
| Endpoint | A domain-dependent finite constant bounds `integral_Omega exp(4*pi*u^2)` uniformly in `u` | No numerical best constant is claimed |
| Sharpness | Every `alpha > 4*pi` has infinite supremum over the same admissible class | This is part of the root, not optional commentary |
| Foundations | Lean 4, pinned mathlib, ordinary classical measure/Sobolev infrastructure | Exact imports, axioms, TCB, and environment fingerprint remain statement-phase work |

Excluded substitutes are the non-sharp `alpha < 4*pi` theorem alone, a single
fixed function, the whole-plane inequality with an additional `L^2` bound,
compact-surface/Onofri variants, higher-dimensional variants, radial-only
classes, and any hypothesis that directly assumes exponential integrability.

Degenerate probes to preserve are the empty domain, the zero function, null
sets, equality in the gradient constraint, and exponents equal to, below, and
above `4*pi`. The statement phase must decide the exact supremum encoding and
show that extended-integral finiteness matches existence of a uniform real
constant.

