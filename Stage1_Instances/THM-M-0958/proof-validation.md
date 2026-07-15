# THM-M-0958 proof-phase validation

Item: `S56-M-0958-PROOF`

Base revision: `435748c4550bad6c03c34931d309befe9658460d`

Base tree: `5354633764fc606c80fe66838d43b491165ea056`

## Implemented bodies

`Proof.lean` contains nine local, placeholder-free declarations making partial
progress toward `M0958-C-DIGIT-EMBED`, `M0958-L-DIGIT-INJECTIVE`,
`M0958-L-NO-CARRY`, `M0958-L-PROGRESSION-FREE`, and
`M0958-L-EMBED-RANGE`. They establish:

- injectivity of pinned `Behrend.map (2 * y)` on coordinate digits below `y`;
- the no-carry lift of image progression equations to coordinatewise sums;
- preservation of `ThreeAPFree` and cardinality by the radix image;
- the geometric-sum range bound below `(2 * y) ^ k`;
- containment, cardinality, and progression-freeness after shifting into the
  exact one-based interval `Ico 1 (n + 1)`; and
- a typed local subpackage composition returning the finite-set embedding from
  explicit digit, positivity, fit, and vector-freeness inputs; it is not a
  certificate closing the broader frozen parent.

These are genuine exact Lean bodies, but the frozen nodes are broader planned
packages and lack exact statement fingerprints. Therefore zero frozen obligations are claimed closed.
The proof does not construct the large convexly independent vector set or
prove the Elkin-scale cardinality estimate.

## Boundary

The frozen minimal machine root cut remains `M0958-T-WITNESS`. A selected
critical external blocker is `M0958-X-DISCREPANCY-BASE`: Elkin's route imports
a five-dimensional rotated-lattice discrepancy theorem, but neither the
repository nor pinned mathlib contains its exact placeholder-free Lean body.
The concentration, annulus, exterior subset, growing-dimensional discrepancy,
floor, and asymptotic packages also remain open. The conditional root harness
consumes the missing witness and cannot replace it; pinned
`Behrend.roth_lower_bound` has a strictly weaker scale.

The provisional root vector remains `[H1, M3, R4]`;
`root_kernel_closed=false`, `theorem_complete=false`, and this handoff is not theorem completion.

## Commands and exact results

All Lean commands used the existing canonical pinned `.lake` artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed. The proof checker creates all `.olean` and log files under a
temporary `/tmp/stage1-m0958-proof.*` directory and removes it on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0958` | 0 | Rank 1492, planned, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0958/build_obligation_artifacts.py --check` | 0 | Frozen generated registry, seven graph families, and readable projection agree: 64 obligations, 85 typed edges, denominator `a6628059...383e5b`. |
| `python3 Stage1_Instances/THM-M-0958/check_obligation_tree.py` | 1 | Expected predecessor-evidence failure at its hard-coded base-revision assertion (`4a10a7a4...` versus current `435748c4...`); no Lean check was reached and no proof credit is claimed. |
| `rg -n --glob '*.lean' --glob '*.json' --glob '*.md' '(ElkinConstructionTarget\|WitnessConstructionTarget\|Elkin\|elkinScale\|0801\.4310)' Stage1_Instances Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Bounded local recheck found the exact target only in this dossier and historical evidence; pinned mathlib hits remain Behrend support, not an exact Elkin body. This is not a global absence claim. |
| `bash Stage1_Instances/THM-M-0958/check_proof.sh` | 0 | Isolated `Statement -> Proof` elaboration with `--trust=0`; nine exact axiom reports were present and used only `propext`, `Classical.choice`, and `Quot.sound`; source, receipt, scope, hashes, pin, and open-root checks passed. |
| `rg -n '\b(sorry\|admit\|sorryAx\|implemented_by\|native_decide\|proof_wanted)\b\|^[[:space:]]*\(axiom\|constant\|opaque\|unsafe\|extern\)[[:space:]]' Stage1_Instances/THM-M-0958/Proof.lean` | 1 | Expected no-match exit; no prohibited proof device occurs. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-0958 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The automation-provided untracked `Formalizations/Lean/.lake` symlink existed
before this work and was not modified. This is dirty-tree, nonrelease worker
evidence pending integration-lane review and master acceptance.

## Known predecessor boundary

`check_obligation_tree.py` hard-codes the historical obligation-tree base
revision `4a10a7a4...`; it exits at that stale-revision assertion on the current
base `435748c4...`. The deterministic builder check above passes. This proof
phase does not rewrite predecessor-owned evidence or count the stale checker
as proof validation.
