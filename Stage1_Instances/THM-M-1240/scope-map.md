# Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Repository identity | `THM-M-1240`, Friedrichs inequality, PDE category, compactly supported Sobolev-function estimate | The name alone does not select one of several Friedrichs/Poincare-type formulations |
| Provisional mathematical family | Control of an `L^p` norm of a zero-boundary or compactly supported Sobolev function by its weak gradient, with a domain-dependent constant | `p`, dimension, boundedness/regularity of the domain, real/complex codomain, and norm normalization are unresolved |
| Functions | A Sobolev function with compact support in the domain, or equivalently a member of a suitably defined zero-trace Sobolev space when a checked density/trace theorem applies | Compact support and zero trace are not interchangeable without hypotheses and a proved transport |
| Quantitative data | Existence of a finite positive constant depending on declared domain/exponent data | Optimal constant, diameter-based constant, and coordinatewise derivative variants are not selected |
| Boundary cases | Constant functions, empty/unbounded/disconnected domains, `p = 1`, `p = infinity`, and support touching the boundary | Each must be decided by the exact source statement; none is excluded by fiat |
| Lean surface | Planned Lean 4 expression using measure, `L^p` norm, weak derivative/Sobolev membership, support or zero-trace data | No exact local or mathlib declaration has been selected or credited |
| Foundations | Lean 4 kernel under the rev-5.6 foundation, TCB, and computation profiles | Exact imports, toolchain fingerprint, axioms, and dependency closure belong to later phases |

## Scope decision

The canonical claim cannot truthfully be made more precise from the repository metadata alone.
The statement phase must first select and pin a primary formulation, then preserve all of its
domain, exponent, support/trace, and constant-dependence conditions. A bounded-domain
`W_0^{1,p}` theorem, a compact-support Euclidean theorem, and an `L^2` Hilbert-space coercivity
estimate are candidate encodings, not interchangeable names for an already frozen target.

No mandatory proof layer is excluded. At minimum, later architecture must expose definitions and
domains, support-to-zero-trace transport if used, the one-dimensional/line estimate or other core
analytic estimate, integration and norm steps, domain-constant control, boundary cases, imported
formal boundaries, and exact recomposition to the selected root.
