# THM-M-1520 proof-phase recheck at ffea62ba

Item: `S56-M-1520-PROOF`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330`

Base tree: `4662e08d189bd534919775f750c6909591aeafcb`

## Verdict

`blocked`. The exact target `Stage1.THM_M_1520.LiouvilleStatement` has no proof body in the owned
source or pinned dependency closure. This recheck adds no proof body and closes no obligation. The
lifecycle remains `planned`, and the root vector stays `[H2, M3, R3] -> [H2, M3, R3]`.

The graph-derived minimal root cut and first failed proof-completion gate are
`M1520-T-ALL-TIMES`. The expanded open analytic work is `M1520-N-FLOW`,
`M1520-B-DIVERGENCE`, `M1520-C-VARIATION`, `M1520-L-JACOBIAN`,
`M1520-L-MEASURABLE`, `M1520-L-CHANGE`, and `M1520-T-ALL-TIMES`.

Pinned mathlib provides local Picard-Lindelof existence and uniqueness plus Lipschitz or continuous
initial-point dependence. It does not provide the spatial differentiable dependence, variational
equation, Jacobi determinant evolution, or Hamiltonian-flow volume theorem needed here. The audited
`velvetmonkey/hamiltonian-lean` result is one-dimensional, assumes the decisive abstract Jacobian
evolution equation, and does not conclude `MeasurePreserving`; importing it would not close this
target.

## Checked Partial Bodies

| Declaration | Revalidated contribution | Open boundary |
|---|---|---|
| `Stage1.THM_M_1520.timeZero_measurePreserving` | volume preservation at `t = 0` | does not close the full boundary obligation or positive-dimensional case |
| `Stage1.THM_M_1520.zeroDimension_measurePreserving` | volume preservation at `n = 0` | does not close the positive-dimensional case |
| `Stage1.THM_M_1520.timeMap_bijective` | inverse-time bijectivity from the flow laws | supplies no spatial differentiability for `M1520-N-FLOW` |
| `Stage1.THM_M_1520.measurePreserving_of_det_fderiv_eq_one` | nonlinear measure transport from differentiability, bijectivity, and determinant one | those analytic inputs remain unconstructed for `Phi t` |
| `Stage1.THM_M_1520.liouvilleStatement_of_analyticPackage` | exact conditional composition to the root | consumes, rather than constructs, `LiouvilleAnalyticPackage` |

These declarations are genuine placeholder-free partial results. They do not close
`LiouvilleAnalyticPackage`, `M1520-T-ALL-TIMES`, or the root. The earlier `proof-blocker.*` and
`proof-execution.md` records are historical partial-attempt evidence based on older revisions; this
pair binds the current base.

## Failed Gate And Retry

The first failed gate is `M1520-T-ALL-TIMES`: there is no checked construction of the analytic
package for every time. Resume only with placeholder-free implementations of positive-dimensional
spatial-flow regularity, Hamiltonian zero divergence, the spatial variational equation,
determinant-one Jacobian evolution, measurability and change-of-variables inputs, and their checked
composition into `LiouvilleAnalyticPackage`, either locally or through an immutable compatible
pinned dependency.

## Validation

All checks ran in this worker clone against the existing pinned Lake artifacts. The pre-existing
untracked `Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, network access, or `.lake` mutation was performed. Temporary Lean objects
were removed after the replays.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1520` | 0 | Rank 189; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| Isolated trust-zero five-module Lean recipe below | 0 | `statement=0 proof=0 flow_algebra=0 jacobian_bridge=0 obligation_tree=0`; every printed axiom set was `[propext, Classical.choice, Quot.sound]`, and FlowAlgebra/JacobianBridge explicitly reported sorry-free declarations. |
| `python3 Stage1_Instances/THM-M-1520/check_obligation_tree.py` | 0 | 16 obligations and 32 typed edges passed; denominator `3e5ecbc...e4c`; root open at M3 and analytic package open at M4. |
| token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom-like declaration, unsafe/oracle, or equivalent prohibited construct. |
| `python3 -m json.tool Stage1_Instances/THM-M-1520/proof-recheck-2026-07-14-head-ffea62ba.json` | 0 | The fresh structured blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1520` | 0 | No whitespace errors in tracked owned-path changes. |
| `git diff --no-index --check /dev/null <fresh-artifact>` for each new file | 1 each | Expected new-file diff exits with empty diagnostic output; both fresh artifacts have no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion self-test manifest. |

The successful narrow Lean replay was:

```bash
set -u
tmp=$(mktemp -d .thm1520-root-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1520/{Statement,Proof,FlowAlgebra,JacobianBridge,ObligationTree}.lean "$tmp/"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 240 "$lean" --trust=0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean" --trust=0 \
  "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean" --trust=0 \
  "$tmp/FlowAlgebra.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 240 "$lean" --trust=0 \
  "$tmp/JacobianBridge.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean" --trust=0 \
  "$tmp/ObligationTree.lean"
```

An earlier same-session replay under `/tmp` omitted Lean's root-directory option and failed only
module-path setup for the four files importing `Statement`; `JacobianBridge.lean` still elaborated.
It carries no proof credit. The relative temporary-directory replay above repaired that invocation
and all five modules passed. Both temporary directories were removed.

## Status Boundary

This is a current-base nonrelease blocker record, not a proof receipt. It does not satisfy
`S56-M-1520-PROOF`, change the task state, or claim audit completion, theorem completion, release,
or master acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
