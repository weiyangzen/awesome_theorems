# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

All commands ran from the repository root on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1184` | 0 | Rank 169, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1184/intake.json >/dev/null` | 0 | Intake JSON parses |
| `test "$(python3 -c 'import json; print(json.load(open("/tmp/thm-m-1184-show.json"))["theorem_id"])')" = THM-M-1184` | 0 | CLI result identifies the intended target |
| `git diff --check -- Stage1_Instances/THM-M-1184` | 0 | No whitespace errors |

This is the smallest real validation appropriate to an intake-only node. No Lean theorem is added
or credited, so a Lean build would not validate the new dossier's claim. Exact elaboration is the
dependent statement node. Known open gates are the statement/environment fingerprints, checked
transports and mutation tests, source pin/errata audit, frozen obligation graphs, proof closure,
hermetic replay, and independent acceptance.
