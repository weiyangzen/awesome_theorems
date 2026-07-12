# Statement validation

Base revision: `1794fae27ddcf6d19b6984502e27a9233890d8d1`.

| Command | Exact result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0317/Statement.lean` | exit 0; target, checked subtype transport, and four mutation witnesses elaborated; printed canonical target and transport |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; `Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | exit 0; `1546 unique targets`, execution ranks `1..1546` |
| `python3 scripts/stage1_target.py show THM-M-0317` | exit 0; rank 683, `L0`, `rework_required`, lifecycle `planned`, theorem complete false |
| placeholder scan over statement artifacts | exit 0; no `sorry`, `axiom`, `admit`, `placeholder`, or `hresult` tokens in Lean source |
| `git diff --check -- Stage1_Instances/THM-M-0317 .stage1-worker-selftest.json` | exit 0; no output |

The clone's `.lake` is the pre-existing automation symlink to the canonical pinned artifacts. No
dependency update, build, clone, or fetch was run. This is narrow statement elaboration evidence,
not theorem-proof or release evidence.
