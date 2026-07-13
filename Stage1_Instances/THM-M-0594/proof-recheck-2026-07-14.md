# THM-M-0594 proof-phase recheck

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `055d2986f15165228f00094a7de24a77795055a2`

Base tree: `0fced52df7813bdc38ea71f4d649a788bb895512`

## Verdict

`blocked`. No placeholder-free proof body or eligible pinned import closes the
exact unrestricted `WhitneyEmbeddingTarget`. The item remains `[ ]`, the root
remains `[H1, M3, R3]`, and no audit, theorem-completion, validation, release,
receipt-acceptance, or master-acceptance claim is made. Because the assigned
positive proof phase is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

The frozen target asks for one finite-dimensional Euclidean map on every
Hausdorff, second-countable, boundaryless finite-dimensional real smooth
manifold, with global smoothness, `IsEmbedding`, and pointwise injective
`mfderiv`. It has no compactness hypothesis and no substituted dimension or
special-case boundary.

## Checked progress

`ProofSupport.lean` adds three real, trust-zero checked supporting lemmas:

- `exists_compact_exhaustion` derives a `CompactExhaustion M` from the target's
  finite-dimensional and second-countable manifold assumptions;
- `exists_global_smooth_bump_covering` derives a locally finite smooth bump
  covering of all of `M`;
- `isEmbedding_of_isProperMap_of_injective` checks the topological bridge from
  a proper injective map to `IsEmbedding`.

Each declaration's axiom report is exactly `[propext, Classical.choice,
Quot.sound]`. These are partial infrastructure bodies only. The bump-cover
index is not finite, and the topological lemma consumes rather than constructs
properness and injectivity. Consequently none of the frozen open obligations
or root debt states changes.

## Failed gate

The first unavailable root-critical proof body is `M0594-C-GLOBAL`: the pinned
closure has no construction of one finite Euclidean tuple that simultaneously
has injective derivative, separates every pair of points, and is proper on a
general noncompact manifold. `M0594-L-TOPOLOGICAL` is now checked only as a
conditional proper-injective bridge; it still lacks the required constructed
premises. The frozen immediate cut set therefore remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite index type. The available `SmoothBumpCovering.fintype` obtains that only
from `[CompactSpace M]`. Accordingly the strongest terminal theorem remains
`exists_embedding_euclidean_of_compact`, which proves a strict specialization
and cannot close the root. The header of the pinned Whitney module explicitly
lists the sigma-compact weak Whitney theorem as TODO work requiring
Sard/Hausdorff-dimension machinery. Bounded repository and dependency-source
searches found only historical compact wrappers and the same explicit open
boundary, not an unrestricted terminal body.

## Validation

All commands ran in this worker clone and reused the automation-provided
canonical `.lake` symlink read-only. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed.

Two preliminary elaborations of the new support file exited `1` during
authoring: the first exposed an extra application of
`Manifold.locallyCompact_of_finiteDimensional` and an unqualified `univ_mem`;
the second retained only the `univ_mem` error. The failed declarations' error
reports included `sorryAx`, as Lean does for incomplete elaboration. Neither
draft was retained or credited. The source was corrected to
`Filter.univ_mem`, after which the trust-zero check below passed with no
`sorryAx`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255; planned; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/ProofSupport.lean` | 0 | support bodies elaborated with the stated axiom reports; type probes confirmed the finite-index/compactness boundary |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | exact unrestricted canonical target elaborated |
| isolated temporary-olean trust-zero recipe for `Statement.lean` and `ObligationTree.lean` | 0 | exact statement and conditional root composition elaborated; composition axioms were `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root remains open M3 |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-0594 --glob '*.lean'` | 1 | expected no-match: no prohibited construct in owned Lean sources |
| declaration search in pinned `WhitneyEmbedding.lean` | 0 | only finite-index immersion and compact-only embedding existence theorems |
| bounded local/pinned semantic source search | 0 | historical compact wrappers and open-boundary metadata only; no unrestricted terminal proof |
| `python3 -m json.tool Stage1_Instances/THM-M-0594/proof-recheck-2026-07-14.json` | 0 | structured blocker syntax passed |
| source-hash verification against the structured record | 0 | every recorded source hash matched its current file |
| three wrapped `git diff --no-index --check /dev/null FILE` checks | 0 | each raw diff exited 1 because the owned file is new and emitted no whitespace diagnostic; expected-exit wrappers passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |
| `git status --short` | 0 | only the preexisting `.lake` symlink and three new owned files were listed |

The isolated composition recipe ran from the repository root and confined its
objects to a removed temporary directory:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0594
tmp=$(mktemp -d /tmp/thm-m-0594-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -t0 -R "$tmp" \
  "$tmp/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Exact source hashes and obligation fingerprints are recorded in the structured
recheck artifact.

## Retry condition

Resume proof execution after implementing the frozen noncompact construction
and checked child-to-parent composition, or after placing an immutable,
license-compatible Lean 4 proof of the exact unrestricted target into the
pinned repository-local validation closure. A compact-only result, conditional
constructor, or supporting topology lemma does not meet that condition.
