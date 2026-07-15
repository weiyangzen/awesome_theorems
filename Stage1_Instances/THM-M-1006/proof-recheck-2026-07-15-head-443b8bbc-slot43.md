# THM-M-1006 current-base proof recheck

Item: `S56-M-1006-PROOF`

Intent: `prove`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

Recheck date: 2026-07-15 (Asia/Shanghai)

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen target because its unrestricted
discrete-jump upper comparison is false at `p = 1 / 2`. This recheck binds the existing
counterexample and partial proof bodies to the current base. The item remains `[ ]`, lifecycle
remains `planned`, and the authoritative root vector remains `[H2, M3, R3]`. The counterexample
supports an `H5` target classification, subject to master review.

For every `N >= 2`, put `q = 1 / N^2`, `s = 1 - q`, and `a = s / q = N^2 - 1`. While active, a
process increments by `+1` with probability `s` and by `-a` with probability `q`, then freezes after
the rare negative jump. The conditional increment is centered because `s - q * a = 0`. At horizon
`N`, the finite martingale satisfies

```text
E[M_N^(1/2)] >= (1/2) N^(1/2),
E[Q_N^(1/4)] <= N^(1/4) + 2^(1/4).
```

Indeed, the no-jump event has probability `s^N >= 1 - Nq >= 1/2` and gives `M_N = Q_N = N`. On a
rare-jump path, `Q_N <= N + N^4 <= 2 N^4`, while the total rare-jump probability is at most
`Nq = 1/N`. The displayed ratio is unbounded, contradicting the single finite `C` quantified before
the probability space, martingale, and horizon in `StatementShape (1 / 2)`. This refutes the
selected finite discrete-time encoding, not the classical continuous-martingale BDG theorem.

`Counterexample.lean` checks supporting transition algebra and asymptotic facts, but it does not
encode the complete probability spaces, filtration, martingale witness, exact lintegrals, moment
bounds, or `Not (StatementShape (1 / 2))`. This remains mathematical blocker evidence rather than
an `M0` kernel-refutation receipt. A source-faithful repair should restrict arbitrary discrete
martingales to at least `p >= 1`, add sufficient hypotheses below one, or select the intended
continuous-martingale formulation.

## Checked Partial Bodies

`Proof.lean` contains placeholder-free proofs of finite telescoping, zero-start reconstruction, and
the horizon-zero maximum and quadratic variation. A fresh direct pinned-Lean trust-zero replay
succeeded. All 14 printed axiom reports from `Proof.lean`, `Counterexample.lean`, and
`ObligationTree.lean` were subsets of `propext`, `Classical.choice`, and `Quot.sound`, with no
`sorryAx`. The proof bodies cover parts of `M1006-N-DIFFERENCES` and `M1006-S-BOUNDARY`; they do not
prove `M1006-T-LOWER`, `M1006-T-UPPER`, or `M1006-ROOT`.

`ObligationTree.lean` also rechecked its conditional composition declaration. That declaration
requires both directional BDG packages as premises and therefore receives no directional or root
proof credit.

The first failed gate is exact-target mathematical truth at `M1006-B-P-RANGE`. The invalidated
positive path is
`M1006-B-P-RANGE -> M1006-T-UPPER -> M1006-T-ASSEMBLE -> M1006-ROOT`.
The predecessor `S56-M-1006-OBLIGATION_TREE` is only provisional `[_]`, not master-accepted; this
independently prevents dependency-legal proof-node acceptance.

## Validation

No dependency update, build, clone, fetch, network operation, or `.lake` mutation was performed.
The automation-provided `.lake` symlink was reused read only. Its pinned `flt-regular` checkout
contains the requested commit object but has an invalid `HEAD` and no checked-out worktree, so the
required `lake env lean` entry point now fails before invoking Lean. This missing canonical artifact
is recorded as a validation blocker rather than repaired or fetched. The same pinned Lean binary and
existing compiled mathlib closure still allowed a narrow direct elaboration replay; this is
nonrelease evidence and does not replace the required Lake validation gate.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | rank 286; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges passed; denominator `12818dc1...14dac6f`; root open at M3 |
| `cd Formalizations/Lean && lake env lean --version` | 1 | pinned `flt-regular` cannot resolve `HEAD`; canonical Lake validation unavailable |
| direct pinned Lean identity check | 0 | Lean `4.29.0`, commit `98dc76e...fab16740`; binary SHA-256 `3e0d0d3d...bae28bbf` |
| direct four-module pinned-Lean `--trust=0 -t0` replay below | 0 | all four modules elaborated; 14 axiom reports were subsets of `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` |
| bounded pinned-mathlib BDG search | 0 | no exact declaration; only adjacent Doob `maximal_ineq` and an unrelated polynomial comment matched |
| token-anchored prohibited-device scan over owned `*.lean` files | 1 | expected no-match; no prohibited Lean declaration token was found |
| `test ! -e .stage1-worker-selftest.json` | 0 | the incomplete proof phase emitted no completion self-test manifest |

The successful direct replay, run from the repository root, was:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm1006-slot43-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1006/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1006/Proof.lean "$tmp/Proof.lean"
cp Stage1_Instances/THM-M-1006/Counterexample.lean "$tmp/Counterexample.lean"
cp Stage1_Instances/THM-M-1006/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
lean_root=$root/Formalizations/Lean
lean_path=$lean_root/.lake/build/lib/lean
while IFS= read -r package_lib; do
  lean_path="$lean_path:$package_lib"
done < <(find "$lean_root/.lake/packages" -path '*/.lake/build/lib/lean' -type d | sort)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 --root="$tmp" "$tmp/Counterexample.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 --root="$tmp" "$tmp/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

The companion JSON record binds the source hashes, base identity, environment, commands, failure
boundary, and retry conditions. It is durable blocker evidence only.

## Retry Condition

Reopen the statement phase and choose a source-faithful valid formulation. Then freeze and accept a
new statement fingerprint and append-only obligation-registry delta before resuming positive proof
execution. Alternatively, explicitly redirect the item to a complete kernel-checked counterexample
target. Independently, restore the already pinned `flt-regular` artifact at its manifest revision so
that `lake env lean` works without fetching or changing dependency pins.

This is current-base nonrelease blocker evidence, not a proof receipt. It changes no task state,
closes no root obligation, and claims neither audit nor theorem completion. Because the assigned
positive proof phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.
