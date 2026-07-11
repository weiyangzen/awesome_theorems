# Statement phase blocker

Item: `S56-M-0008-STATEMENT`  
Base revision: `9e3fd02a2a952da7031bb1dd61387443dd4c1cc7`  
Checked: 2026-07-12

## First failed gate

The rev-5.6 exact-statement gate fails before a canonical Lean declaration may be frozen. The only
repository source wording is `Tor函子的性质` ("properties of the Tor functor") in
`Docs/researches/math_theorems.md`. It gives no proposition, domains, ordered binders, hypotheses,
conclusion, boundary cases, author, title, theorem number, or page. The accepted intake correctly
classifies this as `blocked_on_primary_source_and_statement_disambiguation`.

At least the following mutually non-equivalent roots fit the wording: projective/flat vanishing,
balancedness of the two derived tensor variables, a Tor long exact sequence, and a degree-zero
identification. Selecting any one without a source selection rule would broaden or substitute the
unknown claim. Consequently there is no truthful elaborated-expression hash, canonical target,
alternate-encoding transport, or removed-hypothesis/domain/scope/boundary mutation suite to record.

## Narrow Lean check

`StatementCandidateProbe.lean` imports only `Mathlib.CategoryTheory.Monoidal.Tor` and checks that
the pinned environment can elaborate one candidate family, higher Tor vanishing against a
projective second argument. This is discovery evidence only and is explicitly not a canonical
statement. The checked toolchain is `leanprover/lean4:v4.29.0`; the manifest pins mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, which matches the reused local mathlib checkout.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0008` | 0 | rank 101; lifecycle `planned`; baseline `L0`; `theorem_complete: false` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0008/StatementCandidateProbe.lean` | 0 | Elaborated `CategoryTheory.Tor`, `Tor'`, `isZero_Tor_succ_of_projective`, and the explicitly typed candidate expression; no errors. |

## Retry condition and boundary

Retry only after the master supplies or accepts a stable primary-source selection with a pinpoint
theorem and enough text to crosswalk every assumption and conclusion. Then elaborate exactly that
claim with pinned imports and run the four required semantic mutation classes.

This artifact does not complete the statement node, accept a receipt, alter the execution DAG, or
claim audit/theorem completion. No `.stage1-worker-selftest.json` is emitted because the assigned
deliverable is not self-tested.
