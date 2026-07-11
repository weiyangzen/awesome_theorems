# THM-M-1131 rev-5.6 intake

This is the `planned` dossier for Fourier's law of heat conduction and the advertised derivation
of the heat equation. The repository's one-line description does not identify a precise theorem:
Fourier's law is a constitutive model, while deriving a PDE also requires an energy-balance law
and material assumptions. This intake preserves that boundary rather than formalizing the desired
PDE as an assumption. Historical `已验证` metadata supplies no source or proof credit.

## Scope map

| Surface | Intended scope | Boundary at intake |
|---|---|---|
| Constitutive law | Heat flux is proportional and opposite to the temperature gradient, schematically `q = -K ∇T` | Scalar versus anisotropic conductivity, regularity, coordinates, and units remain to be frozen from a primary source |
| Conservation law | Local internal-energy balance, with optional volumetric heat source | Sign convention, boundary flux, and weak versus classical form remain open |
| Material closure | A relation between internal energy and temperature; in the elementary homogeneous case, constant density, heat capacity, and conductivity | Positivity, spatial dependence, and temperature dependence must be explicit |
| Derived conclusion | Under the selected assumptions, temperature satisfies a heat equation such as `∂ₜT = α ΔT` (or its variable-coefficient/source variant) | Exact domain, initial/boundary data, and equality notion are not yet selected |
| Exclusions | Experimental universality of Fourier's law, ballistic/nonlocal heat transport, and a hypothesis that already asserts the heat equation | Physical validation cannot be replaced by a Lean proof of a conditional mathematical implication |
| Formal system | Lean 4 plus pinned mathlib analysis APIs | No module, declaration, expression hash, or environment fingerprint is credited at intake |

## Intake verdict

Lifecycle is `planned`; provisional vector is `[H1, M3, R3]`. The first failed theorem gate is
exact source-statement identification: the current metadata conflates a constitutive law with a
conditional derivation. The dependent statement phase must choose and elaborate one exact
conditional mathematical implication without broadening or substituting it. No Lean theorem or
theorem-completion claim is made. The open phase DAG is in `task-dag.json`; validation evidence is
in `validation.md`.
