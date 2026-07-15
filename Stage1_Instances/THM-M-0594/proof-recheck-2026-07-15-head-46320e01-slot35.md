# THM-M-0594 proof recheck at 46320e01 (slot35)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T14:02:34+08:00

Base revision: `46320e01d1897482417e7b0d03a15a5b77ae5275`

Base tree: `2260ad94d18a6662ffc00f47b8955ae3a2a18184`

## Verdict

`blocked`. No placeholder-free proof body for the exact unrestricted
`WhitneyEmbeddingTarget` exists in the pinned dependency closure. This attempt
does not add compactness, weaken the conclusion, or count a conditional
constructor as a proof. The proof item remains `[ ]`, lifecycle remains
`planned`, and the root remains `[H1, M3, R3]`. No receipt acceptance,
validation, release, audit completion, or theorem completion is claimed.
Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The exact target covers every finite-dimensional, Hausdorff, second-countable,
boundaryless smooth real manifold. It asks for one map into some
finite-dimensional Euclidean space that is globally smooth, is a topological
embedding, and has injective manifold derivative everywhere. It has neither a
`CompactSpace` premise nor a fixed target-dimension bound.

## First Failed Gate

`M0594-C-GLOBAL` remains open: no local or pinned proof constructs one finite
Euclidean tuple with injective derivative, global point separation, and
properness on an unrestricted noncompact manifold. The frozen immediate root
cut set remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

The checked bodies in `ProofSupport.lean` derive a compact exhaustion, a
locally finite smooth bump covering, and the proper-injective topological
endpoint. `ObligationTree.lean` checks root assembly from an already supplied
smooth embedding witness. None constructs the finite witness required by the
root.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite cover index. `SmoothBumpCovering.fintype` and the terminal
`exists_embedding_euclidean_of_compact` theorem require `CompactSpace M`.
The pinned module explicitly leaves the sigma-compact weak Whitney theorem as
a TODO requiring Sard and Hausdorff-dimension infrastructure. A bounded search
of repository-local Lean and installed pinned packages found only the exact
statement, conditional/support declarations, and compact specializations.

## Smallest Real Validation

No Lake update, build, dependency clone/fetch, or `.lake` mutation ran. The
automation-provided `.lake` symlink was reused read-only. The canonical
`flt-regular` checkout had an invalid `HEAD`, so the literal unoverridden
`lake env lean` command stopped before elaboration. Rather than repair or fetch
that shared checkout, the successful narrow checks used a temporary
`lake --packages` JSON entry that mapped `flt-regular` to the same existing
local directory as a path dependency. The override and temporary object files
were removed after each check; the pinned manifest and dependency cache were
not changed. This is current-worker corroboration, not hermetic release
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| unoverridden `lake env lean --trust=0 -t0 .../Statement.lean` | 1 | Lake stopped before Lean because the shared `flt-regular` checkout could not resolve `HEAD`; no cache repair was attempted |
| temporary path override plus `lake --packages=OVERRIDE env lean --trust=0 -t0 .../Statement.lean` | 0 | exact unrestricted target elaborated using the pinned Lean and mathlib artifacts |
| the same narrow Lake check for `ProofSupport.lean` | 0 | all three support bodies elaborated; axiom reports exactly `[propext, Classical.choice, Quot.sound]`; type probes expose the finite-index/compactness boundary |
| the same narrow Lake check for `AnchorAudit.lean` | 0 | compact-only wrapper elaborated; axiom report exactly `[propext, Classical.choice, Quot.sound]` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` through the same override | 0 | exact target and conditional root composition elaborated; composition axioms exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| prohibited-construct scan of owned Lean files | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney-module endpoint/TODO scan | 0 | only finite-index immersion and compact-only embedding endpoints; unrestricted theorem explicitly TODO |
| bounded repository and installed-package declaration search | 0 | only the exact statement, compact wrappers, support references, and restricted pinned endpoints were located |

The isolated composition recipe generated no repository object file:

```bash
set -euo pipefail
repo_root=$PWD
pkg="$repo_root/Formalizations/Lean/.lake/packages/flt-regular"
target="$repo_root/Stage1_Instances/THM-M-0594"
override=$(mktemp /tmp/thm-m-0594-lake-override.XXXXXX.json)
tmp=$(mktemp -d /tmp/thm-m-0594-slot35-lake.XXXXXX)
trap 'rm -f "$override"; rm -rf "$tmp"' EXIT
printf '{"version":"1.1.0","packages":[{"type":"path","name":"«flt-regular»","scope":"","dir":"%s","configFile":"lakefile.toml","manifestFile":"lake-manifest.json","inherited":false}]}\n' \
  "$pkg" > "$override"
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cd Formalizations/Lean
lean=$(lake --packages="$override" env which lean)
lean_path=$(lake --packages="$override" env printenv LEAN_PATH)
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean" \
  --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean" \
  --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Exact source hashes and the complete command ledger are in the paired JSON.

## Retry Condition

Resume proof execution only after implementing the frozen noncompact weak
Whitney construction with checked child-to-parent composition, or after placing
an immutable, license-compatible proof of the exact unrestricted target into
the pinned repository-local dependency closure. Restore the pinned
`flt-regular` checkout before release validation. A compact-only theorem,
infinite-dimensional topological embedding, or conditional witness constructor
is not a substitute.
