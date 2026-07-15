# THM-M-0580 proof-phase recheck at base 6e4ae3c (slot 8)

Item: `S56-M-0580-PROOF`

Recorded: `2026-07-15T23:45:04+08:00`

Base revision: `6e4ae3c23df4f67f3ebeaa9bfbc9832dbf4a1960`

Base tree: `8e5faba2ff38444d318513ef1d90fe4fc72e12a5`

## Verdict

`blocked`. Proof execution is not dependency-legal. The target-local state
authority remains `planned`, has `accepted_states: []`, and records both
`S56-M-0580-OBLIGATION_TREE` and `S56-M-0580-PROOF` as `open`. The generated
blueprint's `[_]` marker for the prerequisite is provisional worker output,
not master acceptance.

Independently, this base contains no eligible terminal Lean 4 body for the
exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. Its immediate frozen root
cut remains:

- `M0580-N-SMOOTH`, compatible smoothing of the topological manifold;
- `M0580-T-SMOOTH-POINCARE`, the complete smooth three-dimensional Poincare
  package.

`root_of_smoothing_and_smooth_poincare` consumes both packages as premises and
checks only their conditional composition. The diagnostic theorem
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` derives the smooth
package from the exact root, so using it to construct a premise for that root
would be circular.

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
candidate restates dimension three but proves only an unrelated
dimension-zero generalized case.

No proof body or proof receipt was added. The item remains `[ ]`, lifecycle
remains `planned`, the root vector remains `[H2, M4, R4]`, and
`audit_complete`, `root_closed`, and `theorem_complete` remain false.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink and pinned compiled artifacts were reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs were confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git status --short --untracked-files=all`; `git rev-parse HEAD HEAD^{tree}` | 0 | base `6e4ae3c23df4f67f3ebeaa9bfbc9832dbf4a1960`; tree `8e5faba2ff38444d318513ef1d90fe4fc72e12a5`; only the pre-existing automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; L0/rework-required; theorem incomplete |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four mutations killed; pinned toolchain and mathlib revision matched |
| `timeout --foreground --kill-after=5s 180s python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 0 | exact statement anchors are bodyless; immutable external root is statement-only; root remains M4 |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axioms were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| inverted prohibited-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| scoped retained-declaration and source search | 0 | no terminal exact-root or cut-set body; matching mathlib entries are discarded `proof_wanted` markers; local matches are statement surfaces, strings, or negative probes |
| target-local state-authority assertion | 0 | lifecycle `planned`, `accepted_states=[]`, prerequisite and proof tasks both `open` |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 60s lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned dependency revision/tree and clean-tree probes | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` / tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Batteries `756e3321fd3b02a85ffda19fef789916223e578c` / tree `02666252fd943c970ee0b7a66ec65a2e5efe7230`; both tracked package trees clean |

The narrow Lean validation used the pinned toolchain and existing artifacts:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot8-head6e4ae3c.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do
  paths+=("$p")
done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  ProofBlockerProbe.lean
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

There were 53 structured `proof-recheck` packets before this attempt. This far
exceeds the rev-5.6 five-tick split threshold. The master must stop rescheduling
the unchanged root and split it; this proof worker may not edit the DAG.

This is an owned blocker packet, not a proof receipt. It does not satisfy
`S56-M-0580-PROOF`, propose a state promotion, or support theorem completion.
Because the assigned proof phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
