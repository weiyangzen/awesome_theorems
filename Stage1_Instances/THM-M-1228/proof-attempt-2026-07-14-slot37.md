# THM-M-1228 proof-phase recheck: blocked

Item: `S56-M-1228-PROOF`  
Attempt date: 2026-07-14 (`Asia/Shanghai`)  
Base revision: `3bb4cb3ae15dff8b48c93242019edec3bf858e48`  
Base tree: `8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc`

## Verdict

`blocked`: no positive proof body can inhabit the exact frozen interface.
`CaffarelliKohnNirenbergTarget S` is a proposition for an arbitrary
`CKNSourceSemantics`, whose suitability, regularity, and parabolic-measure
predicates have no laws connecting them. The placeholder-free
`ProofBlocker.lean` instantiates suitability as true and the measure-zero
predicate as false, and Lean checks both
`counterexampleTargetIsFalse` and `noUniformTargetProof`. A positive uniform
proof would contradict that countermodel.

This does not refute the mathematical Caffarelli-Kohn-Nirenberg theorem. It
shows that the frozen formal statement is only an unconstrained semantic
interface. Proving a convenient instantiation, assuming the per-solution
conclusion, or substituting ambient Euclidean Hausdorff measure would change
the assigned theorem and is therefore rejected. The predecessor registry is
not modified by this proof worker; it continues to report the root as `M4`.
The current interface has checked `M5` blocker evidence, but changing the
authoritative classification requires a versioned statement/registry repair
and master reconciliation.

## Validation

All commands ran from this worker clone using the automation-provided symlink
to the canonical pinned `.lake` artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network action, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Toolchain and mathlib pin agree; expression SHA-256 is `101ce8f2...f58e5f`; all four registered statement mutations were killed. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok`: M4 boundary, nine Lean probes, mathlib pin, and four immutable external-tree receipts agree. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut set. |
| `LEAN_PATH="$(cd Formalizations/Lean && lake env printenv LEAN_PATH)" "$(cd Formalizations/Lean && lake env which lean)" -o Stage1_Instances/THM-M-1228/Statement.olean Stage1_Instances/THM-M-1228/Statement.lean; LEAN_PATH="Stage1_Instances/THM-M-1228:$(cd Formalizations/Lean && lake env printenv LEAN_PATH)" "$(cd Formalizations/Lean && lake env which lean)" Stage1_Instances/THM-M-1228/ProofBlocker.lean; status=$?; rm -f Stage1_Instances/THM-M-1228/Statement.olean; exit "$status"` | 0 | The exact statement and checked countermodel elaborate; the temporary owned olean was removed. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | No prohibited proof-gap or unsafe declaration; exit 1 is ripgrep's no-match result. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The statement source SHA-256 is
`e5360836f4875e028eabdbf3e76c860aa1566a0f2f4eeb1487588c6ee55ddcc5`;
the checked countermodel source SHA-256 is
`b7c0043752d40a41350080fe5210b65aca2594a2c8cdbae139c3ab058ffacca5`.
The pre-existing untracked `.lake` symlink makes this nonrelease evidence.

## Retry Condition

Reopen and version the statement around fixed, source-faithful definitions of
suitable weak Navier-Stokes solutions, regular points, and one-dimensional
parabolic Hausdorff measure. Freeze a corrected registry, then provide
placeholder-free local bodies or an immutable compatible dependency for
`M1228-S-CONCRETE`, `M1228-E-EPSILON`, `M1228-C-COVER`, and
`M1228-L-MEASURE`, with exact transports and terminal-body provenance.

No positive proof body was added, the root is open, and theorem completion is
false. Because the assigned proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
