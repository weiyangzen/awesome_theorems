# THM-M-0579 proof-phase recheck at base 4e632139

Item: `S56-M-0579-PROOF`  
Intent: `prove`  
Recheck date: 2026-07-14 (Asia/Shanghai)  
Base revision: `4e632139f5060edf088cd107551caac63981263b`  
Base tree: `7a87a6b3f6b71cfb0b2d98872327edc8fe8620e6`

## Verdict

`blocked`. No eligible retained Lean 4 proof body exists in the pinned closure
for the exact frozen proposition `Stage1Instances.THMM0579.Statement`. No proof
source was added. The proof item remains `[ ]`, the lifecycle remains `planned`,
the root vector remains `[H3, M3, R4]`, and neither the audit nor the theorem is
complete.

The first failed gate is terminal proof-body availability. The frozen immediate
root cut is `M0579-T-RECOGNITION` plus `M0579-T-RIGIDITY`; neither has a proof
body. Seven intended recognition dependencies are currently only planned prose
targets in the typed graph, not Lean propositions with checked compositions.
The local `root_of_recognition_and_rigidity` theorem consumes both broad
packages as premises and therefore does not close the root.

A disposable trust-zero probe additionally proves
`Statement.{u} ↔ HomotopySphereRecognition.{u} ∧
HomotopySphereTopologicalRigidity.{u}`. A root homeomorphism yields recognition
via `Homeomorph.toHomotopyEquiv` and yields rigidity by ignoring its extra
homotopy premise; the converse is the existing composition. Thus the frozen cut
is logically equivalent to the root and is not a difficulty-reducing proof
decomposition. A meaningful package implementation first requires the
obligation-tree authority, not this proof worker, to publish an append-only
registry revision with executable terminal contracts.

Pinned mathlib contains the matching names only as Batteries `proof_wanted`
source markers, elaborated under `withoutModifyingEnv` and then discarded.
The trust-zero probe reports all three matching names as `Unknown constant`.
A scoped retained-declaration search found no alternate body in the owned
instances, legacy Stage1 sources, mathlib, or Batteries. The immutable external
candidates already frozen in `anchor-audit.json` offer either a 3D statement
with an unrelated dimension-zero proof or an explicit `sorry`; neither is
eligible to pin or import.

## Validation

All commands ran in this worker clone. Lean outputs were written only to a
disposable `/tmp` directory and removed. The automation-provided untracked
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0579` | 0 | rank 114; planned; hard-mathlib lane; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0579/check_obligation_tree.py` | 0 | 16 obligations and 34 typed edges passed; denominator `984bcfffcea5afa7c11e3f2eb78ad31c2eed6b99e1a0913496186ceb1595776f`; root M3 and both cut packages M4 |
| `python3 Stage1_Instances/THM-M-0579/check_anchor_audit.py` | 0 | frozen target, five candidates, discarded `proof_wanted` boundary, dependency pins, and noncompletion status agree |
| isolated `lake env lean --trust=0` replay | 0 | `Statement.lean` and `ObligationTree.lean` elaborated; conditional composition axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| disposable trust-zero cut-equivalence and absence probe | 0 | cut/root equivalence elaborated with the same three axioms; all matching mathlib names were `Unknown constant` |
| forbidden-construct scan of checked owned Lean sources | 1 | expected no match for `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` |
| exact retained-declaration search | 1 | expected no matching sphere-three theorem, lemma, definition, opaque declaration, or abbreviation |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned dependency revision checks | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`); Batteries `756e3321fd3b02a85ffda19fef789916223e578c` |
| `python3 -m json.tool Stage1_Instances/THM-M-0579/proof-recheck-2026-07-14-head-4e632139.json >/dev/null` | 0 | blocker record is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0579` | 0 | no whitespace errors in owned changes |

