# THM-M-0786 anchor-audit validation

Item: `S56-M-0786-ANCHOR_AUDIT`  
Base revision: `32404187d6cee70b44ae90adf8d0d765752e5149`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The repo-local target and pinned mathlib provide only an exact statement and Borel vocabulary. No
local or pinned-mathlib proof candidate was found. The external search located the dedicated Lean 4
project `sven-manthe/A-formalization-of-Borel-determinacy-in-Lean` and resolved its branch to
immutable revision `42bc874b2357ca7e7573b31854a0d09761e11e41`. Its
`GaleStewartGame.borel_determinacy` has the right arbitrary-move, pruned-tree, Borel-payoff scope.

This is not machine closure evidence here. The revision has no GitHub Actions run, uses Lean
`4.28.0-rc1` and mathlib `b94b918...dced` rather than the repository pins, is not a local dependency,
and has no checked adapter to the canonical total-strategy encoding. A scan of every immutable Lean
source found no textual `sorry`, `admit`, `axiom`, or `unsafe`, but that scan is not a parser-aware
transitive trust audit. Consequently the external candidate is `M5`, not `M1`, and the root moves
truthfully from `M4` discovery debt to `M3` statement/interface debt. The vector remains
`[H1, M3, R3]`; audit completion and theorem completion are false.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-0786` | 0 | rank 791, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repo-local and pinned-mathlib `rg` queries for the recorded aliases | 0 | no proof candidate; only unrelated uses and statement vocabulary were found |
| GitHub repository API queries for quoted Borel determinacy and Gale-Stewart plus Lean | 0 | one dedicated project and no second repository, respectively |
| GitHub commit/tree and immutable raw-file inspection | 0 | revision/tree, declaration, source hash, Lean/mathlib pins, manifest hash, and Apache-2.0 license matched the ledger |
| GitHub Actions runs query at revision `42bc874...1e41` | 0 | `total_count = 0`; no upstream CI receipt available |
| immutable full-tree defensive source scan | 0 | no textual placeholder, bodyless axiom, or unsafe declaration found; explicitly not credited as a parser-aware trust audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0786/Statement.lean)` | 0 | canonical target, checked expansion, mutations, and boundary lemmas re-elaborated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0786/AnchorAudit.lean)` | 0 | pinned `MeasurableSet` and Baire-space measurable-structure APIs re-elaborated without importing the external project |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0786/check_anchor_audit.py)` | 0 | local pin/negative inventory and the captured immutable external snapshot matched; root `M3`, external `M5` |
| `python3 -m json.tool Stage1_Instances/THM-M-0786/anchor-audit.json` | 0 | structured ledger parsed |
| prohibited-token scan over this target's Lean files | 0 | no `sorry`, `admit`, or `axiom` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0786 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. This
phase freezes and self-tests the candidate inventory and classifications pending master acceptance;
it does not claim exhaustive discovery, source acceptance, external reproducibility, audit
completion, or theorem completion.
