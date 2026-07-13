# THM-M-0594 proof recheck at fcfd52dc (slot52)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-14T04:00:22+08:00

Base revision: `fcfd52dc69db3bf455310be55903278133a15a10`

Base tree: `3580154b2d6b61f9bfee3079ce78939155de16ca`

## Verdict

`blocked`. No placeholder-free body for the exact unrestricted
`WhitneyEmbeddingTarget` exists in the pinned dependency closure. This attempt
does not add compactness, weaken the conclusion, or mistake a conditional
constructor for a proof. The proof item remains `[ ]`, lifecycle remains
`planned`, and the root remains `[H1, M3, R3]`. No receipt acceptance,
validation, release, audit completion, or theorem completion is claimed.
Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The target covers every finite-dimensional, Hausdorff, second-countable,
boundaryless smooth real manifold. It asks for one map into a
finite-dimensional Euclidean space that is globally smooth, is a topological
embedding, and has injective manifold derivative everywhere. It has no
`CompactSpace` premise and no fixed target-dimension bound.

## First failed gate

`M0594-C-GLOBAL` remains open: no local or pinned proof constructs one finite
Euclidean tuple with injective derivative, global point separation, and
properness on an unrestricted noncompact manifold. The frozen immediate root
cut set remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

`ProofSupport.lean` supplies real checked progress: a compact exhaustion, a
locally finite smooth bump covering, and the proper-injective topological
endpoint. `ObligationTree.lean` checks root assembly from an already supplied
smooth embedding witness. None constructs the finite witness required by the
root.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite cover index, while `SmoothBumpCovering.fintype` and the terminal
`exists_embedding_euclidean_of_compact` theorem require `CompactSpace M`. The
module header explicitly leaves the sigma-compact weak Whitney theorem as TODO
work requiring Sard and Hausdorff-dimension infrastructure. A repository and
pinned-package declaration search found no unrestricted terminal body. A
read-only check of cached refs likewise found no eligible body; cached refs are
not pinned proof dependencies and receive no proof credit.

## Smallest real validation

All Lean checks used the existing pinned toolchain at trust level zero. The
automation-provided `.lake` symlink was reused read-only. No Lake update,
build, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| trust-zero elaboration of `Statement.lean` | 0 | the exact unrestricted target elaborated |
| trust-zero elaboration of `ProofSupport.lean` | 0 | all three support bodies elaborated; axioms are exactly `[propext, Classical.choice, Quot.sound]`; type probes expose the finite-index/compactness boundary |
| trust-zero elaboration of `AnchorAudit.lean` | 0 | compact-only wrapper elaborated; axioms are exactly `[propext, Classical.choice, Quot.sound]` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact statement and conditional root composition elaborated; composition axioms are exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| prohibited-construct scan of owned Lean files | 1 | expected no-match: no `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney-module endpoint/TODO search | 0 | only finite-index immersion and compact-only embedding endpoints; unrestricted theorem is explicitly TODO |
| `git diff --no-index --check /dev/null FILE` for each fresh artifact, accepting raw exit 1 only with empty output | 0 | both fresh files differ from `/dev/null` and emitted no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion manifest is absent because the proof phase is blocked |

The isolated composition replay used this exact recipe and left no repository
object file:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0594
tmp=$(mktemp -d /tmp/thm-m-0594-fcfd52dc-proof.XXXXXX)
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

The complete command forms and exact source/environment hashes are recorded in
the paired JSON artifact. Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry condition

Resume proof execution only after implementing the frozen noncompact
weak-Whitney construction with checked child-to-parent composition, or after
placing an immutable, license-compatible proof of the exact unrestricted
target into the pinned repository-local closure. A compact-only theorem,
infinite-dimensional topological embedding, or conditional witness constructor
is not a substitute.
