# THM-M-0158 validation-phase result

Item: `S56-M-0158-VALIDATION`
Base revision: `7c8a8597055a5d4012e43f6e2f6727d1a8632aa5`

The structured validator rechecked the exact frozen statement, the conditional composition, and
the direct local proof in a fresh temporary module directory. All elaborate against pinned Lean
4.29.0 and mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The two printed
declarations depend exactly on `propext`, `Classical.choice`, and `Quot.sound`; no `sorry`, `admit`,
local `axiom`, `unsafe`, or `implemented_by` boundary occurs in the checked sources.

## Exact commands and results

Commands ran from the repository root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1..1546 pass. |
| `python3 scripts/stage1_target.py show THM-M-0158` | 0 | rank 657, planned, L0/rework_required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0158/check_validation.py` | 0 | Fresh-directory kernel replay, exact axiom-set check, source hygiene, statement/registry hashes, and clean dependency pin pass. |
| `python3 -m json.tool Stage1_Instances/THM-M-0158/validation-spec.json` | 0 | Structured recipe is valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-0158/validation-receipt.json` | 0 | Provisional node receipt is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0158 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The validator invokes only narrow `lake env lean` checks. It copies `Statement.lean`,
`ObligationTree.lean`, and `Proof.lean` into a fresh temporary directory under
`Formalizations/Lean`, emits temporary `.olean` files there, and removes the directory. It neither
updates nor builds Lake dependencies and verifies that the manifest pin equals the clean checked-out
mathlib revision.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, conditional composition, and `weingartenEquations : WeingartenEquationsTarget` elaborate. |
| Placeholder/unsafe scan | pass | Forbidden proof boundaries are absent from all three checked modules. |
| Trust observation | provisional pass | Both printed declarations report exactly the three expected mathlib/Lean axioms, with no `sorryAx`; no release-grade TCB closure is claimed. |
| Local provenance | pass with stale-state finding | Source and registry hashes agree and pinned mathlib is clean. The frozen graph predates the direct proof and still reports `M0158-T-RECONSTRUCT` open. |
| Hermetic release replay | fail closed | The run reused the canonical writable warm `.lake` cache; no empty-cache cold build, offline restoration, full TCB inventory, or SBOM/license closure was performed. |
| Independent validation | fail closed | One worker in one mutable clone is not a distinct runner, second attestation, or independently implemented verifier. |
| Human/readable review | fail closed | Pinpoint primary-source inspection and independent `H0`/`R0` review remain open. |

This validates the assigned worker phase truthfully but does not grant accepted `M0-*`, `E0/E1`,
`AUDIT-Z`, `THEOREM-Z`, release, or master acceptance. `audit_complete=false` and
`theorem_complete=false`; authoritative graph reconciliation and every failed release gate remain
for later nodes and the integration lane.
