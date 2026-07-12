# THM-M-0025 obligation-tree validation

Item: `S56-M-0025-OBLIGATION_TREE`. Base revision:
`4ecdda4863162748b3ee70bc4ec842789418145d`.

Validation ran in the isolated worker clone on 2026-07-13. It reused the existing manifest-pinned
Lake artifacts and did not update, fetch, clone, or build dependencies. The shared cache makes this
warm, nonrelease evidence.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0025
  exit 0; rank 1070, planned, L0/rework-required, theorem_complete false

python3 -B Stage1_Instances/THM-M-0025/build_obligation_artifacts.py
  exit 0; wrote 26 obligations and 44 typed edges
  denominator: a93e848c6941b5069b7e79e2d5f88ddea8663e7443f7ebcf3719e5b0022ebc3c

python3 -B Stage1_Instances/THM-M-0025/check_obligation_tree.py
  exit 0; PASS THM-M-0025 obligation tree: 26 obligations, 44 typed edges
  root closure: open (H1/M3/R3); exact pinned anchor remains the proof-phase cut

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0025
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean Statement.ilean
  exit 0; canonical statement re-elaborated; exact anchor and internal helper types checked;
  three conditional compositions reported only propext, Classical.choice, and Quot.sound;
  temporary outputs removed; ObligationTree stdout sha256 85ce24ee...9d3205

python3 -m json.tool <each new or changed structured JSON>
  exit 0; every structured artifact parses as JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0025-obligation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0025/build_obligation_artifacts.py \
  Stage1_Instances/THM-M-0025/check_obligation_tree.py
  exit 0; both Python files compiled outside the repository tree

rg -n -i --glob '*.lean' '<prohibited proof and oracle markers>' \
  Stage1_Instances/THM-M-0025/ObligationTree.lean
  exit 1; expected no-match result

git diff --check -- Stage1_Instances/THM-M-0025 .stage1-worker-selftest.json
  exit 0; no tracked whitespace diagnostics; new-file no-index checks also passed
```

The structural validator checks deterministic regeneration, target/DAG identity without modifying
authoritative state, predecessor hashes, unique IDs, exclusions, denominator projections, complete
node schema, all seven typed graphs, adjacency indexes, reciprocal checked proof edges, open
logical-decomposition edges, acyclicity, root reachability, architecture-only recipes, aliases,
pinned source markers and blob, receipt and
self-test agreement, hygiene, and unchanged `[H1, M3, R3]`. It does not install the candidate or
prove that a release gate passed.
