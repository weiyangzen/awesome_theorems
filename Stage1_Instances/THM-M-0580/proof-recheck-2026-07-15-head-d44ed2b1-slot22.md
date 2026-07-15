# THM-M-0580 Proof Recheck: Blocked on Current Base

## Scope and Verdict

This is proof-phase evidence for `S56-M-0580-PROOF` at base
`d44ed2b11fb201a761afad9b133caa8bc97fd710` (tree
`9602084a1c32fa6685f1c60eff540528226decff`). The exact target is
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`, expression SHA-256
`938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`.

The attempt is `blocked`. The target-local task authority has `accepted_states=[]` and records
`S56-M-0580-OBLIGATION_TREE` as open, so this proof item cannot be master-accepted dependency-
legally. The generated checklist's `[_]` prerequisite marker permits provisional preparation only;
it does not override structured target state.

Independently, the immediate root cut set remains `M0580-N-SMOOTH` and
`M0580-T-SMOOTH-POINCARE`. Neither has an eligible terminal body. The local theorem
`root_of_smoothing_and_smooth_poincare` is checked conditional composition: it assumes both open
packages and therefore supplies no root proof body.

The current smoothing proposition asks for `IsManifold` under an already selected `ChartedSpace`;
it neither constructs replacement smooth-atlas data nor states a compatibility bridge. The smooth
package returns the root homeomorphism after adding an `IsManifold` instance, and the diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` checks that the root itself implies this
package. Using that consequence as an independent root premise would be circular. The Ricci-flow,
surgery, extinction, decomposition, and fundamental-group children still have planned
fingerprints rather than exact Lean propositions and own no terminal proof bodies.

Pinned mathlib contains the generalized, topological-three, and smooth-three signatures only as
`proof_wanted` commands. Batteries elaborates these inside `withoutModifyingEnv` and discards them;
the trust-zero probe confirms all three constants are unknown after import. Scoped repository,
legacy, dependency-source, and git-history searches found no exact-root or cut-set body. The
immutable prerequisite external audit likewise records no dimension-three proof body.

No proof body or completion receipt was added. The item remains `[ ]`, lifecycle remains `planned`,
the root vector remains `[H2, M4, R4]`, and `audit_complete`, root closure, and theorem completion
remain false.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean output was confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; L0/rework-required; theorem incomplete |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 matched; all four structural mutations were killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axioms were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| `python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 1 | local and pinned assertions passed before the sole remote GitHub API replay failed with HTTP 403 rate limit; no anchor success was inferred |
| target-local prerequisite-state assertion | 0 | `accepted_states=[]`; `S56-M-0580-OBLIGATION_TREE=open` |
| retained-declaration and history searches | 0 | no exact-root or cut-set body; matching mathlib entries are discarded `proof_wanted` commands; no target `Proof.lean` exists in local history |
| inverted prohibited-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned dependency revision/tree and clean-tree probes | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` / tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Batteries `756e3321fd3b02a85ffda19fef789916223e578c` / tree `02666252fd943c970ee0b7a66ec65a2e5efe7230`; both clean |
| `jq empty ...slot22.json` plus blocker-invariant assertions | 0 | JSON parsed; item/base/outcome/open-state/noncompletion fields, changed paths, and recorded HTTP 403 failure agreed |
| `git diff --check -- ...slot22.{json,md}` | 0 | no whitespace errors |
| scoped worktree and self-test assertions | 0 | only these two owned artifacts changed apart from the pre-existing canonical `.lake` symlink; `.stage1-worker-selftest.json` is absent |

The narrow Lean validation used the pinned toolchain and existing compiled artifacts:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot22-headd44ed2b1.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do paths+=("$p"); done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 ProofBlockerProbe.lean
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean"
```

Temporary olean SHA-256 values were
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` for
`Statement.olean` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8` for
`ObligationTree.olean`.

## Retry Condition

First reconcile and master-accept the prerequisite state. Then publish an append-only obligation-
tree revision with compatible replacement-atlas smoothing data, faithful smooth-Poincare semantics,
exact Lean targets for every proof child, checked composition, and declaration-covering validation
recipes. Implement those corrected packages without placeholders. Alternatively, integrate an
immutable, licensed, compatible exact-root Lean 4 proof with a complete dependency lock and exact-
type, provenance, and trust checks.

There were 45 earlier structured `proof-recheck` packets before this attempt. The rev-5.6 five-tick
rule therefore requires the master to split this oversized root proof item into dependency-legal
child tasks rather than reschedule the unchanged item. This proof worker cannot edit the DAG.

This is an owned blocker packet, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`,
propose a state promotion, or support theorem completion. Because the assigned proof phase is not
genuinely complete, `.stage1-worker-selftest.json` remains absent.
