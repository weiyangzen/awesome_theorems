# THM-M-1006 current-base proof blocker

Item: `S56-M-1006-PROOF`

Intent: `prove`

Base revision: `cc8afe076b125cde06f870d92e10040c76924568`

Base tree: `1f8c1b01a1ec6c271c5ad7f4dbd9538d81ff58a5`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen target: the unrestricted
discrete-jump upper comparison in `StatementShape` is false at `p = 1 / 2`. The proof item remains
`[ ]`, the lifecycle remains `planned`, and the root remains open at `[H2, M3, R3]`. This packet
proposes `H5` for master review but changes no authoritative classification or task state.

For each integer `N >= 2`, put `q = 1 / N^2`. Starting from zero, while active let the process
increment by `+1` with probability `1 - q` and by `-(1 - q) / q` with probability `q`, then freeze
after the rare negative jump. The conditional increment is centered. At horizon `N`, the finite
martingales constructed in `counterexample-analysis.md` satisfy

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

## Existing partial bodies

`Proof.lean` has placeholder-free proofs of finite telescoping, zero-start reconstruction, and the
horizon-zero maximal-process and quadratic-variation identities. `ObligationTree.lean` has a
checked composition theorem, but it assumes both directional BDG packages and supplies no root
proof credit. No proof body was added in this recheck because doing so would require a false,
weakened, conditional, or changed target.

The direct trust-zero diagnostic replay elaborated `Statement.lean`, `Proof.lean`,
`Counterexample.lean`, and `ObligationTree.lean`. All 14 printed axiom reports were subsets of
`propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`. The owned Lean source scan found
no `sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle construct, or `native_decide`.

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
| `cd Formalizations/Lean && timeout --foreground 120 lake env lean --version` | 1 | Lake stopped before Lean because the pinned `flt-regular` directory could not resolve `HEAD`. |
| Direct pinned Lean `--trust=0 -t0` replay below | 0 | All four target modules elaborated; 14 axiom reports contained only the permitted classical kernel axioms and no `sorryAx`. |
| Bounded pinned-mathlib BDG search | 0 | No exact BDG declaration was found; only adjacent Doob maximal-inequality material and an unrelated polynomial comment matched. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no prohibited declaration token was found. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion self-test manifest. |

The required Lake entry point failed exactly with:

```text
error: .../Formalizations/Lean/.lake/packages/flt-regular: could not resolve 'HEAD' to a commit; the repository may be corrupt, so you may need to remove it and try again
```

The narrower diagnostic replay used the pinned executable and only already materialized package
outputs:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d "$root/.thm1006-proof-recheck.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1006/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1006/Proof.lean "$tmp/Proof.lean"
cp Stage1_Instances/THM-M-1006/Counterexample.lean "$tmp/Counterexample.lean"
cp Stage1_Instances/THM-M-1006/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$(cd Formalizations/Lean && elan which lean)
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

## Retry condition

Reopen the statement phase and select a source-faithful valid formulation: restrict the exponent
range, add sufficient jump control, or formalize the intended continuous-martingale theorem. Then
freeze and accept a new statement fingerprint and append-only obligation-registry delta before
resuming positive proof execution. Alternatively, explicitly redirect this item to a fully
kernel-checked counterexample target. The existing pinned `flt-regular` artifact must also be made
resolvable at its manifest revision before canonical `lake env lean` validation, without fetching
or changing the dependency pin.

This is current-base nonrelease blocker evidence, not a proof receipt. It changes no scheduler
state, closes no root obligation, and claims neither audit completion, theorem completion,
validation, release, nor master acceptance. Because the assigned positive proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.
