# THM-M-1241 proof refutation recheck at current base

Item: `S56-M-1241-PROOF`

Intent: `prove`

Recorded: `2026-07-15T14:37:20+08:00` (`Asia/Shanghai`)

Base revision: `29a69c34f06bf3444399287853ea7806767d0944`

Base tree: `de0efce35b6fcc6f851b9c2e643d61ec49d831e0`

## Verdict

`blocked`. The exact frozen proposition is false, so no positive proof body can be implemented or
imported in a consistent Lean environment. The tracked declaration

```text
Stage1Instances.THM_M_1241.not_gagliardoNirenbergTarget :
  not Stage1Instances.THM_M_1241.GagliardoNirenbergTarget
```

was replayed at the current base with `lake env lean --trust=0 -t0`. Lean reports exactly
`[propext, Classical.choice, Quot.sound]` and `Declarations are sorry-free!`.

The counterexample specializes the frozen target to

```text
n = 1, m = 1, j = 0, q = infinity, r = 1, p = infinity, a = 1,
u = the constant function 1.
```

Every parameter hypothesis holds. The zero-order exceptional premise is not needed because its
antecedent includes `r.toReal * m < n`, which reduces to `1 < 1`. The constant function has
order-zero `L^infinity` seminorm `1` and order-one `L^1` seminorm `0`, so the requested estimate
reduces to `1 <= 0` for every proposed constant.

This refutes only the frozen formal encoding. It indicates a missing explicit or implicit endpoint
side condition; it does not refute a suitably corrected classical Gagliardo-Nirenberg theorem.
Independent source reinspection found that the printed passage does permit `r = 1`, so the defect
cannot safely be repaired as a mere transcription typo without a fresh source-fidelity decision.
`Proof.lean` still proves only the unregistered `p = 0` fragment, and
`root_of_finite_and_endpoint_packages` still consumes rather than constructs the terminal packages.

The first failed gate is `M1241-T-ENDPOINT`: `InfiniteEndpointPackage` is inconsistent with the
checked counterexample. The registry-v1 root cut remains `M1241-T-FINITE` plus
`M1241-T-ENDPOINT`, but the endpoint member is now positively refuted rather than merely missing.
The proof item remains `[ ]`, lifecycle remains `planned`, and no receipt or completion state is
claimed. Because the assigned positive proof phase is not complete, `.stage1-worker-selftest.json`
is deliberately absent.

## Narrow validation

All commands ran in this worker clone. The automation-provided `Formalizations/Lean/.lake` symlink
was treated as read-only and reused the canonical pinned artifacts. Temporary Lean objects and logs
were written only below `/tmp` and removed. No `lake update`, `lake build`, dependency clone/fetch,
network discovery, checkout repair, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_statement.py` | 0 | Exact statement fingerprint `bf613985...9feb82`; all four structural mutations killed; pinned toolchain and mathlib identity confirmed. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828...864991e`; registry still projects root M3 and both terminal packages M4. |
| isolated Lake-derived trust-zero four-module recipe below | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Counterexample.lean` elaborated. The checked declarations report only `propext`, `Classical.choice`, and `Quot.sound`; proof and counterexample declarations report sorry-free. |
| prohibited-device scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `extern`, `implemented_by`, or `native_decide` token. |
| `git -C Formalizations/Lean/.lake/packages/mathlib diff --quiet` | 0 | Pinned mathlib remained unmodified at revision `8a178386...95`, tree `bdc39a31...e3c2b`. |
| `git diff --no-index --check /dev/null <new artifact>` for both new artifacts | 1 each | Expected content-difference exits with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The kernel replay recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-slot37-proof.XXXXXX)
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

Reopen source-fidelity and statement review, identify the exact missing endpoint side condition,
correct and re-elaborate the canonical target, and regenerate the obligation registry, typed graphs,
and all dependent fingerprints before retrying proof execution. Silently strengthening the current
statement in this proof phase would be an unauthorized theorem substitution.

This is fresh current-base proof-refutation evidence, not a proof receipt. It does not satisfy
`S56-M-1241-PROOF`, propose scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
