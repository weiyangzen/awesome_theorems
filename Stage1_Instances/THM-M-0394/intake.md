# THM-M-0394 Intake: Siegel's Theorem

## Instance Boundary

- Item: `S56-M-0394-INTAKE`
- Lifecycle: `planned`
- Baseline: `L0 / rework_required`
- Lane: `hard_mathlib_anchor_and_wrapper`
- Canonical topic: finiteness of integral points on affine algebraic curves over number fields.
- Completion boundary: this intake freezes a research scope only. It does not freeze an exact Lean statement, establish source fidelity, or prove any instance of Siegel's theorem.

## Human Claim And Scope Map

The intended classical claim is the following standard form. Let `K` be a number field, let `S` be a finite set of places containing the archimedean places, and let `C/K` be a smooth geometrically integral affine curve. Choose a smooth projective completion `Cbar`, and let `D = Cbar \ C` be its boundary. If either the genus of `Cbar` is positive, or the genus is zero and the geometric boundary has at least three points, then the set of `S`-integral `K`-points of `C` is finite.

This wording is an intake-level mathematical target, not yet the canonical formal expression. The statement phase must settle the model and integrality dependence, including whether the boundary count is over an algebraic closure, whether it counts support or degree, and how `S` and the chosen integral model enter the predicate.

| Scope component | Included interpretation | Still to freeze in statement phase |
|---|---|---|
| Base | arbitrary number field `K` | universe and exact mathlib `NumberField` interface |
| Places | finite `S`, including infinite places | place API versus finite-prime localization API |
| Curve | smooth, geometrically integral affine curve over `K` | scheme API, dimension-one condition, and compactification data |
| Boundary | complement in a smooth projective completion | geometric support cardinality/degree and independence of completion |
| Hypothesis | positive genus, or genus zero with at least three boundary points | exact equivalent formulation and transport directions |
| Points | `K`-rational points integral outside `S` | integral model and predicate invariance |
| Conclusion | finiteness as a set | exact set/subtype and `Set.Finite` expression |

Degenerate cases are not silently absorbed: an empty point set is finite; genus zero with fewer than three geometric points at infinity is excluded from the proposed sufficient hypothesis; singular or reducible curves are outside this normalized form until a checked reduction is supplied.

## Source-Statement Crosswalk

| Source ID | Source and locator | Role | Mapping and caveat |
|---|---|---|---|
| `SRC-SIEGEL-1929` | C. L. Siegel, *Uber einige Anwendungen diophantischer Approximationen*, Abhandlungen der Preussischen Akademie der Wissenschaften, Physikalisch-Mathematische Klasse, 1929, no. 1 | primary historical source | Establishes the classical finiteness method behind the theorem. Exact theorem/page, notation, hypotheses, and errata have not yet been independently checked, so this record is `H3`, not `H0`. |
| `SRC-LANG-FDG` | Serge Lang, *Fundamentals of Diophantine Geometry*, Springer, 1983, Chapter VIII | modern book cross-check | Provides modern integral-point language and a route for comparing genus/boundary formulations. It is secondary and cannot by itself close primary-source fidelity. |
| `LEGACY-S1-M-007` | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_007.lean`, repository base `a8d6489fd935cd71fa4499f2f3f5b051998203f4` | discovery-only Lean artifact | Its `StatementShape` quantifies over predicate fields and explicitly says exact object APIs are unselected. It is not accepted statement or proof evidence under rev-5.6. |

Crosswalk status: the base field, geometric curve, boundary condition, integrality predicate, and finiteness conclusion all have identified source concepts, but none yet has a pinpoint primary-source locator plus reviewed assumption map. Human debt is therefore `H3`; machine debt is `M4` because the exact canonical target is not elaborated; readability debt is `R3` because this intake has no independent review.

## Open Intake DAG

1. `STMT-BASE`: select exact number-field, place, and `S`-integer APIs.
2. `STMT-CURVE`: select the smooth geometrically integral curve and projective-completion APIs.
3. `STMT-BOUNDARY`: formalize genus and geometric boundary cardinality.
4. `STMT-INTEGRAL`: formalize `S`-integral points and model invariance.
5. `STMT-ROOT`: elaborate the exact quantified finiteness proposition and checked transports.
6. `SRC-PINPOINT`: inspect the primary edition for theorem/page, assumptions, and errata.
7. `ANCHOR-AUDIT`: audit repo-local, pinned mathlib, and external Lean 4 candidates after the statement is frozen.

All seven tasks are open. Tasks 1--6 feed `STMT-ROOT`; `ANCHOR-AUDIT` depends on the accepted statement phase. No proof obligation receives closure credit from this dossier.

## Intake Validation

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

The worker ran the following repository checks before writing this dossier:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
python3 scripts/stage1_target.py check
  exit 0: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
python3 scripts/stage1_target.py show THM-M-0394
  exit 0: rank 7, L0/rework_required, planned, theorem_complete false
```

Known failures/open gates: exact source pinpointing, exact Lean elaboration, mutation checks, anchor audit, kernel proof, independent source/readability review, and master acceptance are all intentionally pending beyond intake.
