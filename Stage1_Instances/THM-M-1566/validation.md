# Intake validation

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

The intake was validated with these commands from the repository root:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1566` | exit 0; rank 182, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/intake.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-1566` | exit 0 |

This is structural and documentary intake validation, not Lean elaboration or
theorem validation. Exact source acceptance, statement fingerprint, toolchain
fingerprint, obligation freeze, and all proof/release gates remain open.
