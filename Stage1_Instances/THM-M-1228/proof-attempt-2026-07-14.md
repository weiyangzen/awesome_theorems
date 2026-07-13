# THM-M-1228 proof-phase recheck: blocked

Item: `S56-M-1228-PROOF`  
Attempt date: 2026-07-14 (`Asia/Shanghai`)  
Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`  
Base tree: `da6f991c07f11e8608ddc090af9356558d64d360`

## Verdict

`blocked`: the exact frozen Lean target cannot receive a positive proof body.
`CaffarelliKohnNirenbergTarget S` is parameterized by an unconstrained
`CKNSourceSemantics`; it is not a theorem uniformly true of every such `S`.
The existing placeholder-free `ProofBlocker.lean` gives an allowed
interpretation with suitability identically true and the measure-zero
predicate identically false. Lean kernel-checks:

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

Consequently, a uniform positive proof would contradict this checked
countermodel. Proving the target for a convenient interpretation, adding the
per-solution conclusion as a premise, or replacing parabolic Hausdorff measure
by ambient Euclidean Hausdorff measure would broaden or substitute the frozen
theorem. The conditional `ObligationTree.root_compose` already checks binder
assembly, but its `perSolution` argument is exactly the open analytic theorem
and therefore supplies no root proof credit.

This mismatch is `M5` evidence for the current formal interface. The frozen
predecessor registry is not edited by this proof worker and continues to report
the root at `M4` pending a versioned statement/registry repair and master
reconciliation. The genuine mathematical Caffarelli-Kohn-Nirenberg theorem is
not refuted; its provisional human classification remains separately `H1`.

## Validation

All checks ran in this worker clone using the automation-provided symlink to
the canonical pinned `.lake` artifacts. No `lake update`, `lake build`, clone,
fetch, network action, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Toolchain and mathlib pin agree; expression SHA-256 is `101ce8f2...f58e5f`; all four registered statement mutations were killed. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok`: M4 boundary, nine Lean probes, mathlib pin, and four immutable external-tree receipts agree. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut set. |
| `cd Stage1_Instances/THM-M-1228; LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean && LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) ProofBlocker.lean; status=$?; rm -f Statement.olean; exit $status` | 0 | The exact target and both negative declarations elaborate. Each negative declaration reports `[propext, Classical.choice, Quot.sound]`; the temporary `Statement.olean` was removed. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | No prohibited proof-gap or unsafe declaration; exit 1 is ripgrep's no-match result. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The statement source SHA-256 is
`e5360836f4875e028eabdbf3e76c860aa1566a0f2f4eeb1487588c6ee55ddcc5`;
the checked countermodel source SHA-256 is
`b7c0043752d40a41350080fe5210b65aca2594a2c8cdbae139c3ab058ffacca5`.
The pre-existing untracked `.lake` symlink makes this nonrelease evidence.

## Retry Condition

Reopen and version the statement around fixed, source-faithful definitions of
suitable weak Navier-Stokes solutions, regular points, and one-dimensional
parabolic Hausdorff measure. Then freeze a corrected obligation registry and
provide placeholder-free local bodies or an immutable compatible dependency
for `M1228-S-CONCRETE`, `M1228-E-EPSILON`, `M1228-C-COVER`, and
`M1228-L-MEASURE`, with exact transports and terminal-body provenance.

No positive proof body was added, the root is open, and theorem completion is
false. Because the assigned proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
