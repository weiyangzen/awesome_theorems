# THM-M-1006 current-base proof blocker

Item: `S56-M-1006-PROOF`

Intent: `prove`

Base revision: `ab6974ae3bcabe677e7138ff057a7c005aac12d4`

Base tree: `c640af240d44f02c83a29dfa2f985f601a0dfcc2`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen target. The unrestricted
discrete-jump upper comparison in `StatementShape` is false at `p = 1 / 2`. The proof item remains
`[ ]`, the lifecycle remains `planned`, and the authoritative root remains open at
`[H2, M3, R3]`. The counterexample supports a proposed `H5` classification, but only the master may
review and accept that change.

For every integer `N >= 2`, put `q = 1 / N^2`. Starting from zero, while active let a process
increment by `+1` with probability `1 - q` and by `-(1 - q) / q` with probability `q`, then freeze
after the rare negative jump. The increment is conditionally centered. At horizon `N`, the finite
martingales described in `counterexample-analysis.md` satisfy

```text
E[M_N^(1/2)] >= (1/2) * N^(1/2),
E[Q_N^(1/4)] <= N^(1/4) + 2^(1/4).
```

Their ratio is unbounded, contradicting the one finite upper constant quantified before the
probability space, martingale, and horizon in `StatementShape (1 / 2)`. This refutes the selected
finite discrete-time encoding, not the classical continuous-martingale BDG theorem.

`Counterexample.lean` kernel-checks supporting transition algebra and asymptotics. It does not
encode the complete finite probability spaces, filtration, martingale witness, exact lintegrals,
moment estimates, or `Not (StatementShape (1 / 2))`; it is mathematical blocker evidence rather
than an M0 kernel refutation. The first failed gate is exact-target mathematical truth at
`M1006-B-P-RANGE`. The invalidated positive path is
`M1006-B-P-RANGE -> M1006-T-UPPER -> M1006-T-ASSEMBLE -> M1006-ROOT`.

The prerequisite `S56-M-1006-OBLIGATION_TREE` is also only worker-provisional `[_]`, not
master-accepted `[x]`.

## Existing partial bodies

`Proof.lean` contains placeholder-free proofs of finite telescoping, zero-start reconstruction, and
the horizon-zero maximal-process and quadratic-variation identities. `ObligationTree.lean` contains
a checked composition theorem, but it assumes both missing directional BDG packages and gives no
root proof credit. No proof body was added in this recheck because any positive root body would have
to prove a false target, weaken or change it, or make the missing directions premises.

The trust-zero diagnostic replay elaborated `Statement.lean`, `Proof.lean`, `Counterexample.lean`,
and `ObligationTree.lean`. All 14 printed axiom reports were subsets of `propext`,
`Classical.choice`, and `Quot.sound`, with no `sorryAx`. The owned Lean source scan found no
`sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle construct, or `native_decide`.

## Validation

All dependency inspection and replay were read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout, repair, or `.lake` mutation was performed. The automation-provided `.lake`
symlink is untracked, so this is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | Rank 286; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` | 0 | Before this packet, the sole entry was the pre-existing untracked `Formalizations/Lean/.lake` symlink. |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges passed; denominator `12818dc1...14dac6f`; root open M3. |
| `cd Formalizations/Lean && timeout --foreground 300 lake env lean --version` | 1 | Lake stopped before Lean with `error: external command 'git' exited with code 128`; the pinned `flt-regular` directory has no resolvable `HEAD`, although its manifest commit is present. |
| `cd Formalizations/Lean/.lake/packages/mathlib && timeout --foreground 180 lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e...fab16740`, Release. |
| Isolated four-module pinned-Lean `--trust=0 -t0` replay below | 0 | All four target modules elaborated; all 14 axiom reports contained only the permitted classical kernel axioms and no `sorryAx`. |
| Mathlib-local `lake env lean` four-module replay using its emitted `LEAN_PATH` | 1 | The Lake subprocess reached Lean but its nested package path points to absent `mathlib/.lake/packages/*` directories; `Statement.lean` stopped at `unknown module prefix 'Batteries'`. |
| Bounded pinned-mathlib BDG search | 0 | No exact BDG declaration was found; only adjacent Doob maximal-inequality material and an unrelated polynomial comment matched. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no prohibited declaration token was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-1006/proof-recheck-2026-07-15-head-ab6974ae-slot30.json` | 0 | The companion blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1006` plus per-new-file no-index checks | 0 | No whitespace diagnostics; no-index exit 1 for each new file means only that the file differs from `/dev/null`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion self-test manifest. |

The successful diagnostic replay used the exact pinned executable and only already materialized
package outputs:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm1006-slot30-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1006/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1006/Proof.lean "$tmp/Proof.lean"
cp Stage1_Instances/THM-M-1006/Counterexample.lean "$tmp/Counterexample.lean"
cp Stage1_Instances/THM-M-1006/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
lean_root=$root/Formalizations/Lean
lean_path=$(find "$lean_root/.lake/packages" -path '*/.lake/build/lib/lean' -type d \
  -print | LC_ALL=C sort | paste -sd:)
lean_path="$lean_path:$lean_root/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
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

## Retry condition

Reopen the statement phase and select a source-faithful valid formulation: restrict the exponent
range, add sufficient jump control, or formalize the intended continuous-martingale theorem. Then
freeze and accept a new statement fingerprint and append-only obligation-registry delta before
rerunning anchor audit, obligation-tree construction, and positive proof execution. Alternatively,
explicitly redirect the item to a fully kernel-checked counterexample target. The pinned
`flt-regular` artifact must also have a resolvable `HEAD` at its manifest revision before canonical
`lake env lean` validation, without fetching or changing the dependency pin.

This is current-base nonrelease blocker evidence, not a proof receipt. It changes no scheduler
state, closes no root obligation, and claims neither audit completion, theorem completion,
validation, release, nor master acceptance. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
