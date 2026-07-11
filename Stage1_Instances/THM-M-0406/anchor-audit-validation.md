# THM-M-0406 anchor-audit validation

Item: `S56-M-0406-ANCHOR_AUDIT`  
Base revision: `4dabab14860067cbb1220d76c5a1bd9abd87d624`

The exact commands and results below were run in the worker clone on
2026-07-12. The pre-existing untracked `Formalizations/Lean/.lake` link reused
canonical pinned artifacts. No Lake update, build, clone, fetch, or dependency
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | rank 19, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | commit `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; tree `32c9eace926573a9981787ae97643e520353c893` |
| scoped exact-name/topic `rg` searches over pinned mathlib, all other pinned Lake packages, `flt-regular`, and repo-local Lean | 0 | support and legacy-planning hits only; no terminal Corvaja--Zannier or Subspace-Theorem declaration |
| GitHub recursive-tree API for `google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` | 0 | `truncated=false`, 1204 entries, no relevant path |
| five GitHub repository API searches recorded in `anchor-audit.json` | 0 | totals `0,0,0,0,0`; every response `incomplete_results=false` |
| GitHub code API query for `Corvaja language:Lean` | 0 transport / HTTP 401 | authentication required; access limit recorded |
| grep.app API query for `Corvaja` in Lean | 0 transport / HTTP 429 | no result; access limit recorded |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0406/Statement.lean` | 0 | canonical proposition and exact-type fixture elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0406/AnchorAudit.lean` | 0 | all ten pinned substrate declaration probes elaborated |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | six candidates, pins, hashes, and source witnesses verified; root open |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/anchor-audit.json` | 0 | structured audit parsed |
| `git diff --check -- Stage1_Instances/THM-M-0406 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The bounded inventory is self-tested and ready for master review. Accepted
receipts remain empty, and neither overall audit completion nor theorem
completion is claimed.
