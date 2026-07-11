# Statement-phase blocker

Item: `S56-M-0570-STATEMENT`  
Base revision: `8471ab39f7e977656a7b5ba569063e635a17d5d5`

## Verdict

The exact Lean 4 target cannot yet be frozen truthfully. The accepted intake material records the
repository claim only as "heat-kernel proof of the index theorem" / "Atiyah-Singer theorem by the
heat-kernel method". That description does not determine a unique mathematical proposition. In
particular, it does not choose among:

- the McKean-Singer heat-supertrace identity;
- the cohomological Atiyah-Singer formula for a general elliptic operator;
- a Dirac-type special case; or
- a pointwise local index theorem.

These variants have different domains, operator hypotheses, characteristic classes, coefficient
conventions, normalizations, and conclusions. The intake's `instance.json` therefore deliberately
has `canonical_claim: null` and
`canonical_claim_status: blocked_on_primary_source_and_variant_selection`. Selecting a variant in
this phase would invent missing mathematics and would violate the exact-statement gate in section
5.1 of `Docs/Stage1_Blueprint_rev-5.6.md`.

The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_113.lean` is not a canonical-statement substitute.
Its `StatementShape` quantifies over an abstract `HeatKernelIndexData` record, whose predicates and
index functions are supplied as unconstrained data. Its own documentation calls it a statement
shape candidate and says that the elliptic-operator, heat-kernel, local-density, and
characteristic-class APIs remain abstract. It cannot provide the required source-to-Lean
crosswalk, exact expression fingerprint, or hypothesis mutation results.

Consequently this phase is blocked at the first statement gate. No canonical Lean declaration,
expression hash, alternate-encoding credit, mutation-test acceptance, `M0` credit, audit
completion, or theorem completion is claimed. No `.stage1-worker-selftest.json` is emitted.

## Required unblock

An accountable source reviewer must select a stable primary-source theorem, record its exact
theorem/page and wording, and freeze all operator, manifold, bundle, grading, coefficient, boundary,
and normalization choices. The next statement worker can then encode that proposition without
weakening it, minimize imports, and perform the four required mutation classes.

## Narrow validation evidence

Commands were run from the worker clone on 2026-07-12. No dependency update, fetch, build, or
mutation of the shared `.lake` artifacts was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | exit 0; `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0570` | exit 0; rank 113, `L0`, `rework_required: true`, `lifecycle_mode: planned`, `theorem_complete: false` |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_113.lean)` | exit 0; no output. This establishes only that the legacy abstract boundary elaborates in the pinned environment; it is not exact-statement evidence. |

Known failure: the canonical human claim is absent, so minimal-import determination, canonical
expression serialization, checked transports, and meaningful removed-hypothesis/domain/scope/
boundary mutation tests cannot be performed.
