# THM-M-1006 current-base proof blocker

Item: `S56-M-1006-PROOF`

Intent: `prove`

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

Recheck date: 2026-07-15 (Asia/Shanghai)

## Verdict

`blocked`. A positive proof body cannot inhabit the exact frozen target because its unrestricted
discrete-jump upper comparison is false at `p = 1 / 2`. The item remains `[ ]`, the lifecycle
remains `planned`, and the accepted root vector remains `[H2, M3, R3]`. This packet proposes `H5`
for master review but does not change the authoritative classification.

For each `N >= 2`, let `q = 1 / N^2`. While active, a finite process increments by `+1` with
probability `1-q` and by `-(1-q)/q` with probability `q`, then freezes after the rare negative
jump. Its conditional increment is centered. At horizon `N`, the construction in
`counterexample-analysis.md` gives

```text
E[M_N^(1/2)] >= (1/2) N^(1/2),
E[Q_N^(1/4)] <= N^(1/4) + 2^(1/4).
```

The ratio is unbounded. This contradicts the one finite upper constant quantified before the
probability space, martingale, and horizon in `StatementShape (1 / 2)`. It refutes the selected
finite discrete-time encoding, not the classical continuous-martingale BDG theorem.

`Counterexample.lean` checks transition algebra and asymptotic ingredients, but it does not encode
the complete probability spaces, filtration, martingale witness, exact lintegrals, moment bounds,
or `Not (StatementShape (1 / 2))`. The evidence therefore remains a mathematical blocker rather
than an M0 kernel refutation.

The first failed gate is exact-target mathematical truth at `M1006-B-P-RANGE`. The invalidated
positive path is
`M1006-B-P-RANGE -> M1006-T-UPPER -> M1006-T-ASSEMBLE -> M1006-ROOT`.
Independently, the required predecessor `S56-M-1006-OBLIGATION_TREE` is only provisional `[_]`, not
master-accepted `[x]`.

## Existing Partial Bodies

`Proof.lean` has placeholder-free proofs of finite telescoping, zero-start reconstruction, and the
horizon-zero maximum and quadratic variation. The fresh trust-zero replay below elaborated those
five declarations. `ObligationTree.lean` also elaborated its conditional composition theorem, but
that theorem requires both directional BDG packages as premises and supplies no root proof credit.

All 14 printed axiom reports from `Proof.lean`, `Counterexample.lean`, and
`ObligationTree.lean` were subsets of `propext`, `Classical.choice`, and `Quot.sound`, with no
`sorryAx`. No proof body was added in this recheck because the requested exact proposition is
false; adding a weaker, conditional, or changed theorem would violate the frozen target.

## Validation

All dependency inspection was read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation was performed. The pre-existing automation `.lake` symlink is
untracked, so this is nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | Rank 286; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges passed; denominator `12818dc1...14dac6f`; root open at M3. |
| `cd Formalizations/Lean && lake env lean --version` | 1 | The pinned `flt-regular` repository could not resolve `HEAD`; Lake did not invoke Lean. |
| Direct pinned Lean identity check | 0 | Lean 4.29.0, commit `98dc76e...fab16740`; binary SHA-256 `3e0d0d3d...bae28bbf`. |
| Isolated direct pinned-Lean `--trust=0 -t0` replay below | 0 | `Statement.lean`, `Proof.lean`, `Counterexample.lean`, and `ObligationTree.lean` elaborated; 14 axiom reports had only the permitted classical kernel axioms and no `sorryAx`. |
| Bounded pinned-mathlib BDG search | 0 | No exact BDG declaration; only adjacent Doob `maximal_ineq` and an unrelated polynomial comment matched. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match; no prohibited declaration token was found. |
| Current DAG and source identity assertions | 0 | Base/tree, hashes, proof `[ ]`, predecessor `[_]`, open-root fields, and absent self-test agreed. |
| JSON syntax validation | 0 | The companion packet parsed successfully. |
| Scoped whitespace checks | 0 / 1 each | The tracked check exited 0; each no-index check exited 1 only for the expected new-file difference and emitted no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion self-test manifest. |

The required Lake entry point failed exactly with:

```text
error: .../Formalizations/Lean/.lake/packages/flt-regular: could not resolve 'HEAD' to a commit; the repository may be corrupt, so you may need to remove it and try again
```

The existing pinned Lean binary and compiled dependency closure allowed this narrower nonrelease
replay from the repository root:

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

## Retry Condition

Reopen the statement phase and choose a source-faithful valid formulation: restrict the exponent
range, add sufficient jump control, or formalize the intended continuous-martingale theorem. Then
freeze and accept a new statement fingerprint and append-only obligation-registry delta before
resuming positive proof execution. Alternatively, explicitly redirect the item to a fully
kernel-checked counterexample target. The already pinned `flt-regular` artifact must also be restored
at its manifest revision before canonical `lake env lean` validation, without fetching or changing
the pin.

This is current-base nonrelease blocker evidence, not a proof receipt. It changes no task state,
closes no root obligation, and claims neither audit nor theorem completion. Because the assigned
positive proof phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.
