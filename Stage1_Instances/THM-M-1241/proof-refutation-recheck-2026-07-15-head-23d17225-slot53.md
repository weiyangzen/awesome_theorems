# THM-M-1241 proof-phase refutation recheck at current base

Item: `S56-M-1241-PROOF`

Recorded at: `2026-07-15T16:37:02+08:00` (`Asia/Shanghai`)

Base revision: `23d1722530f7b3b136c8b91db99531a51b16fad8`

Base tree: `a7e9dea5be1dcc0304a7385d19d35795a47e04dd`

## Verdict

`blocked`. A positive proof body cannot be implemented for the exact frozen proposition because the
tracked, placeholder-free theorem
`Stage1Instances.THM_M_1241.not_gagliardoNirenbergTarget` proves its negation.

The checked counterexample specializes the target to `n = m = r = 1`, `j = 0`,
`q = p = infinity`, `a = 1`, and the constant function `u = 1`. The critical restriction is
vacuous because it assumes `1 < r`. The zero-order exceptional hypothesis is also vacuous because
its antecedent includes `r.toReal * m < n`, which reduces to `1 < 1`. The asserted estimate then
has left side `1` and right side `C * 0 ^ 1 * 1 ^ 0 = 0` for every `C : NNReal`.

This refutes only the frozen formal encoding. It indicates a missing explicit or implicit endpoint
side condition; it does not refute a suitably corrected classical Gagliardo-Nirenberg theorem.
Changing the proposition in this proof node would be an unauthorized theorem substitution and
would invalidate the statement fingerprint, obligation registry, typed graphs, and downstream
evidence.

The first failed gate is `M1241-T-ENDPOINT`, whose admitted `r = 1` case entails the false
fixed-parameter conclusion above. The registry-v1 root cut remains `M1241-T-FINITE` and
`M1241-T-ENDPOINT`. `Proof.lean` establishes only an unregistered `p = 0` fragment, while
`root_of_finite_and_endpoint_packages` consumes rather than constructs both terminal packages.
No positive proof body, proof receipt, state change, or completion claim is made. Because the
assigned phase is incomplete, `.stage1-worker-selftest.json` is intentionally absent.

## Narrow validation

All commands ran in this worker clone. The automation-provided `Formalizations/Lean/.lake` symlink
was reused read-only, and Lean outputs were isolated below `/tmp` and removed. No `lake update`,
`lake build`, dependency clone/fetch, network discovery, checkout repair, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_statement.py` | 0 | Exact expression fingerprint `bf613985e300aa3a5b5e8299a1e0e0e059369387e17c7f0d2c92dc8d8190eb82`; all four structural mutations killed; pinned toolchain and mathlib identity confirmed. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828bd656ec7e4545903a4fdd42a5c759de71b31e46f8c4c189be864991e`; root remains M3 and both terminal packages remain M4. |
| isolated trust-zero four-module recipe below | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Counterexample.lean` elaborated. The composer, partial proofs, and refutation report only `propext`, `Classical.choice`, and `Quot.sound`; every printed proof/refutation declaration reports sorry-free. |
| prohibited-device scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `extern`, `implemented_by`, or `native_decide` token. |
| `git -C Formalizations/Lean/.lake/packages/mathlib diff --quiet` | 0 | Pinned mathlib remained unmodified at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The successful kernel replay was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-23d17225-slot53.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base_lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 Proof.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 Counterexample.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry condition

Reopen source-fidelity and statement review, identify the missing endpoint condition, correct and
re-elaborate the canonical target, and regenerate the obligation registry, typed graphs, and every
dependent fingerprint before retrying proof execution.

This fresh current-base artifact is proof-refutation evidence, not a proof receipt. It does not
satisfy `S56-M-1241-PROOF`, propose scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
