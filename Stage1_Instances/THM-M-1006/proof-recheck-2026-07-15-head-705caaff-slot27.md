# THM-M-1006 current-base proof blocker

Item: `S56-M-1006-PROOF`

Intent: `prove`

Base revision: `705caafffbcdaf43757a4468b018716da692307d`

Base tree: `ee88e7872fd1a00bc7c906f6deeb99ecdf7e1a64`

Worker: `slot27`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen target because its unrestricted
discrete-jump upper comparison is false at `p = 1 / 2`. The item remains `[ ]`, lifecycle remains
`planned`, and the authoritative root vector remains `[H2, M3, R3]`. This packet proposes `H5` for
master review but changes no authoritative classification or task state.

For every `N >= 2`, put `q = 1 / N^2`. While active, a process increments by `+1` with probability
`1-q` and by `-(1-q)/q` with probability `q`, then freezes after the rare negative jump. The
conditional increment is centered. At horizon `N`, the finite martingales constructed in
`counterexample-analysis.md` satisfy

```text
E[M_N^(1/2)] >= (1/2) * N^(1/2),
E[Q_N^(1/4)] <= N^(1/4) + 2^(1/4).
```

Their ratio is unbounded. This contradicts the single finite upper constant quantified before the
probability space, martingale, and horizon by `StatementShape (1 / 2)`. It refutes this selected
finite discrete-time encoding, not the classical continuous-martingale BDG theorem.

`Counterexample.lean` kernel-checks supporting transition algebra and asymptotics, but it does not
encode the complete finite probability spaces, filtration, martingale witness, exact lintegrals,
moment estimates, or `Not (StatementShape (1 / 2))`. It therefore supplies mathematical blocker
evidence, not an M0 kernel refutation. The first failed gate is exact-target mathematical truth at
`M1006-B-P-RANGE`; the invalidated positive path is
`M1006-B-P-RANGE -> M1006-T-UPPER -> M1006-T-ASSEMBLE -> M1006-ROOT`.

The prerequisite `S56-M-1006-OBLIGATION_TREE` is also only worker-provisional `[_]`, not
master-accepted `[x]`.

## Existing Partial Bodies

`Proof.lean` has placeholder-free proofs of finite telescoping, zero-start reconstruction, and the
horizon-zero maximal-process and quadratic-variation identities. `ObligationTree.lean` has a
checked composition theorem, but it assumes both directional BDG packages and supplies no root
proof credit. No proof body was added in this recheck because doing so would require a false,
weakened, conditional, or changed target.

The isolated trust-zero replay elaborated `Statement.lean`, `Proof.lean`, `Counterexample.lean`, and
`ObligationTree.lean`. All 14 printed axiom reports were subsets of `propext`, `Classical.choice`,
and `Quot.sound`, with no `sorryAx`. The owned Lean source scan found no prohibited placeholder,
bodyless declaration, unsafe/oracle construct, `native_decide`, or `run_tac`.

## Validation

All dependency inspection and replay were read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout, repair, network operation, or `.lake` mutation was performed. The
automation-provided `.lake` symlink is untracked, so this is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | Rank 286; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` | 0 | Before this packet, the sole entry was the pre-existing untracked `Formalizations/Lean/.lake` symlink. |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges passed; denominator `12818dc1...14dac6f`; root open M3 and directional packages M4. |
| pinned Lean/mathlib identity and SHA-256 checks | 0 | Lean `4.29.0` at `98dc76e...fab16740`; mathlib `8a178386...eea95`; binary `3e0d0d3d...bae28bbf`; manifest `321626c8...cb2d81`. |
| bounded pinned-mathlib BDG search | 0 | No exact BDG or quadratic-variation declaration was found; matches were adjacent Doob `maximal_ineq` and an unrelated polynomial square-function comment. |
| isolated four-module `lake env lean --trust=0 -t0` replay below | 0 | All four target modules elaborated; 14 axiom reports contained only the permitted classical kernel axioms and no `sorryAx`. |
| token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no prohibited declaration token was found. |
| current packet/source/DAG identity assertions | 0 | Base/tree, source hashes, `[ ]` proof state, `[_]` predecessor, open-root flags, and absent self-test agreed. |
| `python3 -m json.tool` on the matching JSON packet | 0 | The current-base blocker packet parsed successfully. |
| scoped tracked diff and no-index whitespace checks | 0 / 1 each | No whitespace diagnostics; each no-index exit 1 denotes only the expected new-file difference. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion self-test manifest. |

The successful isolated Lean replay, run from the repository root, was:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d "$root/.thm1006-proof-recheck.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1006/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1006/Proof.lean "$tmp/Proof.lean"
cp Stage1_Instances/THM-M-1006/Counterexample.lean "$tmp/Counterexample.lean"
cp Stage1_Instances/THM-M-1006/ObligationTree.lean "$tmp/ObligationTree.lean"
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Formalizations/Lean
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" "$tmp/Counterexample.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" "$tmp/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Reopen the statement phase and select a source-faithful valid formulation: restrict the exponent
range, add sufficient jump control, or formalize the intended continuous-martingale theorem. Then
freeze and accept a new statement fingerprint and append-only obligation-registry delta before
resuming positive proof execution. Alternatively, explicitly redirect this item to a fully
kernel-checked counterexample target.

This is current-base nonrelease blocker evidence, not a proof receipt. It changes no scheduler
state, closes no root obligation, and claims neither audit completion, theorem completion,
validation, release, nor master acceptance. Because the assigned positive proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.
