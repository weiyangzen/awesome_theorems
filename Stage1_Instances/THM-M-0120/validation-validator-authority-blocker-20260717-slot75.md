# THM-M-0120 validation validator-authority blocker

## Scope

This is the fail-closed result for `S56-M-0120-VALIDATION` at immutable
worker base `d25efdf450b6236f4750b2eea2cd4f545944d084` (tree
`4674db99ea873d6879a1fa73110c7af3f0884937`). The exact claim tuple is
`(v2_execution_rank=273, phase_layer=5,
phase_item_id=S56-M-0120-VALIDATION)`.

The complete `parent_inspection_order` is empty. It was traversed exactly once
as the complete direct/transitive hard-parent closure. The theorem node also
declares no hard edge, reuse hint, or shared-lemma group. No provider phase
state, receipt, declaration body, reusable artifact, checkbox state,
acceptance, or evidence credit was consumed or transferred. The current graph
SHA-256 is
`441c96e3905667f769f2377a70cff6cfd78835d6a92c3862ce6ccbc3bcf505fe`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_candidate_missing` fails before semantic
validator execution. The HEAD validation contract declares only these
scheduler-owned candidates:

- `Stage1_Instances/THM-M-0120/check_validation.py`
- `Stage1_Instances/THM-M-0120/check_validation.sh`

Neither exists in the worker base, current tree, or Git tree. The mandatory
selection rule therefore has zero candidates, no authority-selected argv, and
no possible stdout object with schema
`stage1-validator-semantic-result/1.0`. The worker is forbidden to create,
refresh, rename, replace, or delete a candidate. Structural checks, Lean exit
zero, or an undeclared adapter cannot substitute for the missing replay.

This scheduler-ownership defect prevents a genuine validation self-test. This
run deliberately emits no `validation-receipt.json` and no
`.stage1-worker-selftest.json`.

## Positive Validation Boundary

Independent gates also fail closed:

- `S56-M-0120-PROOF` is authoritative `[_]`, not master-accepted `[x]`.
- `proof-receipt.json` has `accepted=false`, `verdict=blocked`, and closes none
  of the 25 frozen positive obligations.
- `validation-specs.json` belongs to the obligation-tree phase. All 25 entries
  remain prose-only planned recipes, with no structured argv or positive
  semantic output contract suitable for the validation phase.
- Every frozen obligation has `terminal_proof_body_id=null`; no positive root
  proof body exists.
- A fresh trust-zero replay checks
  `Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget` with exact type
  `Not (MoriConeTheoremTarget.{0,0,0,0})` and reports only `propext`,
  `Classical.choice`, and `Quot.sound`.

The countermodel makes all geometric premise fields true while selecting
unrelated numerical data: the Mori cone is `{-1}`, the canonical pairing is
the identity, and the rational-curve carrier is empty. The asserted
decomposition of `-1` would force `0 <= -1`. This refutes only the disconnected
abstract encoding, not the mathematical Mori cone theorem, and grants no
positive proof or validation credit. The root remains open at `M3`, with
`audit_complete=false` and `theorem_complete=false`.

The integrated schema-1.1 dependency ledger truthfully records the still-empty
closure, but its graph, repository, layer, and item bindings belong to the
earlier proof attempt. No validation-phase replacement is emitted because the
required scheduler-owned semantic validator is absent and no accepted
hard-edge reuse exists to attach to a consumer validation receipt. The
companion JSON records the current empty dependency context directly.

## Bounded Checks

Before writing this report, the standard, theorem-DAG, phase-contract, and
target-manifest validators passed. The target statement, anchor-audit, and
obligation-tree validators also passed while preserving the `M3` boundary and
25 open obligations.

The unchanged `Statement.lean` and `Proof.lean` were copied byte-for-byte to a
fresh temporary directory under the Lean project and elaborated with Lean
4.29.0 at trust level zero. Existing pinned `LEAN_PATH` artifacts were reused
read-only. The statement and proof output SHA-256 values were respectively
`227b41b022b670d99a326070af16b3007dbf438d19f8e7d4745d7afc57370ab4`
and
`3898551895c04d36d276ee78335df8d097d382c9f85862d62a5b4224334412f0`.
The compiled-object SHA-256 values were respectively
`2fdf2632f58d0372d70aaf2c7bec072990ad843627a3775c83fcec60d998582e`
and
`3d6cdabfa5cbe7242c120c94c37edb8ce6571401dadb762297374934fac88afd`.

The mathlib revision was
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with clean tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. No `lake update`, `lake build`,
dependency clone/fetch, network access, or intentional `.lake` mutation was
performed. These are bounded negative checks, not a semantic validation replay
or release-grade hermetic evidence.

After these two blocker files were written, JSON parsing and target-scoped
`git diff --check` passed. A fresh theorem-DAG check then failed because its
deterministic evidence inventory now sees the new target-owned files; the
aggregate standard check reports the same derived mismatch. Worker rules
forbid editing or regenerating that authority. The scheduler integration lane
must regenerate it after copying this blocked snapshot.

## Retry Condition

The scheduler/master lane must publish exactly one declared validation
candidate at authoritative HEAD and issue a fresh claim whose immutable base
contains the identical blob. Positive validation also requires reopening and
repairing the disconnected statement encoding, then refreezing and
master-accepting statement, anchor, obligation-tree, and proof evidence in
exact DAG order. The proof must be a positive placeholder-free root proof, and
the validation specification must contain complete authority-bound structured
recipes and expected semantic outputs.

The validation item remains `[ ]`. This blocker is not a phase receipt, makes
no worker state proposal, and establishes no M0, validation acceptance,
AUDIT-Z, THEOREM-Z, release, theorem completion, or master acceptance.
