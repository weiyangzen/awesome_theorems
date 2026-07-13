# THM-M-1006 current-base proof recheck

Item: `S56-M-1006-PROOF`

Intent: `prove`

Base revision: `8f22279fd1216cdfb5676c758e6bdb08e0ba3e01`

Base tree: `d2e9e68da52ecfcfe15a9c48ac2262400e602667`

Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. The exact frozen target cannot receive a positive proof body because its unrestricted
discrete-jump upper comparison is false at `p = 1 / 2`. The tracked family and estimates are given
in `counterexample-analysis.md`; this recheck binds that blocker and the already checked partial
bodies to the current base. The item remains `[ ]`, the lifecycle remains `planned`, and the
authoritative root vector stays `[H2, M3, R3] -> [H2, M3, R3]` pending master reconciliation.

At horizon `N >= 2`, take `q = 1 / N^2`. While active, a process increment is `+1` with probability
`1-q` and `-(1-q)/q` with probability `q`, and the process freezes after the rare negative jump.
The conditional increment is centered, so the resulting finite process is a martingale. At
`p = 1 / 2`, its maximum and quadratic-variation moments satisfy

```text
E[M_N^(1/2)] >= (1/2) N^(1/2),
E[Q_N^(1/4)] <= N^(1/4) + 2^(1/4).
```

Their ratio is unbounded. This contradicts the one finite constant `C`, quantified before the
probability space, martingale, and horizon in `StatementShape (1 / 2)`. It refutes this finite
discrete-time encoding, not the classical continuous-martingale BDG theorem.

`Counterexample.lean` kernel-checks the exponent range, transition-centering algebra, related jump
parameters, and asymptotic ingredients. It does not formalize the complete product probability
spaces, filtration, martingale witness, lintegral evaluations, or
`Not (StatementShape (1 / 2))`. Thus the negative result is an exact human blocker supporting a
proposed `H5`, not a full kernel refutation or an `M0` receipt. The machine root truthfully remains
open at `M3`.

## Checked Partial Bodies

The current `Proof.lean` still supplies genuine placeholder-free bodies for finite telescoping,
zero-start reconstruction, and the horizon-zero maximum and quadratic variation. Their isolated
trust-zero replay succeeded and each printed axiom set was a subset of `propext`,
`Classical.choice`, and `Quot.sound`. They cover parts of `M1006-N-DIFFERENCES` and
`M1006-S-BOUNDARY`; they do not prove `M1006-T-LOWER`, `M1006-T-UPPER`, or the root.

The first failed gate is exact-target mathematical truth at `M1006-B-P-RANGE`. The invalidated
positive path is `M1006-B-P-RANGE -> M1006-T-UPPER -> M1006-T-ASSEMBLE -> M1006-ROOT`.

## Validation

All Lean checks reused the existing automation-provided `.lake` symlink read only. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Source copies and compiled output were confined to a fresh worker-local temporary
directory and removed by the command trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | rank 286; lifecycle planned; legacy artifacts unaccepted; theorem incomplete |
| isolated pinned-Lean trust-zero recipe below | 0 | `Statement.lean`, `Proof.lean`, and `Counterexample.lean` elaborated; all printed axiom sets were subsets of `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges passed; denominator `12818dc1...14dac6f`; root open at M3 |
| token-anchored prohibited-construct scan over owned `*.lean` files | 1 | expected no-match; no prohibited proof device was found |
| current packet/source/DAG identity assertions | 0 | statement, proof, counterexample, analysis, registry, graph, denominator, `[ ]` state, open-root flags, and absent self-test agreed |
| `git diff --check -- Stage1_Instances/THM-M-1006` plus per-new-file `git diff --no-index --check /dev/null <file>` | 0 / 1 each | no whitespace diagnostics; each exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | the incomplete proof phase emitted no completion self-test manifest |

The successful isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
tmp=$(mktemp -d .thm1006-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1006/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1006/Proof.lean "$tmp/Proof.lean"
cp Stage1_Instances/THM-M-1006/Counterexample.lean "$tmp/Counterexample.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 240 "$lean" --trust=0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean" --trust=0 --root="$tmp" \
  "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean" --trust=0 --root="$tmp" \
  "$tmp/Counterexample.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Reopen the statement phase and choose a source-faithful valid formulation: restrict the exponent
range, add sufficient jump control, or select the intended continuous-martingale theorem. Then
freeze and accept a new statement fingerprint and append-only obligation-registry delta before
resuming proof work. Alternatively, explicitly redirect the item to a complete kernel-checked
counterexample target.

This is current-base nonrelease blocker evidence, not a proof receipt. It changes no task state,
closes no root obligation, and claims neither audit nor theorem completion. Because the positive
proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
