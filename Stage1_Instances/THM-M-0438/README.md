# THM-M-0438 rev-5.6 intake

This is a `planned` dossier for the repository label **志田周期 / Shida periods**. The available
metadata says only “period integrals on Shida varieties” and attributes the item to Goro Shimura.
That wording does not determine a unique theorem, paper, variety, hypotheses, or period relation.
The intake therefore freezes the ambiguity rather than silently replacing it with a theorem about
Shimura varieties.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | The exact theorem intended by the labels `志田周期`, “Shida periods”, and “period integrals on Shida varieties” | Primary source, theorem number, and even the English-name correspondence are unresolved |
| Objects | The intended variety, base field/reflex field, cycle, differential or automorphic/cohomological input, and period comparison | None is specified by the source metadata |
| Analytic layer | A genuinely sourced period integral, including domain, measure/orientation, coefficients, and convergence | The legacy Bochner-integral package is substrate only |
| Geometric layer | A genuinely sourced model and the exact properness/smoothness/moduli assumptions | The legacy `Scheme` fields do not identify the intended object |
| Lean candidate | `AwesomeTheorems.Stage1.S1_M_086.StatementShape` | Discovery only: its conclusion is an input proposition field, so it is not an exact formalization |
| Foundations | Lean 4 kernel and a versioned mathlib closure | Toolchain, imports, axioms, and TCB remain unfrozen |

## Open intake DAG

1. `M0438-I1`: resolve whether `志田`/“Shida” is the intended name or a corrupted reference.
2. `M0438-I2`: identify a primary publication and exact theorem/page/assumptions/errata.
3. `M0438-I3`: freeze the ordered mathematical statement, objects, boundary cases, and notation.
4. `M0438-I4`: only then elaborate the canonical Lean target and check any transport from the legacy candidate.

These tasks are scope-discovery tasks, not proof obligations, and none is accepted by this intake.

## Intake verdict

Lifecycle is `planned`; root vector is `[H3, M4, R4]`. The first failed gate is exact source
statement identification. No historical “已验证” label or legacy Lean declaration receives proof
credit. The theorem is not complete.

Validation commands and their exact outcomes are recorded in `validation.md`.
