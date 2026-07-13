# THM-M-1006 current-base proof recheck

Item: `S56-M-1006-PROOF`

Intent: `prove`

Base revision: `e160de3efab9257518f9bda57545182c2c72e155`

Base tree: `762bcfd6b010e582efebfcac2285095967248cb2`

Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. A positive proof body for the exact frozen target cannot be supplied because its
unrestricted discrete-jump upper comparison is false at `p = 1 / 2`. The counterexample and its
estimates are recorded in `counterexample-analysis.md`; this recheck binds that blocker and the
already checked partial proof bodies to the current base. The item remains `[ ]`, the lifecycle
remains `planned`, and the authoritative root vector remains `[H2, M3, R3]`. The counterexample
supports a proposed `H5` classification, subject to master review.

For each `N >= 2`, set `q = 1 / N^2`. While active, let a process increment be `+1` with
probability `1-q` and `-(1-q)/q` with probability `q`, and freeze it after the rare negative jump.
The conditional increment is centered. At horizon `N`, this finite martingale satisfies

```text
E[M_N^(1/2)] >= (1/2) N^(1/2),
E[Q_N^(1/4)] <= N^(1/4) + 2^(1/4).
```

The ratio is unbounded, contradicting the one finite constant `C` quantified before the
probability space, martingale, and horizon in `StatementShape (1 / 2)`. This refutes the selected
finite discrete-time encoding, not the classical continuous-martingale BDG theorem.

`Counterexample.lean` kernel-checks the exponent range, transition-centering algebra, jump
parameters, and asymptotic ingredients. It does not encode the full product probability spaces,
filtration, martingale witness, exact lintegrals, moment bounds, or
`Not (StatementShape (1 / 2))`. The negative result is therefore a human mathematical blocker,
not a full kernel refutation or an `M0` receipt. Machine status remains `M3`.

## Checked Partial Bodies

`Proof.lean` contains genuine placeholder-free bodies for finite telescoping, zero-start
reconstruction, and the horizon-zero maximum and quadratic variation. The isolated trust-zero
replay below succeeded. Every printed axiom set was a subset of `propext`, `Classical.choice`, and
`Quot.sound`, and no `sorryAx` occurred. These declarations cover parts of
`M1006-N-DIFFERENCES` and `M1006-S-BOUNDARY`; they do not prove `M1006-T-LOWER`,
`M1006-T-UPPER`, or the root.

The first failed gate is exact-target mathematical truth at `M1006-B-P-RANGE`. The invalidated
positive path is
`M1006-B-P-RANGE -> M1006-T-UPPER -> M1006-T-ASSEMBLE -> M1006-ROOT`.

## Validation

All Lean checks reused the automation-provided canonical `.lake` symlink read only. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Temporary source copies and compiled output were confined to a fresh worker-local
directory and removed by the command trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | rank 286; lifecycle planned; legacy artifacts unaccepted; theorem incomplete |
| bounded pinned-mathlib BDG/quadratic-variation search | 0 | no exact BDG or quadratic-variation declaration; only adjacent Doob `maximal_ineq` and one unrelated polynomial comment matched |
| isolated pinned-Lean trust-zero recipe below | 0 | `Statement.lean`, `Proof.lean`, and `Counterexample.lean` elaborated; all printed axiom sets were subsets of `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges passed; denominator `12818dc1...14dac6f`; root open at M3 |
| token-anchored prohibited-device scan over owned `*.lean` files | 1 | expected no-match; no prohibited Lean declaration token was found |
| current packet/source/DAG identity assertions | 0 | base/tree, source hashes, registry denominator, `[ ]` state, open-root flags, and absent self-test agreed |
| `git diff --check -- Stage1_Instances/THM-M-1006` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | the incomplete proof phase emitted no completion self-test manifest |

The successful isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
tmp=$(mktemp -d .thm1006-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1006/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1006/Proof.lean "$tmp/Proof.lean"
cp Stage1_Instances/THM-M-1006/Counterexample.lean "$tmp/Counterexample.lean"
lean_bin=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 240 "$lean_bin" --trust=0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean_bin" --trust=0 --root="$tmp" \
  "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean_bin" --trust=0 --root="$tmp" \
  "$tmp/Counterexample.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Reopen the statement phase and select a source-faithful valid formulation: restrict the exponent
range, add sufficient jump control, or formalize the intended continuous-martingale theorem. Then
freeze and accept a new statement fingerprint and append-only obligation-registry delta before
resuming positive proof execution. Alternatively, explicitly redirect the item to a complete
kernel-checked counterexample target.

This is current-base nonrelease blocker evidence, not a proof receipt. It changes no task state,
closes no root obligation, and claims neither audit nor theorem completion. Because the assigned
positive proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
