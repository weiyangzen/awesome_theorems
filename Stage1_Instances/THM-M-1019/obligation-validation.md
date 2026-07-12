# THM-M-1019 obligation-tree validation

Item: `S56-M-1019-OBLIGATION_TREE`  
Base revision: `08405432a9f96f6c39ff79724e7f5965d01305ca`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The registry freezes 22 required obligations with an exact root fingerprint and a content-derived
denominator. The graph validator requires the complete node schema, validates legal typed edges and
reciprocal indexes in seven separate graph families, proves proof/refinement acyclicity and full root
reachability, checks every readable anchor, and enforces an explicitly open closure boundary.

The existing pinned Lake artifacts were reused. No dependency update, build, clone, fetch, or other
`.lake` mutation was run.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1019` | 0 | rank 495; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1019/build_obligation_artifacts.py` | 0 | wrote 22 obligations and 28 typed edges |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1019/Statement.lean` | 0 | exact frozen target, integral transport, and four mutations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1019/AnchorAudit.lean` | 0 | exact imported wrapper elaborated; printed axioms contain no `sorryAx` |
| `python3 Stage1_Instances/THM-M-1019/check_statement.py` | 0 | exact expression fingerprint and all four statement mutations checked |
| `python3 Stage1_Instances/THM-M-1019/check_anchor_audit.py` | 0 | immutable target, pin/tree, source identity, candidates, and boundary agreed |
| `python3 Stage1_Instances/THM-M-1019/check_obligation_tree.py` | 0 | 22 obligations, 28 typed edges, full reachability, open M1 root |
| `python3 -m json.tool Stage1_Instances/THM-M-1019/obligation-registry.json >/dev/null` | 0 | registry is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1019/typed-graphs.json >/dev/null` | 0 | graph bundle is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1019 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This self-tests only the architecture freeze. Planned fingerprints do not claim elaborated leaf
declarations, empty evidence lists do not close obligations, and the anchor candidate is not promoted
by this phase. Proof bodies, composition certificates, accepted source/readability reviews, transitive
trust, hermetic and independent validation, and theorem completion remain downstream. Master
acceptance is required for this scheduler item.
