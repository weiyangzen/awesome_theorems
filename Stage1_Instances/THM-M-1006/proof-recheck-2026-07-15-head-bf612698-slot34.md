# THM-M-1006 current-base proof blocker

Item: `S56-M-1006-PROOF`

Intent: `prove`

Base revision: `bf6126986da025eabca097776ede0ba9484bbf71`

Base tree: `98c8e9b005d8d255ee3e05a1c34a449daf02a5a5`

Worker: `slot34`

Recheck time: `2026-07-15T17:11:28+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. A sound positive proof cannot inhabit the exact frozen target because its unrestricted
discrete-jump upper comparison is false at `p = 1 / 2`. The proof item remains `[ ]`, lifecycle
remains `planned`, and the authoritative root vector remains `[H2, M3, R3]`. This packet proposes
`H5` for master review but changes no authoritative classification or task state.

For every integer `N >= 2`, set `q = 1 / N^2`. While active, a process increments by `+1` with
probability `1-q` and by `-(1-q)/q` with probability `q`, then freezes after the rare negative jump.
Each conditional increment is centered. At horizon `N`, the finite martingales constructed in
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
moment estimates, or `Not (StatementShape (1 / 2))`. It is mathematical blocker evidence, not an
`M0` kernel refutation. The first failed gate is exact-target mathematical truth at
`M1006-B-P-RANGE`; the invalidated positive path is
`M1006-B-P-RANGE -> M1006-T-UPPER -> M1006-T-ASSEMBLE -> M1006-ROOT`.

The prerequisite `S56-M-1006-OBLIGATION_TREE` is also only worker-provisional `[_]`, not
master-accepted `[x]`, so proof-node acceptance would independently be dependency-illegal.

## Existing Partial Bodies

`Proof.lean` has placeholder-free proofs of finite telescoping, zero-start reconstruction, and the
horizon-zero maximal-process and quadratic-variation identities. `ObligationTree.lean` has a
checked composition theorem, but it assumes both directional BDG packages and supplies no root
proof credit. No positive proof body was added in this recheck because doing so would require a
false, weakened, conditional, or changed target.

The isolated trust-zero replay elaborated `Statement.lean`, `Proof.lean`, `Counterexample.lean`, and
`ObligationTree.lean`. All 14 printed axiom reports were subsets of `propext`,
`Classical.choice`, and `Quot.sound`, with no `sorryAx`. The owned Lean source scan found no
prohibited placeholder, bodyless declaration, unsafe/oracle construct, or `native_decide`.

## Validation

All dependency inspection and replay were read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout, network operation, or `.lake` mutation was performed. The automation-provided
`.lake` symlink is untracked, so this is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | Rank 286; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` | 0 | Before this packet, the sole entry was the pre-existing untracked `Formalizations/Lean/.lake` symlink. |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges passed; denominator `12818dc1...14dac6f`; root open M3; directional packages M4. |
| `cd Formalizations/Lean && timeout --foreground 60 lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e...fab16740`, Release. |
| bounded pinned-mathlib BDG search | 1 | Expected no-match; no exact BDG or quadratic-variation declaration was found in pinned `Mathlib/Probability` or `Mathlib/MeasureTheory`. |
| isolated four-module `lake env lean --trust=0 -t0` replay below | 0 | All four target modules elaborated; the 14 axiom reports contained only the permitted classical kernel axioms and no `sorryAx`. |
| token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no prohibited declaration token was found. |
| source hashes and current DAG-state inspection | 0 | Base/tree, source hashes, `[ ]` proof state, `[_]` predecessor state, blocker boundary, and incomplete-proof flags agreed. |
| `python3 -m json.tool` on the blocker packet | 0 | The structured blocker artifact parsed successfully. |
| current-base packet identity and fail-closed assertions | 0 | Base/tree, source and authority hashes, DAG states, blocker flags, and absent completion self-test agreed. |
| scoped tracked/no-index whitespace checks | 0 | No whitespace diagnostics; both no-index exits were only the expected new-file difference. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion self-test manifest. |

The successful isolated replay, run from the repository root, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm1006-slot34-replay.XXXXXX)
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
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; Lean binary SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`;
`lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Reopen the statement phase and choose a source-faithful valid formulation: restrict the exponent
range, add sufficient jump control, or formalize the intended continuous-martingale theorem. Then
freeze and accept a new statement fingerprint and append-only obligation-registry delta before
rerunning anchor audit, obligation-tree construction, and positive proof execution. Alternatively,
explicitly redirect this item to a complete kernel-checked counterexample target.

This is current-base nonrelease blocker evidence, not a proof receipt. It changes no scheduler
state, closes no root obligation, and claims neither audit completion, theorem completion,
validation, release, nor master acceptance. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
