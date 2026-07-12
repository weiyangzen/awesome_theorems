# Statement-phase blocker

Item: `S56-M-0718-STATEMENT`  
Base revision: `3a479c703900e8096e6b239e7bf5b0da25472b8a`  
Checked on: 2026-07-12 (Asia/Shanghai)

## Verdict

The exact Lean 4 target cannot truthfully be frozen from the available source record. The
repository's entire claim is `通用计算模型` ("universal computation model"). It gives no quantified
statement, machine definition, program/input encoding, simulation relation, divergence semantics,
or source location. The separate `THM-C-0003` wording is metadata for another target and cannot be
used to broaden this one.

Consequently the rev-5.6 statement gate remains blocked at its first prerequisite: exact canonical
mathematical claim identity. There is no declaration/expression or normalized expression hash to
record, and mutation tests would test an invented target rather than the source claim. No proof
evidence was inspected or credited. The existing `[H1, M3, R4]` classification remains unchanged.

## Candidate inspected, not selected

The pinned module `Mathlib.Computability.TuringMachine.ToPartrec` elaborates the substantial
candidate

```lean
Turing.PartrecToTM2.tr_eval (c : Turing.ToPartrec.Code) (v : List Nat) :
  eval (Turing.TM2.step Turing.PartrecToTM2.tr)
      (Turing.PartrecToTM2.init c v) =
    Turing.PartrecToTM2.halt <$> c.eval v
```

and `Turing.PartrecToTM2.tr_supports`. This does not resolve whether the intended theorem requires
one fixed finite machine, a transition function with program-dependent reachable finite support,
or another classical machine and encoding. Treating it as canonical would therefore be a
substituted theorem.

## Validation evidence

The worker reused the existing pinned `.lake` artifacts and did not update, build, clone, fetch, or
otherwise mutate dependencies.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0718` | exit 0; rank 757, lifecycle `planned`, theorem completion false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0718/IntakeProbe.lean)` | exit 0 under pinned Lean 4.29.0; all seven API declarations elaborated, including `tr_eval` and `tr_supports` |

## Unblocking condition

An independently inspected primary source must supply an exact passage and stable edition/page (or
another immutable locator). The next statement attempt must crosswalk that passage to a fixed
machine model, ordered quantifiers, encodings, partial semantics, correctness relation, finiteness
conditions, malformed-input and divergence behavior, and all boundary cases. Only then can it add
the minimal-import Lean target, serialize its elaborated expression/environment fingerprint, and
run the required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

This phase is not self-tested as complete, so no `.stage1-worker-selftest.json` is emitted.
