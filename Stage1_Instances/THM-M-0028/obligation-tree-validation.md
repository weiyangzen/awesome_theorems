# THM-M-0028 obligation-tree validation

Item: `S56-M-0028-OBLIGATION_TREE`. Base revision:
`a16584a808446057f9ca2f2f26e76230cf45b84f`.

Validation ran in the isolated worker clone on 2026-07-13 (`Asia/Shanghai`). It reused the existing
manifest-pinned Lake artifacts and did not update, build, fetch, clone, or modify dependencies. The
shared cache makes this warm, nonrelease evidence.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0028
  exit 0; rank 1073, planned, L0/rework-required, theorem_complete false

python3 -B Stage1_Instances/THM-M-0028/build_obligation_artifacts.py
  exit 0; wrote 25 obligations and 40 typed edges
  denominator: 65d02abdd95b23837143f3a9562ea2ae68a7f0e32f917af40827e25b2aec121b

python3 -B Stage1_Instances/THM-M-0028/check_obligation_tree.py
  exit 0; PASS THM-M-0028 obligation tree: 25 obligations, 40 typed edges
  root closure: open (H1/M3/R3); both exact pinned bridges remain proof-phase cuts

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0028
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean Statement.ilean
  exit 0; the exact statement and both conditional compositions elaborated; all three composition
  declarations reported only propext and Quot.sound; temporary outputs removed;
  ObligationTree stdout sha256 164af0aec671ebff4cdbfe698a4712a5f1414b3b7888bc7d04d8886eac7ed4e0

python3 -m json.tool <each changed structured JSON>
  exit 0; every structured artifact parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0028-obligation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0028/build_obligation_artifacts.py \
  Stage1_Instances/THM-M-0028/check_obligation_tree.py
  exit 0; both Python files compiled outside the repository tree

rg -n -i --glob '*.lean' '<prohibited proof and oracle markers>' \
  Stage1_Instances/THM-M-0028/ObligationTree.lean
  exit 1; expected no-match result

git diff --check -- Stage1_Instances/THM-M-0028 .stage1-worker-selftest.json
  exit 0; no whitespace diagnostics, including no-index checks for new files
```

The structural validator checks deterministic regeneration, target and unchanged DAG identity,
predecessor hashes, the closed registry-kind set, unique IDs, eligibility and pending exclusions,
the frozen denominator, complete node schema and semantic ledgers, all seven typed graphs, complete
adjacency indexes, per-graph acyclicity, reciprocal proof edges, architecture reachability, exact
certificate-to-proof-edge agreement, structured recipes, open closure, source pins and terminal
body hygiene, wrapper deduplication, receipt/self-test agreement, stable reader anchors, and
unchanged `[H1, M3, R3]`. It does not install either candidate body or prove a release gate.
