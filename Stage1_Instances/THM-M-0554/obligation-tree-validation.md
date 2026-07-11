# THM-M-0554 obligation-tree validation

Item: `S56-M-0554-OBLIGATION_TREE`  
Base revision: `b7719b39b5595e187b4d2ecf832d3922a916d38b`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The deterministic builder produced 32 obligations and seven separately typed
graphs. The validator recomputed the frozen denominator digest, checked the
statement/audit input hashes, required one registry row and full node schema
per obligation, checked every leaf ledger is at most 100 steps, checked all
reciprocal proof/composition edges and graph indexes, rejected duplicate edges,
proved the proof graph acyclic, and proved all 30 required machine obligations
reachable from the exact root. It also checked one offline validation recipe
per obligation and confirmed the closure boundary remains open.

The exact target re-elaborated with the pinned Lean executable. The existing
canonical `.lake` symlink was reused and not modified. No update, build,
dependency fetch, clone, or network action ran.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets accepted. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546 accepted. |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106, planned, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/build_obligation_artifacts.py` | 0 | Wrote 32 obligations and 91 typed edges. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS`; denominator `3c72072a...8048b`; root open at M4. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0554/Statement.lean)` | 0 | Exact target and checked expansion elaborated. |
| `python3 -m json.tool` on all three new JSON artifacts | 0 | All structured artifacts parsed. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: no prohibited Lean declaration token. |
| `git diff --check -- Stage1_Instances/THM-M-0554 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Status boundary

This receipt self-tests only the obligation architecture freeze. Planned
fingerprints are not elaborated declarations, reciprocal graph edges are not
composition certificates, and leaf budgets are not proofs. Root M4,
formalization debt, missing source review, missing proof bodies, and all later
validation/release gates remain explicit. Master acceptance is still required.
