# THM-M-1140 proof-phase recheck

Item: `S56-M-1140-PROOF`  
Intent: `prove`  
Base revision: `f3a2545c7e6634696c48f725a9581e7e248c8877`  
Base tree: `a9ade4224e40322a81336ccd63462829ffedc8eb`  
Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. The exact assigned proof phase remains open. No placeholder-free proof body or eligible
pinned import was found for `InteriorLocalRigidity`, so the root remains `[H2, M3, R3]` and the
item remains `[ ]`. This recheck makes no audit, theorem-completion, receipt-acceptance, or master-
acceptance claim.

The exact root is
`Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple`: for every `n : Nat`, a real-valued
`HarmonicOnNhd` function on a nonempty connected open subset of
`EuclideanSpace Real (Fin n)` that attains a maximum at an interior point is constant on the
domain. In particular, narrowing the theorem to the complex plane or to dimensions one or two is
not an admissible proof.

`Proof.lean` already contains a genuine proof of `ConnectedLevelPropagation`. It proves that the
maximum level set is nonempty, closed by continuity, and open from the supplied local neighborhoods,
then uses connectedness of the domain subtype. `ObligationTree.lean` checks that this package and
`InteriorLocalRigidity` compose into the exact root. These checked declarations consume
`InteriorLocalRigidity` as a premise; they do not construct it and therefore do not close the root.

## Failed Gate

The first missing cut is `M1140-L-MEAN-VALUE / M1140-T-LOCAL-PACKAGE`: arbitrary-dimensional
harmonic local rigidity. The pinned general harmonic API provides the Laplacian definition,
`C^2` regularity, continuity, openness of harmonicity, and algebraic closure. It contains no
arbitrary-dimensional mean-value, harmonic-to-real-analytic, unique-continuation, local-rigidity,
or strong-maximum theorem.

The nearby analytic routes do not repair the gap:

- `HarmonicOnNhd.circleAverage_eq` has domain `Complex -> Real` and cannot discharge the target's
  universal Euclidean-dimension binder.
- `HarmonicAt.analyticAt` is likewise specialized to the complex plane; its source explicitly
  retains a TODO for arbitrary finite-dimensional inner-product spaces.
- `AnalyticOnNhd.eqOn_of_preconnected_of_eventuallyEq` is general, but harmonicity cannot be
  converted to its analytic premise in the pinned arbitrary-dimensional API.
- A Hessian argument obtains, at most, pointwise second-derivative information at a maximizer.
  Zero Hessian does not imply local constancy, so this route still requires the unavailable PDE
  propagation or analyticity theorem.

Repo-local search found only the adjacent weak-maximum dossier, which records the same missing
general analytic bridge, and no inhabitant of `InteriorLocalRigidity` or the exact root. The frozen
immutable external audit remains negative. No dependency was fetched, added, updated, or built.

## Validation

All checks reused the automation-provided canonical pinned `.lake` artifacts read-only. Lean source
copies and oleans were confined to a fresh `/tmp` directory and removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | Rank 345; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| isolated trust-zero `lake env lean` recipe below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated; both proof declarations reported exactly `[propext, Classical.choice, Quot.sound]`. |
| `python3 Stage1_Instances/THM-M-1140/check_obligation_tree.py` | 0 | 16 obligations and 36 typed edges passed; denominator `355cbcf...0bee`; the frozen graph reports the root open at `M3` and still predates the local propagation proof. |
| scoped prohibited-construct scan of the three Lean modules | 1 | No match for a `sorry`, `admit`, `axiom`, `unsafe`, or `sorryAx` declaration; exit 1 is ripgrep's expected no-match result. |
| scoped repo and pinned-mathlib searches for harmonic maximum/local-rigidity/analytic bridges | 0/1 | No exact general proof body; only complex-plane mean-value and analyticity results plus the general analytic identity principle. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1140
tmp=$(mktemp -d /tmp/thm-m-1140-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean" --trust=0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" "$lean" --trust=0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" "$lean" --trust=0 Proof.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Resume positive proof work only after a placeholder-free implementation of arbitrary-dimensional
harmonic local rigidity, or discovery of an immutable compatible Lean 4 terminal theorem that can
be pinned, exact-type transported, provenance-audited, and kernel-checked without changing the
frozen target. Assuming that package, specializing the dimension, or returning the conditional
composition would violate the proof-body and exact-target gates.

This is fresh owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1140-PROOF`. Because the assigned phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
