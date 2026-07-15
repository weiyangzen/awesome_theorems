# THM-M-1241 proof-phase refutation recheck at current base

Item: `S56-M-1241-PROOF`

Intent: `prove`

Recorded: `2026-07-16T00:01:10+08:00` (`Asia/Shanghai`)

Base revision: `49cc5eea2717a1ed25f08193051afd36df0958dc`

Base tree: `c99e09f2619b000ef8aa43f8940a3f4bac4cbd37`

## Verdict

`blocked`. No positive proof body or compatible pinned import can inhabit the exact frozen
proposition in a consistent Lean environment. The tracked placeholder-free declarations

```text
Stage1Instances.THM_M_1241.not_gagliardoNirenbergTarget :
  not Stage1Instances.THM_M_1241.GagliardoNirenbergTarget

Stage1Instances.THM_M_1241.not_infiniteEndpointPackage :
  not Stage1Instances.THM_M_1241.InfiniteEndpointPackage
```

were replayed from fresh temporary objects with `lake env lean --trust=0 -t0`. Both report only
`propext`, `Classical.choice`, and `Quot.sound`, and both are sorry-free. The second declaration
directly refutes registered terminal obligation `M1241-T-ENDPOINT`.

The counterexample specializes the target and endpoint package to

```text
n = 1, m = 1, j = 0, q = infinity, r = 1, p = infinity, a = 1,
u = the constant function 1.
```

All parameter hypotheses hold. The critical restriction is vacuous because it assumes `1 < r`.
The zero-order exceptional premise is also vacuous because its antecedent includes
`r.toReal * m < n`, which becomes `1 < 1`. The constant function has order-zero `L^infinity`
seminorm `1` and order-one `L^1` seminorm `0`, so every proposed constant would have to satisfy
`1 <= C * 0 ^ 1 * 1 ^ 0 = 0`.

This refutes only the frozen formal encoding. It identifies a missing endpoint or function-space
condition and does not refute a suitably corrected classical Gagliardo-Nirenberg theorem. Changing
the statement within this proof assignment would be an unauthorized theorem substitution and
would invalidate the statement fingerprint, registry, typed graphs, and dependent evidence.

The first failed gate is `M1241-T-ENDPOINT`, positively refuted rather than merely open. The
registry-v1 root cut remains `M1241-T-FINITE` plus `M1241-T-ENDPOINT`. `Proof.lean` establishes only
an unregistered `p = 0` fragment and closes no frozen obligation. The proof phase remains `[ ]`,
lifecycle remains `planned`, and no proof receipt or completion state is claimed. Because the
assigned positive phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation

All commands ran in this worker clone. The automation-provided `Formalizations/Lean/.lake` symlink
was reused read-only. Temporary Lean objects were written below `/tmp` and removed. No `lake
update`, `lake build`, dependency clone/fetch, network request, checkout repair, or `.lake` mutation
was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422; lifecycle `planned`; theorem incomplete. |
| `env LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1241/check_statement.py` | 0 | Exact expression fingerprint `bf613985e300aa3a5b5e8299a1e0e0e059369387e17c7f0d2c92dc8d8190eb82`; all four structural mutations killed; pinned toolchain and mathlib identity confirmed. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828bd656ec7e4545903a4fdd42a5c759de71b31e46f8c4c189be864991e`; registry still projects root M3 and both terminal packages M4. |
| isolated trust-zero five-module recipe below | 0 | Fresh oleans had sizes 76664, 47368, 71384, 136784, and 147592 bytes. Both refutations report only `propext`, `Classical.choice`, and `Quot.sound` and are sorry-free. |
| prohibited-device scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `extern`, `implemented_by`, or `native_decide` token. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | No output; pinned mathlib remained unmodified. |
| `git diff --check -- Stage1_Instances/THM-M-1241` | 0 | No whitespace errors in the tracked owned-path delta. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |
| `python3 -m json.tool Stage1_Instances/THM-M-1241/proof-refutation-recheck-2026-07-16-head-49cc5eea-slot32.json` | 0 | The structured blocker artifact is valid JSON. |
| blocked-handoff `jq` shape check | 0 | Item, theorem, verdict, open state, two unique changed paths, incomplete proof phase, and absent completion-selftest declaration passed. |
| `git diff --no-index --check /dev/null <new-file>`, repeated for both changed paths | 1 each | Expected no-index difference exits with empty diagnostic output; neither new file has a whitespace error. |

The successful kernel replay recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-49cc5eea-slot32.XXXXXX)
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
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/Proof.olean" Proof.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/Counterexample.olean" Counterexample.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/EndpointCounterexample.olean" EndpointCounterexample.lean
stat -c '%n %s bytes' "$tmp/Statement.olean" "$tmp/ObligationTree.olean" \
  "$tmp/Proof.olean" "$tmp/Counterexample.olean" "$tmp/EndpointCounterexample.olean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry condition

Reopen source-fidelity and statement review, identify the exact missing endpoint or function-space
condition, correct and re-elaborate the canonical target, and regenerate the obligation registry,
typed graphs, and all dependent fingerprints before retrying proof execution. Silently
strengthening or substituting the theorem in this proof phase is forbidden.

This current-base artifact is nonrelease proof-refutation evidence, not a proof receipt. It does
not satisfy `S56-M-1241-PROOF`, propose scheduler state, or claim audit completion, theorem
completion, validation, release, receipt acceptance, or master acceptance.
