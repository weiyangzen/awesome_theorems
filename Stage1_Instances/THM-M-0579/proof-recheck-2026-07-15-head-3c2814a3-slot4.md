# THM-M-0579 proof-phase recheck at base 3c2814a3

Item: `S56-M-0579-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `3c2814a370c2fee02158ca79aa44a48e411c4d18`

Base tree: `e1bd7e27bd922b779322c089410a471b6a1535f0`

## Verdict

`blocked`. The canonical proposition
`Stage1Instances.THMM0579.Statement` is the full topological
three-dimensional Poincare theorem. Neither this repository nor the pinned
Lean dependency closure contains a retained, placeholder-free proof body for
it. This attempt adds no proof body. The item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H3, M3, R4]`, and audit and theorem
completion remain false. Because the requested proof phase is not complete,
`.stage1-worker-selftest.json` is intentionally absent.

The first failed gate is terminal proof-body availability. The frozen minimal
root cut is `M0579-T-RECOGNITION` plus `M0579-T-RIGIDITY`, both at `M4`.
`root_of_recognition_and_rigidity` consumes those packages as premises but
does not prove either. The trust-zero blocker probe establishes

```text
(HomotopySphereRecognition and HomotopySphereTopologicalRigidity) iff Statement
```

so this immediate cut is equivalent to the unproved root rather than a
difficulty-reducing proof decomposition. Recognition still expands through
open smoothing, prime-normalization, Ricci-flow, surgery-control, analytic,
finite-extinction, and recomposition packages. Those ingredients are planned
interfaces rather than implemented proof bodies.

Pinned mathlib contains the matching generalized, topological-three, and
smooth-three signatures only as Batteries `proof_wanted` source markers.
`proof_wanted` elaborates its temporary helper under `withoutModifyingEnv`, so
it retains no theorem. `ProofBlockerProbe.lean` checks all three names with
`#check_failure`; each reports `Unknown constant`. The bounded retained-name
search found no replacement theorem in the owned dossier, repository Lean
source, pinned mathlib, or pinned Batteries. The audited immutable external
candidates are statement-only, incomplete with placeholders, or explicitly
contain `sorry`, so none is an eligible import.

## Validation

All Lean commands used the automation-provided canonical `.lake` symlink and
existing pinned artifacts read-only. Disposable `.olean` outputs were written
under `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, checkout, or `.lake` mutation was performed. This is warm-cache,
nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0579` | 0 | Rank 114; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` | 0 | Before this record, only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `python3 Stage1_Instances/THM-M-0579/check_obligation_tree.py` | 0 | 16 obligations and 34 typed edges passed; denominator `984bcfffcea5afa7c11e3f2eb78ad31c2eed6b99e1a0913496186ceb1595776f`; root M3 and both cut packages M4 |
| `python3 Stage1_Instances/THM-M-0579/check_anchor_audit.py` | 0 | Frozen target, five candidates, discarded `proof_wanted` boundary, dependency pins, and noncompletion status agreed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| Isolated `lake env lean --trust=0` replay | 0 | `Statement.lean`, `AnchorAudit.lean`, `ObligationTree.lean`, and `ProofBlockerProbe.lean` elaborated against existing pinned artifacts; four disposable oleans were removed |
| `#print axioms root_of_recognition_and_rigidity` and `#print axioms immediate_cut_iff_statement` | 0 | Each reported `[propext, Classical.choice, Quot.sound]` |
| Three `#check_failure` probes | 0 | The generalized, topological-three, and smooth-three matching names each reported `Unknown constant` |
| Scoped retained-declaration search | 1 | Expected no-match status across the owned dossier, repository Lean source, pinned mathlib, and pinned Batteries |
| Prohibited-construct scan | 1 | Expected no-match for `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, and `external` in the four checked owned Lean modules |
| Frozen-input diff from `a1a7e939` through current HEAD | 0 | The eight proof inputs plus toolchain and dependency manifest are unchanged |
| Pinned dependency `git status --short` checks | 0 | Both mathlib and Batteries worktrees remained clean |
| `git diff --check` | 0 | No whitespace errors before writing this record |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest absent because this proof item remains blocked |
| `python3 -m json.tool Stage1_Instances/THM-M-0579/proof-recheck-2026-07-15-head-3c2814a3-slot4.json` | 0 | Machine-readable current-base blocker record parsed successfully |
| Target-scoped blocker schema assertion | 0 | Item/base identity, blocked state, noncompletion flags, and owned `changed_paths` passed |
| Trailing-whitespace scan of both new artifacts | 0 | Expected no-match; neither new file has trailing whitespace |

The isolated replay recipe, run from the repository root, was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0579
tmp=$(mktemp -d /tmp/thm-m-0579-proof-slot4-3c2814a3-full.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/AnchorAudit.olean" AnchorAudit.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/ObligationTree.olean" ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/ProofBlockerProbe.olean" ProofBlockerProbe.lean
```

Proof-relevant source hashes for this attempt:

```text
Statement.lean              307061f5847f145fb8cb4e91116ed8ab0c76e3ddc0e9301486fd879be1cf3de8
AnchorAudit.lean            40a767ff49b55bcbfccc9455cec77ae7878476b64b0cecd36dfe639fb2c3550f
ObligationTree.lean         f5214263374c23fd2f235cdf4d06bc9cadfd50d4abbe41de32dd55a7e35f0c63
ProofBlockerProbe.lean      e4bc1b79c8e1525b8bf8f7f8edceeb95be6cd95251aa1e69f6052b32618541a3
obligation-registry.json    8b70a187e8d4e071c3a658f8b5d8d31fb78dcb2fabc1bedeeddca3fd4c62b31a
typed-graphs.json           e8a756448de68ee250734fc480a06bd3fc55f1827f6da5a847b6bd31677ddce7
anchor-audit.json           0285a80d4d59466d71fdd1d163e1c6a09f7a96b1d0372ea8f682fd69c251f7e7
validation-specs.json       353bdfdcd8341bb9bbd3b3c324b634804144b119ed0b8d0ed161e28d222074aa
```

Pinned environment identities are mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, Batteries
`756e3321fd3b02a85ffda19fef789916223e578c`, and toolchain
`leanprover/lean4:v4.29.0`.

## Retry Condition

Implement the frozen missing packages locally without placeholders, or
integrate a licensed immutable compatible Lean 4 proof with exact transport
and complete kernel, composition, provenance, axiom, trust, and pinned-replay
evidence. Before route-based implementation, a future obligation-tree revision
should replace the root-equivalent immediate cut and planned-only ingredient
targets with exact, non-tautological executable contracts.

Assuming either package, treating `proof_wanted` as a theorem, importing a
placeholder or statement-only candidate, or proving a conditional or special
case would substitute a different theorem. This owned artifact is blocker
evidence, not a proof receipt. It does not satisfy `S56-M-0579-PROOF`, change
scheduler state, or claim audit completion, theorem completion, release, or
master acceptance.
