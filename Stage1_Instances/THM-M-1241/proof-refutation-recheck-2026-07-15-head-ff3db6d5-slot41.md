# THM-M-1241 proof-phase refutation recheck at current base

Item: `S56-M-1241-PROOF`

Base revision: `ff3db6d51326417873f49c410421f8f3e13be993`

## Verdict

`blocked`: the exact frozen proposition cannot receive the requested positive proof body because
the tracked, placeholder-free Lean theorem
`Stage1Instances.THM_M_1241.not_gagliardoNirenbergTarget` proves its negation.

The checked counterexample specializes the target to `n = m = r = 1`, `j = 0`,
`q = p = infinity`, `a = 1`, and the constant function `u = 1`. The critical-case restriction
does not apply because it assumes `1 < r`, while the zero-order exceptional hypothesis is vacuous
because its antecedent contains `r.toReal * m < n`, which reduces to `1 < 1`. The target therefore
asserts an estimate whose two sides reduce to `1` and `0`.

This refutes only the frozen formal encoding. It points to a missing explicit or implicit endpoint
side condition and does not refute a suitably corrected classical Gagliardo-Nirenberg theorem.
Correcting the proposition is outside this proof-phase assignment: doing so would change the
canonical expression fingerprint and require a new statement review, obligation registry, typed
graphs, and dependent evidence.

The first failed gate is `M1241-T-ENDPOINT`: its admitted `r = 1` instance directly requires the
false fixed-parameter conclusion exhibited by the counterexample. The registry-v1 root cut remains
`M1241-T-FINITE` plus `M1241-T-ENDPOINT`.
`Proof.lean` proves only an unregistered `p = 0` fragment, and
`root_of_finite_and_endpoint_packages` consumes rather than constructs the two terminal packages.
No positive proof body, proof receipt, state change, or completion claim is made. Because the
assigned proof phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation

All commands ran in this worker clone. The automation-provided `Formalizations/Lean/.lake` symlink
was reused read-only. Temporary Lean objects were placed below `/tmp` and removed. No `lake update`,
`lake build`, dependency clone/fetch, network discovery, checkout repair, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_statement.py` | 0 | Exact statement fingerprint `bf613985e300aa3a5b5e8299a1e0e0e059369387e17c7f0d2c92dc8d8190eb82`; all four structural mutations killed; pinned toolchain and mathlib identity confirmed. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828bd656ec7e4545903a4fdd42a5c759de71b31e46f8c4c189be864991e`; registry still projects root M3 and both terminal packages M4. |
| isolated Lake-derived trust-zero four-module recipe below | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Counterexample.lean` elaborated. The composer, partial proofs, and refutation report only `propext`, `Classical.choice`, and `Quot.sound`; all printed proof/refutation declarations report sorry-free. |
| prohibited-device scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `extern`, `implemented_by`, or `native_decide` token. |
| `git -C Formalizations/Lean/.lake/packages/mathlib diff --quiet` | 0 | Pinned mathlib remained unmodified at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The kernel replay recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-slot41-current.XXXXXX)
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
re-elaborate the canonical target, and regenerate the obligation registry, typed graphs, and all
dependent fingerprints before retrying proof execution. Silently strengthening the proposition in
this proof phase would be a forbidden theorem substitution.

This fresh current-base artifact is proof-refutation evidence, not a proof receipt. It does not
satisfy `S56-M-1241-PROOF`, propose scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
