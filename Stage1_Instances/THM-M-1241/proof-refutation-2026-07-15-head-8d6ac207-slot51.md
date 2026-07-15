# THM-M-1241 proof-phase refutation at current base

Item: `S56-M-1241-PROOF`

Recorded at: `2026-07-15T13:37:04+08:00` (`Asia/Shanghai`)

Base revision: `8d6ac2078d37dc107d80c38c020de01c6f9affce`

Base tree: `a9332226f35fa562b7dbbe9feab5f5a2da80d013`

## Verdict

`blocked`. The exact frozen proposition is false. `Counterexample.lean` proves the placeholder-free
kernel theorem
`Stage1Instances.THM_M_1241.not_gagliardoNirenbergTarget :
  not Stage1Instances.THM_M_1241.GagliardoNirenbergTarget`.

The counterexample specializes the target to

```text
n = 1, m = 1, j = 0, q = infinity, r = 1, p = infinity, a = 1,
u = the constant function 1.
```

All parameter hypotheses hold. The printed exceptional hypothesis is not required because its
antecedent contains `r.toReal * m < n`, which becomes `1 < 1`. The constant function is `C^1`, its
order-zero `L^infinity` seminorm is `1`, and its order-one `L^1` seminorm is `0`. The asserted
inequality therefore reduces to `1 <= C * 0 ^ 1 * 1 ^ 0 = 0`, a contradiction for every
`C : NNReal`.

The checked refutation applies to this frozen formal encoding. It identifies an apparent omitted
critical endpoint condition, but it does not by itself refute the correctly stated classical
Gagliardo-Nirenberg theorem or settle the primary-source transcription; the proposed `H5/M5`
classification remains subject to master review.

This is not the previously recorded degenerate `p = 0` fragment. It is a nonzero endpoint admitted
by the exact statement. Consequently neither `InfiniteEndpointPackage` nor the canonical root can
have a proof body in a consistent environment. The first failed proof gate is now the stronger
`M1241-T-ENDPOINT` refutation, and the proof phase cannot be completed by further implementation or
by importing a compatible theorem of the same type.

## Narrow validation

All commands ran in this worker clone. No network operation, dependency fetch, Lake update, Lake
build, or `.lake` mutation was performed. The automation-provided `.lake` symlink was reused only
for already-built libraries. Full Lake environment derivation remains unavailable because the
shared `flt-regular` checkout cannot resolve `HEAD`; the counterexample replay used an explicit
`LEAN_PATH` assembled from existing build-library directories and excluded that incomplete package.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; root M3, both terminal packages M4. |
| scoped trust-zero `lake env lean` recipe below | 0 | `Statement.lean` and `Counterexample.lean` elaborated. `not_gagliardoNirenbergTarget` reports only `propext`, `Classical.choice`, and `Quot.sound`, and Lean reports it sorry-free. |
| `python3 Stage1_Instances/THM-M-1241/check_statement.py` | terminated | It stalled in `lake env lean` while Lake attempted to resolve the incomplete shared dependency checkout; its generated temporary source was removed and no dependency was repaired. |
| `cd Formalizations/Lean && lake env printenv LEAN_PATH` | terminated | It likewise stalled while resolving the incomplete shared `flt-regular` checkout. |
| prohibited-device scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `extern` token. |
| `git -C Formalizations/Lean/.lake/packages/mathlib diff --quiet` | 0 | The pinned mathlib checkout was not modified. |

The successful replay was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-slot51-counterexample.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path="$lean_root/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
while IFS= read -r d; do lean_path="$lean_path:$d"; done < <(
  find -L "$lean_root/.lake/packages" -path '*/.lake/build/lib/lean' -type d \
    ! -path '*/flt-regular/*' -print | sort
)
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 Counterexample.lean
```

Pinned identities observed for the replayed environment are Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The refutation source SHA-256 is
`419ba289bd4fbf4e748948ceccc81ff7ee480ef33c33f0d10b6c94dc8b480719`.

## Retry condition

Correct and re-freeze the canonical statement so that the refuted endpoint is excluded or supplied
with the mathematically necessary side condition, then regenerate the obligation registry and all
dependent fingerprints before retrying proof execution. The exact correction must come from a new
source-fidelity review; this worker does not broaden or silently substitute the assigned theorem.

This is proof-phase refutation evidence, not a proof receipt. It does not satisfy
`S56-M-1241-PROOF`, change scheduler state, or claim audit completion, theorem completion,
validation, release, or master acceptance. Because the assigned phase is not complete,
`.stage1-worker-selftest.json` is intentionally absent.
