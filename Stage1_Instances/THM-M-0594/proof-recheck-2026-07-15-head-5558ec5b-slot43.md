# THM-M-0594 proof recheck at 5558ec5b (slot43)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T07:16:41+08:00

Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

Base tree: `f17ce1a24cd65800f536301fdb66a12e18ef3ae3`

## Verdict

`blocked`. The recorded bounded searches located no placeholder-free proof
body for the exact unrestricted `WhitneyEmbeddingTarget` in the pinned Lean
closure. This attempt does not add
compactness, weaken the conclusion, or credit a conditional witness
constructor as the theorem. The proof item remains `[ ]`, lifecycle remains
`planned`, and the root remains `[H1, M3, R3]`. No receipt acceptance,
validation, release, audit completion, or theorem completion is claimed.
Because the positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The frozen target covers every finite-dimensional, Hausdorff,
second-countable, boundaryless smooth real manifold. It requires one map into
some finite-dimensional Euclidean space that is globally smooth, is a
topological embedding, and has injective manifold derivative everywhere. It
has neither a `CompactSpace` premise nor a fixed target-dimension bound.

## First failed gate

`M0594-C-GLOBAL` remains open: no located local or pinned terminal body constructs one
finite Euclidean tuple with injective derivative, global point separation,
and properness for the general, possibly noncompact manifold. The immediate
frozen root cut set remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

`ProofSupport.lean` derives a compact exhaustion, a locally finite smooth bump
covering, and the abstract proper-injective topological endpoint.
`ObligationTree.lean` checks root assembly from an already supplied smooth
embedding witness. These are genuine checked interfaces, but none constructs
the finite witness required by the root. The frozen map-specific
`M0594-L-TOPOLOGICAL` node therefore remains M4 despite the checked generic
endpoint; this proof recheck does not rewrite the accepted graph status.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite cover index. `SmoothBumpCovering.fintype` and
`exists_embedding_euclidean_of_compact` require `CompactSpace M`. A direct
trust-zero probe under the exact target assumptions failed specifically
because Lean could not synthesize `CompactSpace M`. The pinned Whitney module
explicitly leaves the sigma-compact weak theorem as a TODO requiring Sard and
Hausdorff-dimension machinery. Read-only inspection of cached
`origin/master` at `4efb186f102ebfd2eea1545c151d6fbcfdff0e43` found the
same TODO and compact-only endpoint; that non-pinned ref receives no proof
credit.

A bounded supplemental network search on 2026-07-15 used Sourcegraph and
GitHub for candidate discovery only. It located only compact mathlib artifacts
and `leanprover/lean-eval` PR 353, whose candidate body is explicitly
`by sorry`; that prohibited evaluation artifact receives no proof credit. No
network access was used for Lean validation or dependency acquisition.

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
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/ProofSupport.lean` | 0 | all three support bodies elaborated; axiom reports were exactly `[propext, Classical.choice, Quot.sound]`; type probes exposed the finite-index/compactness boundary |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/AnchorAudit.lean` | 0 | compact-only wrapper elaborated; its axiom report was exactly `[propext, Classical.choice, Quot.sound]` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact target and conditional root composition elaborated; composition axioms were exactly `[propext, Classical.choice, Quot.sound]`; no repository object was emitted |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| prohibited-construct scan of owned Lean files | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| prohibited-construct scan of pinned Whitney source | 1 | expected no-match |
| pinned Whitney-module endpoint/TODO scan | 0 | only finite-index immersion and compact-only embedding endpoints; unrestricted theorem explicitly TODO |
| bounded repository and installed-package declaration search | 0 | only the exact statement, compact wrappers, support references, and restricted pinned endpoints were located |
| exact-context compact-wrapper probe | 1 | expected failure: Lean could not synthesize `CompactSpace M`; the temporary probe was removed |
| cached `origin/master` Whitney source inspection | 0 | cached head `4efb186f...` retained the same TODO and compact-only endpoint; it receives no proof credit |
| bounded Sourcegraph/GitHub supplemental search | n/a | only compact mathlib artifacts and a prohibited `by sorry` lean-eval candidate were located; no dependency was fetched |
| blocker JSON parse, fresh-artifact whitespace checks, obligation recheck, and self-test absence check | 0 | JSON valid; no whitespace diagnostics; frozen tree still passed; positive self-test manifest absent |

The isolated composition recipe generated no repository object file:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0594
tmp=$(mktemp -d /tmp/thm-m-0594-slot43-proof.XXXXXX)
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

Resume proof execution only after implementing the frozen weak Whitney
construction for the general, possibly noncompact target with checked
child-to-parent composition, or after
placing an immutable, license-compatible proof of the exact unrestricted
target into the pinned repository-local dependency closure. A compact-only
theorem, infinite-dimensional topological embedding, or conditional witness
constructor is not a substitute.

Status boundary: this is current-base nonrelease blocker evidence, not a
positive proof receipt. It does not satisfy `S56-M-0594-PROOF`, propose a
scheduler-state transition, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
