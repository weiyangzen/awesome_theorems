# Statement validation

Base revision: `c1872cd2c3f098acab4c5741887722d0d0b47838`.

The exact target is `Stage1Instances.THM_M_0988.StatementShape` in
`Statement.lean`. It explicitly quantifies both probability spaces, measures,
the iid sequence, and the Gaussian-law witness. The sole direct import is the
pinned module that declares the matching mathlib theorem.

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0988/Statement.lean` | exit 0; the pinned theorem type, canonical target, and four distinct mutation expressions printed |
| `python3 Stage1_Instances/THM-M-0988/check_statement.py` | exit 0; canonical expression SHA-256 `fc6e4406127b02f2881070dba8415e942f5c0b5197bbdd05167f3b6f5300daf9`; four mutations distinguished |
| `python3 -m json.tool Stage1_Instances/THM-M-0988/statement.json` | exit 0 |
| `rg -n "\\b(sorry|axiom|admit)\\b" Stage1_Instances/THM-M-0988/Statement.lean Stage1_Instances/THM-M-0988/check_statement.py` | exit 1; no matches (expected clean scan) |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `git diff --check -- Stage1_Instances/THM-M-0988` | exit 0; no output |

`lake env lean --version` reported Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. The reused pinned mathlib checkout
reported revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

This is statement-only evidence. Primary-source acceptance, anchor provenance,
proof closure, trust analysis, hermetic replay, and independent review remain
open, so neither theorem proof nor theorem completion is claimed.
