# Statement validation record

Item: `S56-M-1288-STATEMENT`. Base revision:
`d9a306e1c1d941b347946d9efe1f1a8225f40978`.

Commands were run from the repository root on 2026-07-12 unless the command
contains an explicit `cd`. No dependency update, fetch, clone, or build was run.
The pre-existing untracked `Formalizations/Lean/.lake` link supplied the pinned
artifacts and was not changed by this item.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1288` | 0 | rank 459, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386...` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1288/Statement.lean` | 0 | target, three imports, helper definitions, and three structural mutations elaborated; `#print` emitted the target |
| `python3 -m json.tool Stage1_Instances/THM-M-1288/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1288 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The SHA-256 of the complete `pp.explicit=true` Lean output was
`399dca9a18e2ab2e7577ab64e41f7bc79a0b3f20cc5c4fcb3f3d7d9593408126`;
the statement file hash was
`fc152a0dff8d2dd50231d76f5fcc32ad0bd3edbf3fc5c69bfe856a73ef67ce6d`.

This is statement elaboration evidence only. In particular, no proof body,
source-audit acceptance, checked alternate transport, or theorem-completion
receipt is claimed.
