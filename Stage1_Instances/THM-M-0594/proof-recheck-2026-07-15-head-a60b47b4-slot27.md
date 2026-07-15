# THM-M-0594 proof recheck at a60b47b4 (slot27)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T18:53:53+08:00

Base revision: `a60b47b4551b044fd5fad26599908ccef4000024`

Base tree: `58186bfbc3502322297e8d601fc091da540ba77b`

## Verdict

`blocked`. The exact unrestricted `WhitneyEmbeddingTarget` still has no
placeholder-free proof body in the pinned repository-local dependency closure.
This attempt does not add compactness, weaken the conclusion, or count an
empty-source case or conditional constructor as a root proof. The proof item
remains `[ ]`, the lifecycle remains `planned`, and the root remains
`[H1, M3, R3]`. No receipt acceptance, validation, release, audit completion,
theorem completion, or master acceptance is claimed. Because the assigned
proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately
absent.

The frozen target covers every finite-dimensional, Hausdorff,
second-countable, boundaryless smooth real manifold. It asks for a map into
some finite-dimensional Euclidean space that is globally smooth, is a
topological embedding, and has injective manifold derivative everywhere. It
has neither a `CompactSpace M` premise nor a fixed target-dimension bound.

## First Failed Gate

`M0594-C-GLOBAL` remains open: no local or pinned proof constructs one finite
Euclidean tuple with injective derivative, global point separation, and
properness on an unrestricted inhabited noncompact manifold. The frozen
immediate root cut set remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

The checked bodies in `ProofSupport.lean` derive a compact exhaustion, a
locally finite smooth bump covering, and a generic proper-injective
topological endpoint. `ObligationTree.lean` checks root assembly from an
already supplied smooth embedding witness. `ProofBoundary.lean` proves the
empty-source case. None constructs the finite witness required for an
inhabited noncompact source.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite cover index. `SmoothBumpCovering.fintype` and the terminal
`exists_embedding_euclidean_of_compact` theorem require `CompactSpace M`.
The pinned Whitney module explicitly leaves the sigma-compact weak theorem as
a TODO. A fresh exact-context trust-zero attempt through that compact endpoint
failed at the missing `CompactSpace M` instance, which confirms that the
available theorem is not a transport of the frozen root.

Pinned `Mathlib.Topology.MetricSpace.HausdorffDimension` does contain
`ContDiff.dimH_range_le` and
`ContDiff.dense_compl_range_of_finrank_lt_finrank`. Those lemmas could support
a future generic-projection proof, but they do not supply the missing
manifold-level projection reduction, finite-color patching across a compact
exhaustion, or smooth proper-exhaustion construction.

## Smallest Real Validation

The existing pinned toolchain and already built package objects were reused
read-only. No Lake update, Lake build, dependency clone/fetch, checkout,
repair, or `.lake` mutation ran. This is narrow current-worker corroboration,
not release evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground 300 lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e...ab16740` available through Lake |
| same directory, `lake env lean --trust=0 -t0` on `Statement.lean` | 0 | exact unrestricted target elaborated |
| same trust-zero replay on `ProofSupport.lean` | 0 | three support bodies elaborated; axioms exactly `[propext, Classical.choice, Quot.sound]`; finite-index/compactness boundary printed |
| same trust-zero replay on `AnchorAudit.lean` | 0 | compact-only wrapper elaborated; axioms exactly `[propext, Classical.choice, Quot.sound]` |
| isolated temporary-olean trust-zero replay of `Statement.lean`, `ObligationTree.lean`, and `ProofBoundary.lean` | 0 | exact statement, conditional composition, and empty-source case elaborated; both proof axiom reports exactly `[propext, Classical.choice, Quot.sound]` |
| isolated exact-context proof attempt through `exists_embedding_euclidean_of_compact` | 1 | expected failure: Lean could not synthesize `CompactSpace M`; temporary source removed |
| prohibited-construct scan of owned Lean files and the pinned Whitney module | 1 each | expected no-match: no bodyless declaration, `sorry`, `admit`, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney-module endpoint/TODO scan | 0 | unrestricted theorem explicitly TODO; only finite-index immersion and compact-only embedding endpoints exist |
| bounded target, Stage1, and pinned-package declaration search | 0 | no unconditional inhabitant of `WhitneyEmbeddingTarget` was located |
| read-only cached `origin/master` Whitney-module check | 0 | cached commit `4efb186f...` retains the TODO and restricted endpoints; it receives no proof credit |
| Hausdorff-dimension and smooth-proper-exhaustion search | 0 | two range-dimension lemmas exist, but no manifold-level smooth proper-exhaustion endpoint was found |
| source/environment hashes and repository/mathlib revision-tree checks | 0 | all recorded identities matched |
| `python3 -m json.tool` on the paired blocker JSON | 0 | structured current-base blocker artifact parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0594` | 0 | no whitespace errors in owned changes |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the assigned proof phase is blocked |

The isolated dependent-module recipe generated no repository object file:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0594
tmp=$(mktemp -d /tmp/thm-m-0594-slot27-proof-a60b47b4.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/ProofBoundary.lean" "$tmp/ProofBoundary.lean"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout --foreground 300 "$lean" \
  --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout --foreground 300 "$lean" \
  --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout --foreground 300 "$lean" \
  --trust=0 -t0 -R "$tmp" "$tmp/ProofBoundary.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Exact source hashes and the structured command ledger are in the paired JSON.

## Retry Condition

Resume proof execution only after implementing the frozen inhabited
noncompact weak-Whitney construction with checked child-to-parent
composition, or after placing an immutable, license-compatible proof of the
exact unrestricted target into the pinned repository-local dependency
closure. A compact-only theorem, empty-source case, infinite-dimensional
topological embedding, or conditional witness constructor is not a
substitute.

Status boundary: this is fresh current-base nonrelease blocker evidence, not a
positive proof receipt. It does not satisfy `S56-M-0594-PROOF`, propose a
scheduler-state transition, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
