# Source-statement crosswalk

## Candidate primary sources

- Jean Leray, "Sur le mouvement d'un liquide visqueux emplissant l'espace", *Acta Mathematica*
  63 (1934), 193-248. This is the primary whole-space weak-solution source candidate.
- Eberhard Hopf, "Uber die Anfangswertaufgabe fur die hydrodynamischen Grundgleichungen",
  *Mathematische Nachrichten* 4 (1951), 213-231. This is the primary bounded-domain/source-family
  candidate associated with the Leray-Hopf formulation.

Bibliographic identification is discovery evidence only. Exact theorem/page, original hypotheses,
edition or scan, translation decisions, and errata have not been inspected and therefore do not
establish `H0`.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "Leray-Hopf weak solution" | global finite-energy weak solution | a predicate containing weak equation, incompressibility, trace, and energy inequality | included; exact definition open |
| "Navier-Stokes equation" | viscous incompressible evolution | domain, derivatives/distributions, viscosity, nonlinear term, pressure or solenoidal projection | included; encoding open |
| initial data | divergence-free finite kinetic energy datum | concrete solenoidal `L2`-type space | included; domain convention open |
| global existence | solution on all nonnegative times | time-indexed function in source-prescribed Bochner spaces | included; exact spaces open |
| energy inequality | a priori kinetic-energy/dissipation bound | measurable norms, time integration, and quantified inequality | included; force/time convention open |

## Fidelity boundary

The Stage0 text says only "weak solution of the Navier-Stokes equation" and labels it verified. That
label supplies neither a theorem statement nor machine evidence. The statement phase must select
one primary formulation and map every assumption row by row; it may add a separately checked
transport to another standard formulation, but may not silently combine Leray's and Hopf's domain
conventions. Independent source review is required before `H0`.

No repo-local Lean declaration has been credited at intake. Candidate mathlib or external formal
artifacts belong to the later anchor-audit phase.