The isolated elaboration recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0579
tmp=$(mktemp -d /tmp/thm-m-0579-current-probe.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" --trust=0 -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 ProofAvailabilityProbe.lean
```

`ProofAvailabilityProbe.lean` was created in the owned directory for this
command and removed immediately after the successful run, leaving no source or
compiled output behind. Its exact contents were:

```lean
import ObligationTree

noncomputable section

universe u

namespace Stage1Instances.THMM0579

open ContinuousMap

theorem proofAvailabilityProbe_cut_iff_root :
    Statement.{u} ↔
      HomotopySphereRecognition.{u} ∧
        HomotopySphereTopologicalRigidity.{u} := by
  constructor
  · intro root
    constructor
    · intro M _ _ _ _ _
      rcases root M with ⟨homeomorph⟩
      exact ⟨homeomorph.toHomotopyEquiv⟩
    · intro M _ _ _ _ _ _
      exact root M
  · rintro ⟨recognition, rigidity⟩
    exact root_of_recognition_and_rigidity recognition rigidity

#print axioms proofAvailabilityProbe_cut_iff_root

#check_failure ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere
#check_failure SimplyConnectedSpace.nonempty_homeomorph_sphere_three
#check_failure SimplyConnectedSpace.nonempty_diffeomorph_sphere_three

end Stage1Instances.THMM0579
```

The exact negative scan commands were:

```bash
rg -n --pcre2 '\b(sorry|admit|axiom|sorryAx|unsafe|implemented_by|native_decide|external)\b' \
  Stage1_Instances/THM-M-0579/{Statement.lean,AnchorAudit.lean,ObligationTree.lean}

rg -n --pcre2 \
  '^(?:public\s+)?(?:theorem|lemma|def|opaque|abbrev)\s+(?:[A-Za-z0-9_]+\.)*(?:nonempty_homeomorph_sphere_three|nonempty_diffeomorph_sphere_three|nonempty_homeomorph_sphere)(?:\s|\[|:)' \
  Stage1_Instances Formalizations/Lean/AwesomeTheorems \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib \
  Formalizations/Lean/.lake/packages/batteries/Batteries
```

Both returned exit 1, ripgrep's no-match status. The three `#check_failure`
commands reported:

```text
ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere
SimplyConnectedSpace.nonempty_homeomorph_sphere_three
SimplyConnectedSpace.nonempty_diffeomorph_sphere_three
```

Proof-relevant source hashes were unchanged:

```text
Statement.lean              307061f5847f145fb8cb4e91116ed8ab0c76e3ddc0e9301486fd879be1cf3de8
ObligationTree.lean         f5214263374c23fd2f235cdf4d06bc9cadfd50d4abbe41de32dd55a7e35f0c63
obligation-registry.json    8b70a187e8d4e071c3a658f8b5d8d31fb78dcb2fabc1bedeeddca3fd4c62b31a
typed-graphs.json           e8a756448de68ee250734fc480a06bd3fc55f1827f6da5a847b6bd31677ddce7
anchor-audit.json           0285a80d4d59466d71fdd1d163e1c6a09f7a96b1d0372ea8f682fd69c251f7e7
validation-specs.json       353bdfdcd8341bb9bbd3b3c324b634804144b119ed0b8d0ed161e28d222074aa
```

## Retry Condition

First publish a versioned, non-tautological, executable obligation-tree
revision. Then resume after its terminal packages are implemented without
placeholders, or after discovery of a licensed immutable Lean 4 proof with a
compatible dependency lock and exact checked transport to the canonical root.
The result must pass kernel, exact-type, composition, axiom, placeholder,
provenance, trust, and pinned-replay gates. Assuming a package, treating
`proof_wanted` as a theorem, or proving a conditional/special case would
substitute a different theorem.

This owned artifact is a blocker record, not a proof receipt. It does not
satisfy `S56-M-0579-PROOF`, propose scheduler state, or claim audit completion,
theorem completion, release, or master acceptance. Because the positive proof
phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
