# THM-M-0594 proof recheck at 3af3b6bc (slot28)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T16:56:23+08:00

Base revision: `3af3b6bc58d308bda7dc1cb164a9a258512b8c53`

Base tree: `65dce2e2ba00c806bf25b436c98caf996c1c56d2`

## Verdict

`blocked`. This attempt adds one real, placeholder-free exact-target boundary
proof: `whitneyEmbeddingTarget_of_isEmpty` proves the canonical proposition
when the source type is empty. It chooses target dimension zero and discharges
smoothness, topological embedding, and derivative injectivity without changing
the canonical statement.

This theorem does not close any frozen proof-graph obligation: the unrestricted
inhabited/noncompact construction is still absent. The proof item remains
`[ ]`, lifecycle remains `planned`, and the root remains `[H1, M3, R3]`. No
receipt acceptance, validation, release, audit completion, or theorem
completion is claimed. Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## First failed gate

`M0594-C-GLOBAL` remains open: no local or pinned terminal body constructs one
finite Euclidean tuple with injective derivative, global point separation, and
properness on an arbitrary inhabited noncompact manifold. The frozen immediate
root cut set remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

`ProofSupport.lean` derives a compact exhaustion, a locally finite smooth bump
covering, and the proper-injective topological endpoint. `ObligationTree.lean`
checks root assembly from an already supplied witness. Pinned mathlib provides
only a finite-index immersion and a compact-manifold embedding; its Whitney
module explicitly leaves the sigma-compact weak theorem as a TODO requiring
Sard/Hausdorff-dimension machinery. The new empty case does not supply those
missing global constructions.

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
| same trust-zero command on `ProofSupport.lean` | 0 | all three support bodies elaborated; axiom reports were exactly `[propext, Classical.choice, Quot.sound]`; probes exposed the finite-index/compactness boundary |
| same trust-zero command on `AnchorAudit.lean` | 0 | compact-only wrapper elaborated; its axiom report was exactly `[propext, Classical.choice, Quot.sound]` |
| direct trust-zero `lake env lean` on `ProofBoundary.lean` before creating a target-local object | 1 | Lean reported unknown module prefix `Statement`; no repository object was created, and the isolated recipe below supplied the required temporary `Statement.olean` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ProofBoundary.lean` | 0 | the exact-target empty-source proof elaborated; its axiom report contained exactly `propext`, `Classical.choice`, and `Quot.sound` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact target and conditional root composition elaborated; composition axioms were exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| prohibited-construct scan of owned Lean files | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney-module endpoint/TODO scan | 0 | only finite-index immersion and compact-only embedding endpoints; unrestricted theorem explicitly TODO |
| scoped repository declaration search | 0 | only exact statement/support declarations, compact wrappers, the new empty case, and restricted pinned endpoints; no unconditional inhabitant was found |

The boundary-proof replay generated no repository object file:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0594
tmp=$(mktemp -d /tmp/thm-m-0594-slot28-boundary.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ProofBoundary.lean" "$tmp/ProofBoundary.lean"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean" \
  --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean" \
  --trust=0 -t0 -R "$tmp" "$tmp/ProofBoundary.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Exact source hashes and the complete command ledger are in the paired JSON.

## Retry condition

Resume proof execution by implementing the frozen inhabited noncompact weak
Whitney construction with checked child-to-parent composition, or by placing
an immutable, license-compatible proof of the exact unrestricted target into
the pinned repository-local dependency closure. A compact-only theorem,
empty-source case, infinite-dimensional topological embedding, or conditional
witness constructor is not a substitute.

Status boundary: this is fresh current-base nonrelease proof-progress and
blocker evidence, not a positive proof receipt. It does not satisfy
`S56-M-0594-PROOF`, propose a scheduler-state transition, or claim audit
completion, theorem completion, validation, release, receipt acceptance, or
master acceptance.
