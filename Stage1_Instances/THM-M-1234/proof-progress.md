# THM-M-1234 proof execution

Item: `S56-M-1234-PROOF`. Execution date: 2026-07-12. Base revision:
`9258763ef5d98df2b13458756f43399dd7e63278`.

## Result

The proof phase is blocked and is not self-tested as complete. `Proof.lean`
adds a real kernel-checked proof of the zero-initial-data boundary case. Its
velocity and vorticity are identically zero; the weak divergence, curl,
momentum equation, integrability, and one-sided trace fields are discharged
directly. This is only a proper special case of the frozen universal target.

The canonical `Stage1Rev56.THMM1234.Statement` remains open for arbitrary
`InitialData`. In the frozen proof graph, the first unresolved root cut is
`M1234-A-STRUCTURE` plus `M1234-E-CLOSURE`: mathlib supplies neither the global
smooth approximation/compactness construction nor passage of the nonlinear
Euler term and initial trace. The predecessor anchor audit found no exact
external Lean closure. Implementing those analytic packages is the concrete
retry condition. The checked special case is not substituted for the root and
does not advance the root beyond `M3` or claim theorem completion.

## Validation

Validation used the existing pinned Lake environment. No update, build,
dependency clone, or fetch was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows,
  300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-1234
  exit 0
  rank 158; planned; L0/rework-required; theorem_complete=false

LEAN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-1234
LEAN_PATH="$LEAN_PATH" "$LEAN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN" Proof.lean
rm -f Statement.olean
  exit 0
  zero_data_solution axioms: [propext, Classical.choice, Quot.sound]
  zero_data_statement axioms: [propext, Classical.choice, Quot.sound]
  zero_initial_data axioms: [propext, Classical.choice, Quot.sound]
```

The initial direct `lake env lean ../../Stage1_Instances/THM-M-1234/Proof.lean`
attempt exited 1 because the sibling `Statement` module had no compiled module
on Lean's search path. The recorded successful command compiles `Statement.lean`
to a temporary owned `Statement.olean`, adds the owned directory to `LEAN_PATH`,
checks `Proof.lean`, and deletes the temporary artifact.

No `.stage1-worker-selftest.json` is emitted because the assigned universal
proof phase has not passed its completion gate.
