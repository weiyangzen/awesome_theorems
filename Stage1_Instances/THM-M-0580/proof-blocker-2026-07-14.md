# THM-M-0580 proof-phase recheck: blocked

Item: `S56-M-0580-PROOF`  
Attempt: `2026-07-14T01:02:10+08:00`  
Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`  
Base tree: `da6f991c07f11e8608ddc090af9356558d64d360`

## Verdict

`blocked`: this execution found no eligible proof body for the exact target
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No Lean source or proof receipt was added,
and the root debt remains `[H2, M4, R4]`. The proof phase, audit, root, and theorem are not
complete.

The frozen immediate cut set is still:

- `M0580-N-SMOOTH`, compatible smoothing for the fixed topological three-manifold context;
- `M0580-T-SMOOTH-POINCARE`, the full smooth three-dimensional Poincare package.

The second package expands through metric construction, short-time Ricci flow, noncollapsing,
canonical neighborhoods, surgery construction and existence, finite extinction, decomposition,
and fundamental-group elimination. The local theorem
`root_of_smoothing_and_smooth_poincare` checks only their conditional composition into the exact
root. It consumes both packages as premises and constructs neither, so it supplies no root proof
credit.

Pinned mathlib contains the matching topological and smooth signatures only as `proof_wanted`
source markers. A direct Lean probe reports both names as unknown constants; there is no retained
declaration to import. Repository and pinned-dependency searches found only statement surfaces,
audit constants, adjacent infrastructure, and conditional wrappers. The prerequisite immutable
external audit likewise found a dimension-three statement and an unrelated dimension-zero proof,
not a terminal proof of the exact target.

## Validation

All commands ran in this worker clone. The narrow composition check wrote `Statement.olean` only
inside a disposable `/tmp` directory and removed it with a shell trap. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed. The automation-provided
untracked `.lake` symlink was left unchanged.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | Rank 115; planned; L0/rework-required; theorem incomplete. |
| Isolated pinned Lean recipe below | 0 | The exact statement and conditional composition elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]` and no `sorryAx`. |
| `python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 0, then 1 on repeat | The initial run confirmed bodyless exact anchors, a statement-only external dimension-three root, and root `M4`. A final repeat reached the same pinned local checks but GitHub returned HTTP 403 rate-limit exceeded while replaying the immutable external source; no stronger claim is based on that failed repeat. |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d64...a6d`; smoothing and smooth Perelman packages remain unproved. |
| Direct `lake env lean` checks of both `SimplyConnectedSpace.nonempty_*_sphere_three` names | 1 | Expected negative evidence: both are `Unknown constant`; the pinned source has `proof_wanted` markers at lines 47 and 52 and no theorem declarations. |
| Scoped source search of repo and pinned Lean packages | 0 | No alternate terminal Perelman/Poincare proof body was found; hits were statement and audit surfaces. |
| Scoped forbidden-token scan of `Statement.lean`, `AnchorAudit.lean`, and `ObligationTree.lean` | 0 | No `sorry`, `admit`, `axiom`, `unsafe`, or `sorryAx` token. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The successful isolated elaboration recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" ObligationTree.lean
```

`check_statement.py` was not credited as completed evidence: under concurrent load it exceeded the
bounded execution window while elaborating repeated mutation copies. Its temporary files and
processes were removed, and the previously accepted statement hash remains unchanged.

## Reopen Condition

Resume only after both frozen cut-set packages are implemented without placeholders, or after an
immutable compatible Lean 4 terminal proof with a complete dependency lock and license can be
exact-type transported and checked in the pinned closure. Assuming either package, treating
`proof_wanted` as an axiom, or returning the conditional composition would violate the exact-target
and proof-body gates.

This report is not a proof receipt and does not satisfy `S56-M-0580-PROOF`. Because the assigned
phase is not genuinely complete, `.stage1-worker-selftest.json` remains absent.
