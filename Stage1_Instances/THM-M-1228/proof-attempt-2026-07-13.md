# THM-M-1228 proof attempt: blocked

Item: `S56-M-1228-PROOF`  
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

## Result

Positive proof execution is blocked at `M1228-S-CONCRETE`. The frozen target
uses `CKNSourceSemantics` because the pinned Lean closure has no concrete
source-faithful definitions of suitable weak Navier-Stokes solutions, regular
points, or one-dimensional parabolic Hausdorff measure. The decay,
epsilon-regularity, bad-cylinder covering, and terminal measure arguments are
also absent. The existing conditional `ObligationTree.root_compose` cannot
produce its open per-solution premise.

`ProofBlocker.lean` makes an additional statement defect precise. It defines an
allowed interface interpretation where suitability is always true and the
measure-zero predicate is always false. Lean kernel-checks:

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

Both declarations report exactly `[propext, Classical.choice, Quot.sound]`.
This is a checked blocker for the arbitrary semantic interface, not a
refutation of the mathematical Caffarelli-Kohn-Nirenberg theorem and not a
positive proof body. The accepted pre-worker registry still records `M4`; this
attempt proposes `M5` for the refutable formal interface, while the genuine CKN
theorem retains its separate provisional human classification `H1`. Only a
versioned statement/registry re-freeze and master acceptance may change those
authoritative records. Root closure, theorem completion, and all later
validation/release claims remain false.

## Validation

All commands ran in the worker clone using the pre-existing canonical `.lake`
link. No update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, planned, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges pass; root remains M4 and the four-node cut set remains open. |
| `cd Stage1_Instances/THM-M-1228 && LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean && LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) ProofBlocker.lean; status=$?; rm -f Statement.olean; exit $status` | 0 | The statement and checked blocker elaborate; both negative declarations report `[propext, Classical.choice, Quot.sound]`; the temporary owned olean is removed. |
| `rg -l -i -g '*.lean' '(caffarelli\|kohn\|nirenberg\|navier.?stokes\|suitable.?weak\|parabolic.?hausdorff\|epsilon.?regular)' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Only the unrelated Gagliardo-Nirenberg-Sobolev source matches; no CKN body is present. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | No prohibited Lean proof-gap declaration; exit 1 means no match. |
| `git diff --check -- Stage1_Instances/THM-M-1228` | 0 | No whitespace errors. |

## Retry condition

Refreeze a statement around concrete source-faithful analytic definitions, then
provide placeholder-free local implementations or an immutable compatible
dependency for `M1228-S-CONCRETE`, `M1228-E-EPSILON`, `M1228-C-COVER`, and
`M1228-L-MEASURE`, including exact transports and terminal-body provenance.

The assigned positive proof phase is not self-tested complete, so no
`.stage1-worker-selftest.json` is emitted.
