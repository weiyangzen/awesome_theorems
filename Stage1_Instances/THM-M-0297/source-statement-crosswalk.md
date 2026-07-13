# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2132-2137` supplies exactly the title `Marcinkiewicz interpolation
theorem`, Jozef Marcinkiewicz, 1939, the gloss `interpolation of weak-type operators`, importance
`high`, and status `verified`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:8197-8222` repeats that metadata but leaves exact definitions and
premises, proof route, dependencies, equivalent formulations, axiom policy, machine-checked status,
and artifact links open. The rev-5.6 manifest preserves `verified` only as untrusted metadata and
resets the target to `L0 / rework_required`.

The catalog contains no bibliography, formula, ordered binders, measure-space assumptions,
operator class, exponent conditions, endpoint constants, conclusion, incorporated definitions,
proof boundary, errata, or reviewer. Its gloss therefore identifies a theorem family but does not
freeze one proposition.

## Historical source lead

A pinpoint bibliographic lead is J. Marcinkiewicz, *Sur l'interpolation d'operations*, *Comptes
rendus hebdomadaires des seances de l'Academie des sciences* 208 (1939), pages 1272-1273. The
reference is corroborated in the machine-readable reference list for Antoni Zygmund, *On a theorem
of Marcinkiewicz concerning interpolation of operations*, later reprinted in *Selected Papers of
Antoni Zygmund* (Springer, 1989), pages 214-239, DOI
`10.1007/978-94-009-1045-4_12`.

This is a credible primary-source locator and explains the catalog's attribution and date. It is
not yet `H0`: no lawful complete copy is admitted to the repository, no exact French passage is
transcribed, no incorporated definitions or proof boundary are mapped, no correction or errata
search is accepted, and no independent reviewer has approved fidelity. Zygmund's later paper is a
source lead and elaboration, not permission to replace the original result with any modern variant.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| weak type | distribution-function inequality or weak/Lorentz quasi-norm bound | measures of superlevel sets, thresholds, powers, constants | formula and conventions absent |
| operator | linear, sublinear, quasilinear, or restricted-domain operation | typed map plus algebraic/measurability laws | class and domain absent |
| endpoints | two exponent pairs, possibly including infinity | `ENNReal`/real exponents and endpoint-order predicates | pairs and restrictions absent |
| interpolation | convex reciprocal-exponent relations through `theta` | exact equations for intermediate `p` and `q` | parameter and formulas absent |
| strong conclusion | `Lp -> Lq` membership, norm inequality, or bounded extension | `MemLp`, `eLpNorm`, `Lp`, extension and representative proofs | strength and constant absent |
| measure spaces | finite, sigma-finite, separable, or unrestricted | measurable spaces, measures, typeclasses | all choices absent |
| 1939 | publication and provenance datum | source record only | plausible source located, not admitted |
| `verified` | untrusted inventory label | no declaration or proof body | explicitly rejected as evidence |

## Variant boundary

A standard modern scalar theorem often assumes a sublinear operator of weak types at two distinct
endpoints and concludes strong type at an intermediate point. Sources vary on whether domain and
target exponent pairs coincide, whether one endpoint is infinity, whether the operator is merely
quasilinear, whether spaces must be sigma-finite, how weak type is normalized, and whether the
result is first proved on simple functions and then extended. Restricted weak-type, Lorentz-space,
multilinear, vector-valued, and quasi-Banach versions have different premises and conclusions and
cannot be silently substituted.

The neighboring Riesz-Thorin theorem uses strong endpoint estimates and linearity rather than the
weak endpoint contract named here. Chebyshev-Markov inequalities in pinned mathlib convert strong
`Lp` information into superlevel estimates but do not supply the desired weak-to-strong operator
interpolation theorem.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`MeasureTheory.MemLp`, `MeasureTheory.eLpNorm`, `MeasureTheory.eLpNorm_eq_lintegral_rpow_enorm_toReal`,
`MeasureTheory.mul_meas_ge_le_pow_eLpNorm'`, and `MeasureTheory.meas_ge_le_mul_pow_eLpNorm_enorm`.
These declarations authenticate nearby `Lp` and distribution-estimate infrastructure. A bounded
case-insensitive search found no terminal Marcinkiewicz or weak-type interpolation declaration in
repo-local Lean or pinned mathlib. This is discovery only; exhaustive formal-candidate and
proof-body audit remains the dependent anchor-audit phase.

## Required source admission

The statement phase must preserve and hash a lawful complete source edition, select one exact
result and proof boundary, transcribe every incorporated definition, ordered binder, hypothesis,
exponent relation, conclusion, constant, and boundary case, reconcile the historical statement with
any modern encoding, audit translations and corrections, and obtain independent review. It must
then freeze and mutation-test the same exact Lean expression. Until then the canonical mathematical
and Lean targets remain null and the source classification remains `H1`.
