# THM-M-0594 proof recheck at 506796f9 (slot62)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T06:27:26+08:00

Base revision: `506796f90c31097a0d170410e431f83da4b1853c`

Base tree: `32c911b35ce53ab8fd2ad6bfd6a34bdc603ef50d`

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

## First failed gate

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
a TODO requiring Sard and Hausdorff-dimension infrastructure. Bounded searches
of repository-local Lean, installed pinned packages, cached mathlib refs, and
other local Lean worktrees found only the exact statement, support and
conditional declarations, compact specializations, and the same TODO. The
external code-search endpoints attempted during this recheck returned service
or authentication errors, so no external-search success is claimed.

## Smallest real validation

All Lean checks used the existing pinned toolchain at trust level zero. The
automation-provided untracked `.lake` symlink was reused read-only. No Lake
update, build, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | exact unrestricted target elaborated |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/ProofSupport.lean` | 0 | all three support bodies elaborated; their axiom reports are exactly `[propext, Classical.choice, Quot.sound]`; type probes expose the finite-index/compactness boundary |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/AnchorAudit.lean` | 0 | compact-only wrapper elaborated; its axiom report is exactly `[propext, Classical.choice, Quot.sound]` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact target and conditional root composition elaborated; composition axioms are exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| prohibited-construct scan of owned Lean files | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney-module endpoint/TODO scan | 0 | only finite-index immersion and compact-only embedding endpoints; unrestricted theorem explicitly TODO |
| bounded repository and installed-package declaration search | 0 | only the exact statement, compact wrappers, support references, and restricted pinned endpoints were located |

The isolated composition recipe generated no repository object file:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0594
tmp=$(mktemp -d /tmp/thm-m-0594-slot62-proof-506796f9.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
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

## Retry condition

Resume proof execution only after implementing the frozen noncompact weak
Whitney construction with checked child-to-parent composition, or after placing
an immutable, license-compatible proof of the exact unrestricted target into
the pinned repository-local dependency closure. A compact-only theorem,
infinite-dimensional topological embedding, or conditional witness constructor
is not a substitute.

Status boundary: this is fresh current-base nonrelease blocker evidence, not a
positive proof receipt. It does not satisfy `S56-M-0594-PROOF`, propose a
scheduler-state transition, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
