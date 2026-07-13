# THM-M-0594 proof recheck at bad90e2e (slot52)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-14T03:40:49+08:00

Base revision: `bad90e2e2479d376609447202eb4f437789d0d11`

Base tree: `df3ade7b4d06057f8aac33369c3d69bd391aa05a`

## Verdict

`blocked`. No placeholder-free body for the exact unrestricted
`WhitneyEmbeddingTarget` exists in the pinned dependency closure, and this run
did not manufacture one by adding compactness or weakening the conclusion. The
proof item remains `[ ]`, lifecycle remains `planned`, and the root remains
`[H1, M3, R3]`. No acceptance, validation, release, or theorem-completion claim
is made. Because the positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The exact target covers every finite-dimensional, Hausdorff, second-countable,
boundaryless smooth real manifold, with no `CompactSpace` premise. It asks for
one map into a finite-dimensional Euclidean space that is globally smooth, is a
topological embedding, and has injective manifold derivative everywhere.

## First failed gate

`M0594-C-GLOBAL` remains open: no local or pinned body constructs a single
finite-dimensional Euclidean map with injective derivative, global point
separation, and properness on the unrestricted noncompact manifold. The frozen
immediate root cut set remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

The checked support does not close this cut set. `ProofSupport.lean` derives a
compact exhaustion and a locally finite smooth bump covering, and proves that a
proper injective continuous map is an embedding. `ObligationTree.lean` packages
an already supplied smooth embedding witness. None constructs the required
finite witness.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` needs a finite
cover index, while `exists_embedding_euclidean_of_compact` needs
`CompactSpace M`. The module explicitly leaves the sigma-compact weak Whitney
theorem as a TODO requiring Sard/Hausdorff-dimension machinery. Thirty distinct
cached historical versions of that module were inspected; the relevant cached
modern refs, including `origin/master` at `4efb186f...`, retain the same TODO and
compact endpoint. No cached ref receives proof credit.

A supplemental network search found the LeanEval Whitney problem at immutable
head `f4d4534a28341956978d26fed42162a2c1d72f59` (PR 353), but its theorem body is
literally `by sorry`. The related Sard problem at head
`f31b858d6d8a7f5933163283b8926a791d1295dc` (PR 377) is also `by sorry`. These
Apache-2.0 benchmark prompts are placeholders, not external proof candidates.

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
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/AnchorAudit.lean` | 0 | compact-only wrapper elaborated; its axiom report is exactly `[propext, Classical.choice, Quot.sound]` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact target and conditional root composition elaborated; composition axioms are `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide\|proof_wanted' Stage1_Instances/THM-M-0594 --glob '*.lean'` | 1 | expected no-match: no prohibited construct in owned Lean sources |
| cached-object and selected-ref inspection of `Mathlib/Geometry/Manifold/WhitneyEmbedding.lean` | 0 | 30 distinct cached source blobs; selected modern refs retain the noncompact TODO and compact-only endpoint |
| GitHub API plus immutable raw-source probes for LeanEval PRs 353 and 377 | 0 | both external problem declarations end in `by sorry`; no proof credit |
| `python3 -m json.tool Stage1_Instances/THM-M-0594/proof-recheck-2026-07-14-head-bad90e2e-slot52.json >/dev/null` | 0 | structured blocker record is valid JSON |
| no-index whitespace checks for both fresh blocker artifacts | 0 | both files differ from `/dev/null` and have no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion manifest is absent because the positive proof phase is blocked |

The isolated composition recipe generated no repository artifacts:

```bash
tmp=$(mktemp -d /tmp/thm-m-0594-slot52-proof-bad90e2e.XXXXXX)
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
infinite-dimensional topological embedding, a benchmark hole, or a conditional
witness constructor is not a substitute.
