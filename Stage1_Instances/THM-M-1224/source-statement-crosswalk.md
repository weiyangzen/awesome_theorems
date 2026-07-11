# Source-statement crosswalk

## Candidate primary sources

- Manoussos Grillakis, "Regularity and asymptotic behaviour of the wave equation with a critical
  nonlinearity", *Annals of Mathematics* 132(3) (1990), 485-509.
- Manoussos Grillakis, "Regularity for the wave equation with a critical nonlinearity",
  *Communications on Pure and Applied Mathematics* 45(6) (1992), 749-774.

These bibliographic records and the repository's short phrase `NLW的正则性` identify the intended
source family, but are not `H0`. Exact theorem numbers/pages, wording, definitions, hypotheses,
edition copies, and errata have not yet been independently inspected.

## Crosswalk

| Repository/source phrase | Frozen intended component | Required Lean component | Intake status |
|---|---|---|---|
| "Grillakis theorem" / `NLW的正则性` | critical NLW regularity theorem | concrete PDE proposition, not a metadata package | variant frozen; exact source anchor open |
| critical nonlinearity | defocusing quintic `u^5` in `R^3` | real-valued spacetime function and power nonlinearity | included; encoding open |
| wave equation | `u_tt - Delta u + u^5 = 0` | time derivatives, spatial Laplacian, pointwise/distributional equality | included; sign convention to verify |
| smooth initial data | source-accurate smooth finite-energy/localized Cauchy data | initial traces and function-space predicates | included; exact class open |
| regularity | global classical solution with persistence of smoothness | existence, uniqueness if source states it, global domain, derivative regularity | included; exact conclusion open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_155.lean` records the same 3D defocusing quintic
variant and useful audit vocabulary. It also explicitly says the terminal theorem is not repo-local
closed. Its structures, strings, `rfl` metadata checks, and any abstract statement shape receive no
rev-5.6 statement or proof credit. The pinned mathlib and external search must be repeated during
anchor audit.

Before `H0`, an independent reviewer must inspect the selected article theorem and surrounding
definitions, reconcile the two papers, check errata, and approve every source-to-Lean assumption
and conclusion row.
