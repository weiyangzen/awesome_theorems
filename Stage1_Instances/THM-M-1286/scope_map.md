# Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Schwarz rearrangement does not increase the `L^p` weak-gradient seminorm, `1 <= p < infinity` | Human claim frozen; formal types open |
| Function space | Nonnegative `u in W^{1,p}(R^n)` vanishing at infinity | Exact representative and weak-derivative conventions open |
| Rearrangement | Radial, radially nonincreasing `u*`, equimeasurable with `u` | Lean construction and uniqueness convention open |
| Energy | `integral |grad u*|^p <= integral |grad u|^p` | Bochner/ENNReal/Real integral encoding open |
| Domain form | Whole space is canonical; bounded-domain `W_0^{1,p}` is an alternate via zero extension | Transport is not credited until checked |
| Proof architecture | level sets, symmetric balls, equimeasurability, coarea/isoperimetry, approximation and lower semicontinuity | Architecture is provisional, not an obligation registry |
| Foundations | Lean kernel plus versioned measure/Sobolev dependencies | Foundation and TCB fingerprints open |

Out of scope are equality/rigidity cases, Steiner or polarization variants, anisotropic energies,
`p = infinity`, fractional Sobolev variants, and toy finite-sequence rearrangement inequalities.
Signed inputs require an explicit checked reduction through absolute value and are not silently folded
into the nonnegative root. The `p = 2` Dirichlet integral wording is a specialization, not a valid
replacement for the frozen finite-`p` claim.

Boundary probes reserved for the statement phase include `n = 0`, `p < 1`, `p = infinity`, constant
nonzero functions on all of `R^n`, a signed input without the absolute-value bridge, and deletion of
the finite-superlevel-set condition.
