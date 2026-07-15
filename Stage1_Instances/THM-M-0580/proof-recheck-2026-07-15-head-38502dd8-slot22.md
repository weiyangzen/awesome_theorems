# THM-M-0580 Proof Recheck: Blocked on Current Base

## Scope and Verdict

This is proof-phase evidence for `S56-M-0580-PROOF` at base
`38502dd8cfdb1c7b89d62d802952ab596838ec7e` (tree
`334fd05726c0b982153d6aec154745629a2c9bc1`). The exact target is
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`, expression SHA-256
`938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`.

The attempt is blocked. The target-local task authority has `accepted_states=[]` and records
`S56-M-0580-OBLIGATION_TREE` as open, so this proof item is not dependency-legal for acceptance.
The generated checklist's `[_]` prerequisite marker is provisional and does not override that
structured state.

Independently, the root cut set remains `M0580-N-SMOOTH` and
`M0580-T-SMOOTH-POINCARE`. Neither has an eligible terminal body. The checked local theorem
`root_of_smoothing_and_smooth_poincare` is conditional on both packages and therefore cannot close
the root.

The current smoothing proposition requires `IsManifold` for an already selected `ChartedSpace`;
it does not construct replacement smooth-atlas data or a compatibility bridge. The smooth package
concludes the same homeomorphism as the root under an extra `IsManifold` instance, and
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` checks that the root itself implies this
package. Treating that consequence as an independent root premise would be circular. The Ricci-flow,
surgery, extinction, decomposition, and fundamental-group children still have planned fingerprints
rather than exact Lean propositions and own no terminal proof bodies.

Pinned mathlib contains the generalized, topological-three, and smooth-three signatures only as
`proof_wanted` commands. Batteries elaborates these inside `withoutModifyingEnv` and discards them;
the trust-zero probe confirms all three names are unknown after import. Scoped retained-declaration
searches found no exact-root or cut-set body elsewhere in the repository or pinned package closure.
The immutable external audit likewise contains no dimension-three proof body.

No proof body or receipt was added. The item remains `[ ]`, lifecycle remains `planned`, the root
vector remains `[H2, M4, R4]`, and audit completion, root closure, and theorem completion remain
false.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean output was confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; L0/rework-required; theorem incomplete |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four statement mutations killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 0 | exact statement anchors are bodyless; immutable external root is statement-only; root remains M4 |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axioms were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| target-local prerequisite-state assertion | 0 | `accepted_states=[]`; `S56-M-0580-OBLIGATION_TREE=open` |
| retained-declaration scan plus pinned source inspection | 0 | no theorem, lemma, or opaque declaration for any relevant name; exactly three matching mathlib entries are discarded `proof_wanted` commands |
| inverted prohibited-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned dependency revision/tree and clean-tree probes | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` / tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Batteries `756e3321fd3b02a85ffda19fef789916223e578c` / tree `02666252fd943c970ee0b7a66ec65a2e5efe7230`; both clean |

The narrow Lean validation used the pinned toolchain and existing compiled artifacts:

```bash
set -euo pipefail
repo=$PWD
lean_root="$repo/Formalizations/Lean"
target="$repo/Stage1_Instances/THM-M-0580"
tmp=$(mktemp -d /tmp/thm-m-0580-proof-38502dd8-slot22.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do paths+=("$p"); done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 ProofBlockerProbe.lean
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

There were 44 earlier structured `proof-recheck` packets before this attempt. The rev-5.6 five-tick
rule therefore requires the master to split this oversized root proof item into dependency-legal
child tasks rather than reschedule the unchanged item. This proof worker cannot edit the DAG.

This is an owned blocker packet, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`,
propose a state promotion, or support theorem completion. Because the assigned proof phase is not
genuinely complete, `.stage1-worker-selftest.json` remains absent.
