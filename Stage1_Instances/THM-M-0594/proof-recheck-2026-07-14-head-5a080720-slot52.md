# THM-M-0594 proof recheck at 5a080720 (slot52)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-14T03:27:18+08:00

Base revision: `5a080720059200b542aa35ee17a748b3251fe8d0`

Base tree: `d7029aa7599db39fbcc55e968a4fe70376143f27`

## Verdict

`blocked`. The exact unrestricted `WhitneyEmbeddingTarget` still has no
placeholder-free local proof body and no eligible proof in the pinned dependency
closure. The proof item remains `[ ]`, lifecycle remains `planned`, and the root
remains `[H1, M3, R3]`. No acceptance, validation, release, or theorem-completion
claim is made. Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The frozen target covers every finite-dimensional, Hausdorff, second-countable,
boundaryless smooth real manifold. It asks for one map into a finite-dimensional
Euclidean space that is globally smooth, is a topological embedding, and has
injective manifold derivative everywhere. It has neither a `CompactSpace`
premise nor a fixed target-dimension bound.

## First failed gate

`M0594-C-GLOBAL` remains open: no local or pinned body constructs a single finite
Euclidean map with injective derivative, global point separation, and properness
on the unrestricted noncompact manifold. The frozen immediate root cut set is:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

The existing checked support is genuine but does not close that cut set.
`ProofSupport.lean` derives a compact exhaustion and an arbitrarily indexed
locally finite smooth bump covering, and proves proper plus injective implies
`IsEmbedding`. `ObligationTree.lean` packages an already supplied embedding
witness. None of these bodies constructs the required finite witness.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
`Finite` cover index. The construction of such an index and the terminal
`exists_embedding_euclidean_of_compact` theorem require `CompactSpace M`.
The module explicitly leaves the sigma-compact weak Whitney theorem as a TODO
requiring Sard/Hausdorff-dimension machinery. An independent bounded search of
the repository and installed pinned packages found no unrestricted terminal
body. The already cached immutable mathlib `origin/master` commit
`4efb186f102ebfd2eea1545c151d6fbcfdff0e43` retains the same TODO and restricted
endpoints; it is not the pinned dependency and receives no proof credit.

## Smallest real validation

All Lean checks used the existing pinned toolchain at trust level zero. The
automation-provided `.lake` symlink was reused read-only. No Lake update, build,
clone, fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | exact unrestricted target elaborated |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/ProofSupport.lean` | 0 | all three support bodies elaborated; their axiom reports are exactly `[propext, Classical.choice, Quot.sound]` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact target and conditional root composition elaborated; composition axioms are `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide\|proof_wanted' Stage1_Instances/THM-M-0594 --glob '*.lean'` | 1 | expected no-match: no prohibited construct in owned Lean sources |
| declaration/TODO search in pinned `WhitneyEmbedding.lean` | 0 | only finite-index immersion and compact-only embedding existence endpoints; unrestricted theorem explicitly TODO |
| same bounded search in cached mathlib `origin/master` | 0 | cached commit retains the same TODO and restricted endpoints |

The isolated composition recipe generated no repository artifacts:

```bash
tmp=$(mktemp -d /tmp/thm-m-0594-slot52-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_root=$PWD/Formalizations/Lean
target=$PWD/Stage1_Instances/THM-M-0594
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
the pinned repository-local closure. A compact-only result, an
infinite-dimensional topological embedding, or a conditional witness
constructor is not a substitute.
