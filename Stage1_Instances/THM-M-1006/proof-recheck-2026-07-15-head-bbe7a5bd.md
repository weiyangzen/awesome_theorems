# THM-M-1006 current-base proof recheck

Item: `S56-M-1006-PROOF`

Intent: `prove`

Base revision: `bbe7a5bd1c72a12f3f43b79b6a4cac3f62d2085a`

Base tree: `aa558ed6f23779c7d2d9a8427775f709d8b7e31b`

Recheck date: 2026-07-15 (Asia/Shanghai)

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen target because its unrestricted
discrete-jump upper comparison is false at `p = 1 / 2`. The finite rare-jump martingales and their
moment estimates are given in `counterexample-analysis.md`; this recheck binds that blocker and the
already checked partial bodies to the current base. The item remains `[ ]`, lifecycle remains
`planned`, and the authoritative root vector remains `[H2, M3, R3]`. The counterexample supports a
proposed `H5` classification, subject to master review.

For every `N >= 2`, put `q = 1 / N^2`. While active, a process increments by `+1` with probability
`1-q` and by `-(1-q)/q` with probability `q`, then freezes after the rare negative jump. The
conditional increment is centered. At horizon `N`, the process satisfies

```text
E[M_N^(1/2)] >= (1/2) N^(1/2),
E[Q_N^(1/4)] <= N^(1/4) + 2^(1/4).
```

Their ratio is unbounded, contradicting the one finite `C` quantified before the probability space,
martingale, and horizon in `StatementShape (1 / 2)`. This refutes the selected finite discrete-time
encoding, not the classical continuous-martingale BDG theorem. `Counterexample.lean` checks the
exponent, transition algebra, jump parameters, and asymptotic ingredients, but it does not encode the
complete probability spaces, filtration, martingale witness, exact lintegrals, moment bounds, or
`Not (StatementShape (1 / 2))`. This is therefore a mathematical blocker rather than an `M0`
kernel-refutation receipt.

## Checked Partial Bodies

`Proof.lean` contains placeholder-free proofs of finite telescoping, zero-start reconstruction, and
the horizon-zero maximum and quadratic variation. The isolated trust-zero replay below succeeded.
Every printed axiom set was a subset of `propext`, `Classical.choice`, and `Quot.sound`, with no
`sorryAx`. These bodies cover parts of `M1006-N-DIFFERENCES` and `M1006-S-BOUNDARY`; they do not
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

All Lean checks reused the automation-provided canonical `.lake` symlink read only. No `lake
update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was performed.
Temporary sources and compiler output were confined to a fresh worker-local directory and removed
by the command trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | Rank 286; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges passed; denominator `12818dc1...14dac6f`; root open at M3 |
| bounded pinned-mathlib BDG/quadratic-variation search | 0 | No exact declaration; matches were adjacent Doob `maximal_ineq` and an unrelated polynomial comment |
| isolated pinned-Lean trust-zero recipe below | 0 | `Statement.lean`, `Proof.lean`, `Counterexample.lean`, and `ObligationTree.lean` elaborated; axiom union was `propext`, `Classical.choice`, and `Quot.sound` |
| token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match; no prohibited declaration token was found |
| source hashes and current DAG-state inspection | 0 | Base/tree, source hashes, `[ ]` proof state, `[_]` predecessor state, open-root flags, and absent self-test agreed |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion self-test manifest |

The successful isolated recipe, run from the repository root, was:

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
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 240 lake env lean --trust=0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 lake env lean --trust=0 --root="$tmp" \
  "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 lake env lean --trust=0 --root="$tmp" \
  "$tmp/Counterexample.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 lake env lean --trust=0 --root="$tmp" \
  "$tmp/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

The source identity command was:

```bash
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
sha256sum \
  Stage1_Instances/THM-M-1006/{Statement,Proof,Counterexample,ObligationTree}.lean \
  Stage1_Instances/THM-M-1006/counterexample-analysis.md \
  Stage1_Instances/THM-M-1006/{obligation-registry,typed-graphs,validation-specs}.json \
  Formalizations/Lean/lake-manifest.json
```

It returned the base and tree above and the hashes recorded in the companion JSON. Inspection of
`Docs/Stage1_Execution_DAG_rev-5.6.json` returned `[_]` for `S56-M-1006-OBLIGATION_TREE` and `[ ]`
for `S56-M-1006-PROOF`.

The structured companion record binds the current source hashes, base identity, environment pins,
commands, failure boundary, and retry condition. It is durable blocker evidence only.

## Retry Condition

Reopen the statement phase and choose a source-faithful valid formulation: restrict the exponent
range, add sufficient jump control, or formalize the intended continuous-martingale theorem. Then
freeze and accept a new statement fingerprint and append-only obligation-registry delta before
resuming positive proof execution. Alternatively, explicitly redirect the item to a complete
kernel-checked counterexample target.

This is current-base nonrelease blocker evidence, not a proof receipt. It changes no task state,
closes no root obligation, and claims neither audit nor theorem completion. Because the assigned
positive proof phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.
