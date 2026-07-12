# Intake validation (historical phase record)

Base revision: `c90787f590a3c33f8b60f77575a97c71b3e93ff6`.

This file records the earlier intake phase and is superseded for the exact expression by
`statement-validation.md`. At intake, validation was limited to target/standard consistency,
bounded source and formal-candidate discovery, JSON syntax, scoped intake invariants, and
whitespace. The worker clone's pre-existing untracked `Formalizations/Lean/.lake` link/artifact was
not modified or counted as an intake changed path.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0770` | exit 0; rank 579, L0/rework_required, planned, theorem_complete false |
| `rg -n 'theorem.*zorn\|zorn_le\|exists_maximal_of_chains_bounded' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0; pinned `Mathlib/Order/Zorn.lean` candidates located |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95`, matching `lake-manifest.json` |

| `python3 -m json.tool Stage1_Instances/THM-M-0770/{instance,task-dag}.json` (run once per file) | exit 0 for both files |
| scoped Python intake-invariant check | exit 0; planned lifecycle, zero accepted state, exact owned file set, and all six downstream tasks open |
| scoped Python prohibited-construct and whitespace check | exit 0; no Lean proof files, forbidden proof constructs, trailing whitespace, tabs, or missing final newlines |
| `git diff --check` | exit 0; no tracked whitespace errors; the scoped Python check covers this new untracked dossier |

Known downstream failures are primary-source pinning and review, exact statement
selection and mutation tests, canonical Lean elaboration/fingerprint, candidate and trust audit,
obligation registry and typed graphs, proof/composition/readability closure, hermetic replay, and
independent verification. These keep theorem completion false without invalidating this planned
intake.

## Validation-phase execution

Item: `S56-M-0770-VALIDATION`

Base revision: `b17067c5d92786b270337cbdd3bfaf74df7773f9`

Validation timestamp: `2026-07-12T05:00:34Z`

The proof-phase declaration was kernel-replayed against the exact frozen target. A separate
`Validation.lean` reconstruction calls `zorn_le`, explicitly handles the empty-chain case, and
therefore does not reuse the proof phase's `zorn_le_nonempty` invocation. The fail-closed validator
also checked input hashes, the proof receipt closure set, the clean pinned mathlib revision and
Zorn source, the local placeholder policy, and both axiom reports.

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0770
python3 Stage1_Instances/THM-M-0770/check_statement.py
python3 Stage1_Instances/THM-M-0770/check_anchor_audit.py
python3 Stage1_Instances/THM-M-0770/check_obligation_tree.py
python3 Stage1_Instances/THM-M-0770/check_proof.py
  all exit 0
(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0770/check_proof.sh)
  exit 0: zornsLemma depends on [propext, Classical.choice, Quot.sound]
python3 Stage1_Instances/THM-M-0770/check_validation.py
  exit 0: exact proof root and independent zorn_le reconstruction passed;
  pinned provenance/trust checks passed; release-only gates remain blocked
```

This is nonrelease worker evidence. The proof dependency lacks master acceptance, and the frozen
typed graph still records its pre-proof `root_closed=false` / `M3` boundary. The run reused the
canonical pinned warm `.lake` cache, so it is not a cold empty-cache hermetic replay. The independent
probe ran in this checkout with that shared cache, not on a distinct independently provisioned
runner. Complete transitive provenance/TCB, offline restoration, SBOM/license evidence, H0/R0,
deterministic release bundling, and master acceptance remain open. `audit_complete=false` and
`theorem_complete=false`.
