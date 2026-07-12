# Intake validation

Base revision: `418e6ea60487eaae4d9a1fa7aeb4bb7c575c33ee`.

Validation is intentionally limited to target/standard consistency, dossier structure, pinned API
availability, forbidden proof-token hygiene, and whitespace. `Formalizations/Lean/.lake` is the
automation clone's pre-existing symlink to the canonical pinned artifacts; no dependency update,
fetch, build, or mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0559` | exit 0; rank 607, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0559/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0559/task-dag.json` | exit 0 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0559/IntakeSurface.lean` | exit 0; `Topology.CWComplex`, `HomotopyGroup.Pi`, `ContinuousMap.HomotopyEquiv`, and `ContinuousMap` elaborated under Lean 4.29.0 |
| forbidden proof-token scan over owned Lean sources | exit 0; no proof escape or assumed declaration |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0559` | exit 0; no output |

The first downstream gate remains the exact statement. In particular, API existence does not
establish the component map, functorial induced maps on `HomotopyGroup.Pi`, or Whitehead's theorem.
Primary theorem/page and errata inspection, source review, statement mutation tests, formal-anchor
audit, obligation registry, proof, hermetic replay, and independent validation all remain open.

## Statement-phase validation (2026-07-12 Asia/Shanghai)

The existing canonical pinned `.lake` symlink was reused without update, fetch, build, or other
dependency mutation.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0559` | exit 0; rank 607, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0559/Statement.lean` | exit 0; induced component/group maps, canonical target, checked expansion, three mutations, and explicit target print elaborated under Lean 4.29.0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0559/statement.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0559/statement-receipt.json` | exit 0 |
| forbidden declaration/proof-escape scan over `Statement.lean` | exit 0; no forbidden declaration or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-0559 .stage1-worker-selftest.json` | exit 0; no output |

## Anchor-audit worker validation

Base revision: `9898022a0eed3cf9fb3c55a6affb6176224f33cf`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique ordered targets validated |
| `python3 scripts/stage1_target.py show THM-M-0559` | exit 0; rank 607, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0559/AnchorAudit.lean` | exit 0; pinned model-category Whitehead candidates and topology substrate elaborated |
| immutable codeload inspection of `jzxia/WhiteheadTheorem@ee1d4a5c332e6b95853bfa0719efd9f435317307` | exit 0; archive SHA-256 `4faf267fd0ce760ca4db88240fec8782278d9fa2e28977b2c70fd54c9a291023`; declaration, source pins, Apache-2.0 license, and scoped proof-token scan recorded; nothing installed or fetched into `.lake` |
| `python3 -m json.tool Stage1_Instances/THM-M-0559/anchor-audit-receipt.json` | exit 0 |
| scoped forbidden proof-token scan over `Stage1_Instances/THM-M-0559/*.lean` | exit 0; no active `axiom`, `unsafe`, `sorry`, `admit`, or `sorryAx` |
| `git diff --check -- Stage1_Instances/THM-M-0559 .stage1-worker-selftest.json` | exit 0; no output |

The narrow Lean check validates only pinned mathlib interfaces. The external archive is immutable
source evidence, not an integrated build: its toolchain/mathlib revisions and theorem scope differ.
No anchor is assigned kernel-closure credit.

This is worker-local statement evidence, not proof or release evidence. Primary-source acceptance,
anchor audit, obligation expansion, proof closure, trust closure, replay, and independent master
acceptance remain open.
