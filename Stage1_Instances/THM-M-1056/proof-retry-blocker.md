# THM-M-1056 proof retry blocker

Item: `S56-M-1056-PROOF`  
Base revision: `0afbf514f9bd5f339943542106f6b811869fe572`  
Attempt date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`; the assigned proof phase is not self-tested as complete. No proof
body was added, no frozen obligation was closed, and no worker self-test
manifest was written.

The exact target is the full finite-dimensional, invertible Oseledets splitting
theorem. The only local composer,
`Stage1Instances.THM_M_1056.root_of_oseledetsCorePackage`, assumes
`OseledetsCorePackage`, which is definitionally the entire target. It is a
checked conditional interface, not a proof.

The first failed root cut remains `M1056-T-CORE`. Its necessary open branches
include the Kingman bridge, exterior-power processes, forward and backward
Lyapunov flags, transversality, strongly measurable complementary projections,
equivariance, simultaneous vector growth, and transport from matrix coordinates
to the arbitrary finite-dimensional normed Borel fiber.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains no named
Kingman or Oseledets terminal declaration. Repo and package inspection found no
already-present external source or compiled artifact supplying one, and the
target assumptions contain no contradiction that could close the proposition
vacuously. The audited external anchor
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
is absent from the pinned closure, requires Lean 4.30.0-rc2 and a different
mathlib revision, and proves a matrix/submodule formulation without the checked
polymorphic coordinate and projection transports required by this target. It
cannot receive proof credit here.

## Fresh validation

No dependency was updated, built, cloned, or fetched, and `.lake` was not
modified.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; `rework_required: true`; `theorem_complete: false`. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | 19 obligations and 49 typed edges passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root open M3; core M4. |
| `rg -n '\\b(sorry|admit|axiom)\\b|sorryAx' Stage1_Instances/THM-M-1056 --glob '*.lean'` | 1 | No prohibited proof token in owned Lean sources; exit 1 means no match. |
| `rg -n -i '(^|[^A-Za-z])(oseledets|multiplicative ergodic|kingman)([^A-Za-z]|$)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No named terminal Oseledets or Kingman declaration; exit 1 means no match. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| from `Formalizations/Lean`: `LEAN_NUM_THREADS=1 lake env lean --root=../../Stage1_Instances/THM-M-1056 -o /tmp/thm-m-1056-lake-env-retry.deL9fE/Statement.olean ../../Stage1_Instances/THM-M-1056/Statement.lean`, then `LEAN_NUM_THREADS=1 LEAN_PATH=/tmp/thm-m-1056-lake-env-retry.deL9fE:$(lake env printenv LEAN_PATH) lake env lean --root=../../Stage1_Instances/THM-M-1056 ../../Stage1_Instances/THM-M-1056/ObligationTree.lean` | 0 | Exact statement and conditional composition freshly elaborated through `lake env lean`; unused-binder warnings only. `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary output was removed. |

The shared host was heavily saturated during validation; `LEAN_NUM_THREADS=1`
kept the narrow replay bounded. The pre-existing untracked
`Formalizations/Lean/.lake` link remains nonrelease evidence and was not changed
by this worker.

After writing this report, `git diff --check -- Stage1_Instances/THM-M-1056`
exited 0 with no output.

## Reopen condition

Resume only after providing placeholder-free bodies at the frozen types for the
open core branches, or after making an immutable, compatible external proof
available with checked exact transports, terminal provenance, and trust data.
Until then the root stays `[H1, M3, R3]`; this proof item cannot truthfully
receive `[_]`, an accepted receipt, or theorem-completion credit.
