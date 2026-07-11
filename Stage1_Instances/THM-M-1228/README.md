# THM-M-1228 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Caffarelli-Kohn-Nirenberg
partial regularity theorem. Historical Stage1 code is discovery material only and
contributes no accepted proof or statement credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Partial regularity of suitable weak solutions of the three-dimensional incompressible Navier-Stokes equations | Exact source hypotheses and canonical Lean expression remain for the statement phase |
| Solution model | Velocity and pressure on space-time, weak Navier-Stokes equation, incompressibility, local energy inequality, and the integrability conditions in the primary theorem | The legacy `SuitableWeakSolutionData` is only a candidate model |
| Geometry | Backward parabolic cylinders, parabolic scaling, regular and singular points | A genuine parabolic metric and measure model is not yet frozen |
| Quantitative branch | Scale-invariant quantities, compactness/decay, and epsilon regularity | Architecture only; no lemma is credited |
| Root conclusion | Regularity off the singular set and vanishing one-dimensional parabolic Hausdorff measure of that set | Euclidean Hausdorff measure is not an acceptable substitute |
| Foundations | Lean 4 kernel plus pinned mathlib, with explicit classical/choice and computation profiles | Toolchain, imports, TCB, and environment fingerprint remain open |

The root cannot be replaced by a Gagliardo-Nirenberg inequality, a smooth-solution
regularity fact, a finite-dimensional estimate, or an abstract package whose
essential PDE and measure conclusions are assumed as fields. The provisional
formal surface and its exclusions are structured in `intake.json`; source mapping
is recorded in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The source
identity is located, but its exact theorem/assumption/errata mapping has not been
independently accepted. The first failed theorem gate is the exact-statement gate:
there is no elaborated canonical Lean target, expression hash, environment
fingerprint, checked transport, or mutation record. The theorem is not complete.

## Validation

The commands and exact intake-only results are in `validation.md`. They validate
manifest membership, repository consistency, JSON syntax, and dossier hygiene;
they do not constitute Lean kernel evidence.
