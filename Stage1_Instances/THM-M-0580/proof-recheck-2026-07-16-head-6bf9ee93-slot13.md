# THM-M-0580 proof-phase recheck at base 6bf9ee93 (slot 13)

Item: `S56-M-0580-PROOF`

Recorded: `2026-07-16T04:55:34+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. No placeholder-free Lean body inhabits the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget` or either member of its
frozen immediate root cut:

- `M0580-N-SMOOTH`, compatible smoothing of the topological three-manifold;
- `M0580-T-SMOOTH-POINCARE`, the complete smooth three-dimensional Poincare
  package.

`root_of_smoothing_and_smooth_poincare` consumes both packages as explicit
premises and checks only their conditional composition. The diagnostic theorem
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` derives the smooth
package from the root, so using it to construct a premise would be circular.

The required dependency ledger records an empty hard-parent, ancestor, edge,
and reuse-hint closure against graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`
and context digest
`cdf6c9f8de36e769dba3868e130e3dbcced7e1e38e0429fb4b3a728c4b787aff`.
The one weak shared-module group was inspected through member `THM-M-0579`.
That target freezes the same topological three-dimensional Poincare statement,
but its proof phase is open and its sources retain only statement encodings,
conditional composition, and blocker probes. The common
`Mathlib.Geometry.Manifold.PoincareConjecture` import therefore supplies no
terminal body or proof credit; the ledger decision is `not_applicable`.

Pinned mathlib contains the generalized, topological-three, and smooth-three
signatures only as `proof_wanted` entries. Batteries elaborates such entries
inside `withoutModifyingEnv` and discards them. The trust-zero probe confirmed
that all three names are unknown after importing the module. Scoped source
searches found no retained exact-root or cut-set declaration.

The frozen prerequisite also needs an append-only correction before its child
packages can receive exact proof credit. `TopologicalThreeManifoldSmoothable`
asks whether an already selected `ChartedSpace` is smooth rather than exposing
compatible replacement-atlas data. `SmoothThreeDimensionalPoincare` concludes
the root homeomorphism under an extra `IsManifold` instance rather than a
diffeomorphism-valued smooth theorem; indeed, the root implies that package.
The Ricci-flow, surgery, extinction, decomposition, and topology children use
planned fingerprints rather than exact Lean propositions and own no bodies.

The rev-5.6 execution DAG records the prerequisite as worker-self-tested `[_]`
and scheduled this proof item as `[ ]`, so provisional exploration is allowed.
The target-local `task-dag.json` still says `planned`, has no accepted states,
and calls both tasks open; that projection drift is a separate repair and is
not used as the first proof-body blocker.

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
| `python3 Docs/tools/check_stage1_standard.py` | 1 | nested v2 validator rejected deterministic regeneration because the required target-owned dependency ledger enters the generated evidence inventory; the checked-in graph itself remains byte-identical to the scheduler-supplied digest |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | rejected deterministic regeneration for the same newly required ledger inventory delta; no graph authority was edited |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; theorem incomplete |
| `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 1 | stopped at the nested v2 deterministic-regeneration failure caused by the required ledger inventory delta |
| inline call to `scripts.stage1_execution_cron.validate_dependency_reuse_ledger` with the exact graph digest and base revision | 0 | schema, empty hard closure, shared decision, graph/context digests, and revision passed |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | canonical expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four structural mutations killed; pinned environment matched |
| `timeout --foreground --kill-after=5s 180s python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 1 | immutable local assertions ran before the external GitHub API replay returned HTTP 403 rate-limit exceeded; no moving network result is credited |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axioms were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| inverted prohibited-construct scan over four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| scoped retained-declaration and source search plus pinned Poincare/Batteries inspection | 0 | no terminal root/cut-set body; matching entries are discarded `proof_wanted` markers |
| `git diff --check` | 0 | no whitespace errors |

The structural failures expose a repository-generic validator defect: the
generator's shared-group discovery correctly excludes
`dependency-reuse-ledger.json`, but its evidence inventory does not. Merely
writing the mandatory target-owned ledger therefore makes deterministic
regeneration disagree with the immutable graph digest that the ledger binds.
This worker may modify only `Stage1_Instances/THM-M-0580`, so it records rather
than repairs that shared-tool inconsistency. The checked-in DAG remains
byte-identical to digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`.

The narrow Lean validation used the pinned toolchain and existing compiled
artifacts:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot13-head6bf9ee93.XXXXXX)
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

Publish and master-accept a corrected append-only obligation architecture,
split the oversized root proof item into stable child tasks, and implement the
exact smoothing and smooth-Poincare packages without placeholders.
Alternatively, integrate an immutable, licensed, compatible exact-root Lean 4
proof with a complete dependency lock, exact-type transport, provenance, and
trust evidence.

There were 56 structured proof-recheck packets before this attempt, already far
beyond the five-tick split threshold. The master should stop rescheduling the
unchanged root and split it; this proof worker may not edit the execution DAG.

This is an owned blocker packet, not a proof receipt. It does not satisfy
`S56-M-0580-PROOF`, propose a state promotion, or support theorem completion.
Because the assigned proof phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
