# THM-M-0594 proof recheck at ffea62ba

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-14T02:33:37+08:00

Base revision: `ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330`

Base tree: `4662e08d189bd534919775f750c6909591aeafcb`

## Verdict

`blocked`. No placeholder-free local body or eligible pinned import closes the
exact unrestricted `WhitneyEmbeddingTarget`. The execution item remains `[ ]`,
the root remains `[H1, M3, R3]`, and no receipt acceptance, audit completion,
theorem completion, validation, release, or master acceptance is claimed.
Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The target ranges over every finite-dimensional, Hausdorff, second-countable,
boundaryless smooth real manifold. It requires one map into a finite-dimensional
real Euclidean space that is globally smooth, is a topological embedding, and
has injective manifold derivative everywhere. It has no `CompactSpace` premise
and no substituted dimension bound.

## Failed gate

The first missing root-critical body is `M0594-C-GLOBAL`: the pinned closure has
no construction of one finite Euclidean tuple that simultaneously has
injective derivative, separates all points, and is proper on a general
noncompact manifold. The frozen immediate cut set remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

The existing `ProofSupport.lean` bodies are real checked progress, but not root
closure. They produce a compact exhaustion and a locally finite smooth bump
covering, and prove that a proper injective map is an `IsEmbedding`. The bump
cover index is not finite, while the topological endpoint consumes rather than
constructs properness and point separation. `ObligationTree.lean` similarly
packages an already supplied smooth embedding witness without constructing it.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires
`[Finite iota]`, and `SmoothBumpCovering.fintype` obtains that index only from
`[CompactSpace M]`. Its final theorem is therefore
`exists_embedding_euclidean_of_compact`, a strict specialization. The module
header explicitly leaves the sigma-compact weak Whitney theorem as TODO work
requiring Sard and Hausdorff-dimension infrastructure. The read-only cached
mathlib `origin/master` commit
`4efb186f102ebfd2eea1545c151d6fbcfdff0e43` still has the same boundary.

## Validation

All kernel commands used the existing pinned toolchain with trust level zero.
The automation-provided canonical `.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | exact unrestricted target elaborated |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/ProofSupport.lean` | 0 | all three support declarations elaborated; each axiom report was exactly `[propext, Classical.choice, Quot.sound]`; type probes confirmed the finite-index/compactness boundary |
| isolated temporary-olean trust-zero replay for `Statement.lean` and `ObligationTree.lean` | 0 | exact statement and conditional root composition elaborated; composition axioms were exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations, 46 typed edges, denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide\|proof_wanted' Stage1_Instances/THM-M-0594 --glob '*.lean'` | 1 | expected no-match: no prohibited construct in owned Lean sources |
| declaration search in pinned `WhitneyEmbedding.lean` | 0 | only finite-index immersion and compact-only embedding existence endpoints |
| cached `origin/master` Whitney-module audit | 0 | immutable cached commit `4efb186f...0e43` retains the TODO and the same restricted endpoints |
| unauthenticated GitHub repository query for quoted Whitney embedding plus Lean | 0 | `total_count: 0`; code-search routes were rate-limited or blocked and receive no exhaustive-search or proof credit |
| `git status --short --untracked-files=all` before this receipt | 0 | only the automation-provided `.lake` symlink was untracked |
| `python3 -m json.tool Stage1_Instances/THM-M-0594/proof-recheck-2026-07-14-head-ffea62ba.json >/dev/null` | 0 | structured blocker record is valid JSON |
| strict SHA-256 verification for the eight recorded source hashes | 0 | all owned-source and pinned Whitney-module hashes matched |
| wrapped `git diff --no-index --check /dev/null FILE` for both fresh artifacts | 0 | each raw diff exited 1 because the file is new, emitted no whitespace diagnostic, and the expected-exit wrapper passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent because the proof phase is blocked |
| final scoped `git status --short --untracked-files=all` | 0 | only the preexisting `.lake` symlink and the two fresh owned blocker artifacts were listed |

The isolated composition check confined generated objects to a removed
temporary directory:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0594
tmp=$(mktemp -d /tmp/thm-m-0594-current-proof.XXXXXX)
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
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Exact source hashes and the full command ledger are in the paired JSON record.

## Retry condition

Resume proof execution only after implementing the frozen noncompact
weak-Whitney construction with checked child-to-parent composition, or after
placing an immutable, license-compatible proof of the exact unrestricted
target into the pinned repository-local closure. A compact-only result,
infinite-dimensional topological embedding, or conditional constructor is not
a substitute.
