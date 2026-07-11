# THM-M-0404 Intake Dossier

Lifecycle: `planned`. This dossier records intake scope only. It accepts no legacy proof credit and does not claim an elaborated exact target, audit completion, or theorem completion.

## Scope map

The intended claim is the Skolem-Mahler-Lech theorem for a `Nat`-indexed linear recurrence over an arbitrary characteristic-zero field. The candidate Lean surface quantifies `K`, its `Field` and `CharZero` instances, `E : LinearRecurrence K`, and `u : Nat -> K`, assumes `E.IsSolution u`, and describes the zero predicate by finite lists of exceptional indices and arithmetic progressions.

In scope are zero-order recurrences, the identically zero sequence, the empty zero set, finite zero sets, and progressions with step zero. No nondegeneracy, invertibility, algebraic-closedness, or recurrence-order assumption may be added silently. The exact behavior of the list encoding, duplicate entries, one-sided progressions, and the equivalence with eventual periodicity must be checked in the statement phase.

The historical file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_017.lean` is discovery input only. Its `StatementShape` is the candidate canonical expression; `StatementShapeEventuallyPeriodic` is an alternate encoding with an explicitly unproved bridge at intake.

## Source-statement crosswalk

| Source surface | Source wording / role | Candidate Lean component | Intake status |
|---|---|---|---|
| Stage0 entry `THM-M-0404` | "Skolem-Mahler-Lech theorem"; zeroes of a linear recurrence | Entire candidate target | Metadata label only; not source evidence |
| `Docs/Stage1_Blueprint.md`, S1-M-017 | Linear recurrence sequence zero indices | `E`, `u`, `E.IsSolution u`, `u n = 0` | Legacy discovery only |
| Classical finite-union formulation | Zero set is a finite set plus finitely many arithmetic progressions | `IsFiniteUnionOfArithmeticProgressions` | Mathematical wording frozen provisionally; primary edition/theorem/page audit remains open |
| Classical eventual-periodic formulation | Membership in the zero set is eventually periodic | `IsEventuallyPeriodic` | Alternate target only; equivalence is not credited |
| Historical Lean candidate | Characteristic-zero field formulation | `StatementShape` | Candidate only; exact elaboration/hash and mutation tests belong to the dependent statement node |

No primary-source theorem/page/errata record was established during this bounded intake. Consequently human-source status is not `H0`; the anchor-audit node must locate and independently review the original Skolem/Mahler/Lech statements and reconcile their domains and recurrence conventions.

## Open task DAG

`S56-M-0404-STATEMENT` -> `ANCHOR_AUDIT` -> `OBLIGATION_TREE` -> `PROOF` -> `VALIDATION` -> `RELEASE`. The first task must minimally elaborate the candidate, record normalized expression and environment hashes, check the eventual-periodic transport (or retain it as non-machine), and mutation-test hypotheses, domain, binder scope, and boundary cases. No obligation registry or discovery result is frozen by this intake.

## Intake validation

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

Commands executed from repository root on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0404
  exit 0: execution rank 17, planned, theorem_complete false
```

These are real membership and structural checks, not Lean proof validation. Node-specific self-test also validates JSON parsing and whitespace below; master acceptance remains outstanding.
