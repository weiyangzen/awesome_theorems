# THM-M-0580 proof-phase recheck at base 952a52b7 (slot 8)

Item: `S56-M-0580-PROOF`

Recorded: `2026-07-16T00:38:18+08:00`

Base revision: `952a52b764e12269aeeeccdb678e3e83e1c49ba8`

Base tree: `d024f123bc0a0a408d43b12bb9d0cc3b77c9e522`

## Verdict

`blocked`. Proof execution is not dependency-legal. The target-local state
authority remains `planned`, has `accepted_states: []`, and records both
`S56-M-0580-OBLIGATION_TREE` and `S56-M-0580-PROOF` as `open`. The generated
blueprint's `[_]` prerequisite marker is provisional worker output, not master
acceptance.

Independently, no eligible terminal Lean 4 body exists in this base or its
pinned dependency closure for the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. The immediate frozen root
cut remains:

- `M0580-N-SMOOTH`, compatible smoothing of the fixed topological manifold;
- `M0580-T-SMOOTH-POINCARE`, the complete smooth three-dimensional Poincare
  package.

`root_of_smoothing_and_smooth_poincare` consumes both packages as premises and
checks only their conditional composition. The diagnostic theorem
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` derives the smooth
package from the root, so using it to construct a root premise would be
circular.

The frozen prerequisite also requires append-only correction before child
proof work can receive credit. `TopologicalThreeManifoldSmoothable` checks
`IsManifold` for an already selected `ChartedSpace`; it supplies neither a
replacement atlas nor a compatibility bridge. `SmoothThreeDimensionalPoincare`
concludes the root homeomorphism under an extra `IsManifold` instance rather
than exposing the source diffeomorphism-valued smooth result. Its Ricci-flow,
noncollapse, canonical-neighborhood, surgery, extinction, decomposition, and
fundamental-group children have planned fingerprints rather than exact Lean
propositions and own no terminal proof bodies.

Pinned mathlib contains the generalized, topological-three, and smooth-three
signatures only as `proof_wanted` entries. Batteries elaborates those entries
inside `withoutModifyingEnv` and discards them. The trust-zero probe confirmed
that all three names are unknown after import. Scoped local and pinned-source
searches found no exact-root or cut-set terminal body. The immutable external
candidate recorded by the anchor audit restates dimension three but proves
only an unrelated dimension-zero generalized case.

No proof body or proof receipt was added. The item remains `[ ]`, lifecycle
remains `planned`, the root vector remains `[H2, M4, R4]`, and
`audit_complete`, `root_closed`, and `theorem_complete` remain false.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink and canonical pinned artifacts were reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs were confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git status --short --untracked-files=all`; `git rev-parse HEAD HEAD^{tree}` | 0 | base `952a52b764e12269aeeeccdb678e3e83e1c49ba8`; tree `d024f123bc0a0a408d43b12bb9d0cc3b77c9e522`; only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; L0/rework-required; theorem incomplete |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four structural mutations killed; pinned toolchain and mathlib revision matched |
| `timeout --foreground --kill-after=5s 180s python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 0 | exact statement anchors bodyless; immutable external root statement-only; root M4 |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axioms were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| inverted prohibited-construct scan over four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| scoped retained-declaration and source search plus pinned Poincare/Batteries inspection | 0 | no terminal root/cut-set body in the local or pinned closure; the matching mathlib entries are discarded `proof_wanted` markers |
| target-local state-authority assertion | 0 | lifecycle `planned`, accepted states empty, prerequisite and proof tasks open |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 60s lake env lean --version` plus pinned dependency revision/tree probes | 0 | Lean 4.29.0 commit `98dc76e3`; mathlib `8a178386`/tree `bdc39a31`; Batteries `756e3321`/tree `02666252`; both tracked package trees clean |

The narrow Lean validation used the pinned toolchain and existing compiled
artifacts:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot8-head952a52b7.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
lean_bin=$(cd "$lean_root" && lake env which lean)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 300s "$lean_bin" --trust=0 -t0 \
  --root="$target" -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 300s "$lean_bin" --trust=0 -t0 \
  --root="$target" -o "$tmp/ObligationTree.olean" "$target/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 300s "$lean_bin" --trust=0 -t0 \
  --root="$target" "$target/ProofBlockerProbe.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean"
```

The three Lean invocations exited 0. Temporary olean SHA-256 values were
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6`
for `Statement.olean` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8`
for `ObligationTree.olean`.

## Retry Condition

First publish and master-accept an append-only prerequisite revision with
replacement-atlas smoothing data and compatibility, faithful
diffeomorphism-valued smooth semantics, exact Lean targets for every child,
checked composition, and declaration-covering recipes. Split the oversized
root item into dependency-legal proof children, then implement those corrected
packages without placeholders. Alternatively, integrate an immutable,
licensed, compatible exact-root Lean 4 proof with complete dependency lock,
exact-type, provenance, and trust checks.

There were 55 structured `proof-recheck` packets before this attempt. This far
exceeds the rev-5.6 five-tick split threshold. The master must stop rescheduling
the unchanged root and split it; this proof worker may not edit the DAG.

This is an owned blocker packet, not a proof receipt. It does not satisfy
`S56-M-0580-PROOF`, propose a state promotion, or support theorem completion.
Because the assigned proof phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
