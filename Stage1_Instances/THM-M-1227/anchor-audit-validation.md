# THM-M-1227 anchor-audit validation

Base revision: `c00bc6793b3d4c186b81b80bbaf165b32e125b58`.

Validation used only the existing pinned `.lake` artifacts. No dependency update, clone, fetch, or
build was run. Exact command output is summarized below; machine-readable revisions, hashes, search
terms, and result boundaries are in `anchor-audit.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1227` | 0 | rank 416; planned; theorem_complete false |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; inspected checkout clean |
| bounded `rg`/`git grep` over pinned `Mathlib/**/*.lean` | 0 | only TestFunction prose matched; zero terminal candidates |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1227/AnchorAudit.lean` | 0 | all substrate probes elaborated; zero-candidate check compiled |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1227/Statement.lean` | 0 | canonical expression remains a `Prop` |
| `python3 -m json.tool Stage1_Instances/THM-M-1227/anchor-audit.json` | 0 | structured audit is valid JSON |
| `rg -n '\\b(sorry|admit|axiom)\\b' Stage1_Instances/THM-M-1227/AnchorAudit.lean` | 1 | expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1227` | 0 | no whitespace errors |

Known failure boundary: no exact terminal Lean theorem was found, so proof closure, obligation-tree
execution, hermetic validation, and theorem completion remain open. This is a self-tested
anchor-audit node pending master acceptance.
