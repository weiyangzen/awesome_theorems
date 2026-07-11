# THM-M-1051 rev-5.6 intake

This is the `planned` dossier for the Krylov-Safonov Harnack estimate. The short
repository description does not determine whether the intended root is the elliptic or
parabolic theorem, so this intake records that ambiguity rather than silently choosing a
stronger or weaker result. Historical `已验证` metadata supplies no proof credit.

## Scope map

| Surface | Intended scope | Boundary at intake |
|---|---|---|
| Root family | Interior Harnack inequality for nonnegative solutions of uniformly elliptic/parabolic nondivergence-form equations with merely measurable coefficients | The exact elliptic/parabolic variant must be selected from a pinned primary source |
| Equation | A linear second-order nondivergence operator, schematically `aᵢⱼ Dᵢⱼu` (and `- ∂ₜu` in the parabolic case) | Sign convention, lower-order terms, and solution notion remain open |
| Coefficients | Bounded measurable coefficient matrix satisfying quantitative uniform ellipticity | Symmetry convention and ellipticity constants must be frozen |
| Solution | Nonnegative solution in an interior ball or parabolic cylinder | Classical, strong/Sobolev, or viscosity solution is not yet selected |
| Conclusion | A scale-invariant comparison of an interior supremum with an interior infimum, with a constant controlled only by structural data | Domains, nested regions, and constant dependencies require exact transcription |
| Exclusions | Divergence-form Moser Harnack, harmonic-only special cases, probabilistic analogues, and assumptions containing the desired estimate | These may be comparison artifacts but cannot replace the root |

## Intake verdict

Lifecycle is `planned`; provisional vector is `[H1, M3, R3]`. The first failed theorem
gate is exact statement identification. No Lean theorem or proof closure is claimed.
The open phase DAG is recorded in `task-dag.json`; validation evidence is in
`validation.md`.
