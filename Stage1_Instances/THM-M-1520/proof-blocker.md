# THM-M-1520 proof-phase blocker

Item: `S56-M-1520-PROOF`

Attempt date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `309f58b7a54d36653b3483a543c6378eea53882c`

Base tree: `1051ab77fe56d6e32ba26761bbcfd3ad8a258743`

## Verdict

`blocked`: this attempt makes real proof progress but does not complete the assigned proof phase.
The exact target `Stage1.THM_M_1520.LiouvilleStatement` remains open, lifecycle remains `planned`,
and the recorded root vector remains `[H2, M3, R3]`. There is no proof receipt, master acceptance,
validation/release claim, H0/R0 claim, theorem-completion claim, or worker self-test manifest.

Two new placeholder-free Lean bodies implement dependency-legal parts of the frozen route:

| Declaration | Exact contribution | Status boundary |
|---|---|---|
| `Stage1.THM_M_1520.timeMap_bijective` | derives that every `Phi t` is bijective with inverse `Phi (-t)` from the frozen identity and flow laws | algebraic subbranch of `M1520-N-FLOW`; no spatial regularity |
| `Stage1.THM_M_1520.measurePreserving_of_det_fderiv_eq_one` | applies pinned mathlib's nonlinear change-of-variables theorem to turn differentiability, bijectivity, and determinant one into volume preservation | terminal measure-transport step of `M1520-L-CHANGE`; its three hypotheses remain to be produced for `Phi t` |

The earlier `Proof.lean` bodies `timeZero_measurePreserving` and
`zeroDimension_measurePreserving` remain genuine `M1520-S-BOUNDARY` results. The existing
`liouvilleStatement_of_analyticPackage` is only a conditional composer: it consumes, rather than
constructs, `LiouvilleAnalyticPackage`. None of these declarations closes an entire frozen
obligation, the analytic package, `M1520-T-ALL-TIMES`, or the root.

The first failed proof-completion gate and graph-derived minimal root cut remain
`M1520-T-ALL-TIMES`. Expanded missing work includes spatial differentiability of the global flow
(`M1520-N-FLOW`), zero divergence from the symmetric Hessian (`M1520-B-DIVERGENCE`), the spatial
variational equation (`M1520-C-VARIATION`), determinant-one evolution (`M1520-L-JACOBIAN`), the
resulting measurable/differentiable time maps (`M1520-L-MEASURABLE`), assembly of the
change-of-variables inputs (`M1520-L-CHANGE`), and construction of the all-times analytic package.

Pinned mathlib has local Picard-Lindelof and ODE uniqueness infrastructure, but no theorem deriving
the required differentiable dependence on initial conditions or Jacobian evolution from the
frozen orbitwise time-derivative hypotheses. Its topological `Flow` API yields homeomorphisms only
after joint continuity is supplied and has no volume-preservation theorem. No exact Hamiltonian
Liouville theorem exists in the pinned closure. Assuming the missing analytic package, weakening
the target, or adding a moving dependency would not be a valid implementation.

## Validation evidence

Commands ran in this worker clone using the existing pinned Lean artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed. The pre-existing untracked
`Formalizations/Lean/.lake` symlink was left unchanged, so this is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard valid: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest valid: 1546 unique targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1520` | 0 | Rank 189, lifecycle `planned`, baseline L0/rework-required, theorem incomplete. |
| Pinned temporary-copy Lean recipe below | 0 | All four modules elaborated; both new declarations are sorry-free; every printed axiom set is exactly `[propext, Classical.choice, Quot.sound]`. |
| `python3 Stage1_Instances/THM-M-1520/check_obligation_tree.py` | 0 | Frozen registry structurally valid: 16 obligations and 32 typed edges. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 (expected) | No `sorry`, `admit`, `sorryAx`, `implemented_by`, `native_decide`, `extern`, or prohibited declaration token. |
| `python3 -m json.tool Stage1_Instances/THM-M-1520/proof-blocker.json` | 0 | Blocker record is valid JSON. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No self-test manifest exists because the proof phase is incomplete. |
| Scoped whitespace and new-file hygiene checks | 0 | No whitespace error, CR, NUL, missing final newline, or trailing whitespace in the changed owned files. |

The exact narrow Lean recipe was:

```bash
TMP=$(mktemp -d .thm1520-final-lean.XXXXXX)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cp Stage1_Instances/THM-M-1520/{Statement,Proof,FlowAlgebra,JacobianBridge}.lean "$TMP/"
LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 240 "$LEAN" --trust=0 \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LP" timeout 240 "$LEAN" --trust=0 \
  "$TMP/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LP" timeout 240 "$LEAN" --trust=0 \
  "$TMP/FlowAlgebra.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 240 "$LEAN" --trust=0 \
  "$TMP/JacobianBridge.lean"
rm -rf "$TMP"
```

Its exact status summary was
`statement_exit=0 proof_exit=0 flow_algebra_exit=0 jacobian_bridge_exit=0`.
`#print sorries` printed `Declarations are sorry-free!` for both new bodies. `#print axioms`
reported `[propext, Classical.choice, Quot.sound]` for the two earlier boundary bodies and the two
new declarations, with no `sorryAx`.

## Reopen condition

Resume only with placeholder-free implementations, or an immutable compatible pinned dependency,
for the positive-dimensional spatial-flow regularity, divergence/variation/Jacobian evolution, and
their checked composition into `LiouvilleAnalyticPackage`. The two new bodies can then discharge
inverse-time bijectivity and the final nonlinear measure transport. This blocker record and the
earlier `proof-execution.md` are partial-attempt evidence, not authoritative task closure.
