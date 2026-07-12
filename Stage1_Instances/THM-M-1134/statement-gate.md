# Statement gate: blocked

Item: `S56-M-1134-STATEMENT`

Base revision: `f4f075401578599668ebc61cf26de19055cb97e4`.

## Gate result

The exact Lean 4 target cannot be truthfully frozen or elaborated from the available source record.
The only mathematical statement in `Docs/researches/math_theorems.md` is `正解的下界估计`
("lower-bound estimate for positive solutions"). `Docs/Stage0_Blueprint.md` repeats that phrase and
explicitly leaves the precise definitions and assumptions open. Neither record identifies a
primary source, theorem number, page, or a particular formulation of the parabolic Harnack
inequality.

The phrase does not determine the spatial dimension, spatial domain, time interval, heat-operator
normalization, solution/regularity predicate, positivity convention, comparison points or
cylinders, time ordering, boundary separation, inequality constant, or its dependencies. These
choices distinguish inequivalent theorems. Introducing any of them would broaden or substitute the
repository claim rather than elaborate its exact target. Consequently there is no canonical Lean
expression, minimal import set, expression hash, checked alternate encoding, or legitimate mutation
suite to record.

The prerequisite `S56-M-1134-INTAKE` is also only provisional (`[_]`) in the generated blueprint,
not master-accepted (`[x]`). No dependency-legal statement acceptance is claimed.

## First failed gate and retry condition

First failed gate: rev-5.6 section 5 target identity. The canonical human claim is ambiguous, so
section 5.1 Lean elaboration must fail closed before proof or anchor evidence is inspected.

Retry only after an accountable source decision supplies a primary-source edition, theorem/page,
assumption and errata crosswalk and freezes every parameter listed above. After master acceptance of
the intake dependency, the statement phase can encode that exact claim, determine minimal pinned
imports, elaborate it with fixed options, fingerprint the expression/environment, and run the four
required mutation classes.

## Scoped validation record

All commands were run in the worker clone on 2026-07-12. No dependency fetch, update, or build was
performed, and the canonical `.lake` symlink was not modified.

| Command | Exact result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | exit 0; `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1134` | exit 0; rank 339, baseline `L0`, `rework_required: true`, lifecycle `planned`, `theorem_complete: false` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; `Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)` |
| `rg -n -C 5 "热方程的Harnack不等式|正解的下界估计" Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; located only the underspecified metadata statement and its Stage0 repetition |

Known failure: exact-target elaboration was not run because no exact target exists in the source
record. Running Lean on a chosen parabolic Harnack variant would be fake evidence for this item.
This phase is blocked, is not self-tested, and does not support a `.stage1-worker-selftest.json`.
