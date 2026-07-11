# Obligation-tree validation

Item: `S56-M-0398-OBLIGATION_TREE`  
Base revision: `b38353d62a9d55f41b9a0f70eb889ff9af6a9fe9`  
Validation date: 2026-07-12

The structural self-test recomputes the registry denominator, requires all
node-schema fields, checks the seven graph families and reciprocal proof
edges, rejects proof cycles and orphaned proof-route nodes, binds validation
recipes, and asserts the open-root boundary. The Lean run builds only a local
temporary `Statement.olean` under the owned directory, checks the conditional
composition, prints its axioms, and removes that object. It does not mutate the
pinned `.lake` tree.

| Command | Exact result |
|---|---|
| `python3 Stage1_Instances/THM-M-0398/build_obligation_artifacts.py` | exit 0; wrote 15 obligations and 29 typed edges |
| `python3 Stage1_Instances/THM-M-0398/check_obligation_tree.py` | exit 0; denominator `ad4d614392ebd6517f699e3babba9bd3daa3d35d62c125b1be851a9ced57d741`; root open at M3, `M0398-L4` cut |
| `cd Stage1_Instances/THM-M-0398 && LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean -o Statement.olean Statement.lean && LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean ObligationTree.lean && rm Statement.olean` | exit 0; `root_of_finiteExceptionalWithConstant` elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 1546 uniform-L0 targets and all assurance groups passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0398` | exit 0; rank 11, planned, L0/rework required, theorem complete false |
| `python3 -m json.tool` on the registry, graphs, validation specs, and instance | exit 0 for all four files |
| `git diff --check -- Stage1_Instances/THM-M-0398` | exit 0; no whitespace errors |

Known failures and open gates: `M0398-N1`, `C1`, `C2`, `L1`, `L2`, `L3`, and
the recomposed constant-factor engine `L4` have no Lean proof bodies. The
node-specific primary-source crosswalk, terminal provenance/trust closure,
readable reconstruction, hermetic replay, and independent review remain open.
Consequently this receipt self-tests only the obligation-tree phase and makes
no theorem-completion claim.
