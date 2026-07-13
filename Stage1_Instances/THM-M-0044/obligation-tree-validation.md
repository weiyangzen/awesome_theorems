# THM-M-0044 obligation-tree validation

Item: `S56-M-0044-OBLIGATION_TREE`. Base revision:
`bba12d6e1323b0998c5f255e488c95ef89ab9e4c`.

Validation ran in the isolated scheduler worker clone on 2026-07-13. The automation-provided
canonical `.lake` symlink and its pinned artifacts were reused. No `lake update`, build, dependency
fetch, clone, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots,
  1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0044
  exit 0
  rank 1084; planned; L0/rework_required; theorem_complete false

python3 -B Stage1_Instances/THM-M-0044/build_obligation_artifacts.py
  exit 0
  ca7e41568d1de7831322431b4b7821d0c443907eededff9c9d94cb464c44bd91

python3 -B Stage1_Instances/THM-M-0044/check_obligation_tree.py
  exit 0
  PASS THM-M-0044 obligation tree: 39 obligations, 190 typed edges
  registry denominator sha256: ca7e41568d1de7831322431b4b7821d0c443907eededff9c9d94cb464c44bd91
  root closure: open (H1/M3/R3); the real and complex positive-dimension packages remain M4

cd Formalizations/Lean
rm -rf /tmp/stage1-thm-m-0044-obligation-lean
mkdir -p /tmp/stage1-thm-m-0044-obligation-lean
lake env lean --root=../.. ../../Stage1_Instances/THM-M-0044/Statement.lean \
  -o /tmp/stage1-thm-m-0044-obligation-lean/Statement.olean
LEAN_PATH="/tmp/stage1-thm-m-0044-obligation-lean:$(lake env printenv LEAN_PATH)" \
  lake env lean --root=../.. ../../Stage1_Instances/THM-M-0044/ObligationTree.lean
  exit 0
  selectedEmptyDimensions, root_of_real_and_complex, and the exact root elaborated;
  both checked declarations report only propext, Classical.choice, and Quot.sound
  Lean output sha256: da80d0ef0b993029b13baa6459153f5cb57535d544ce0e5d69abe04602de67f2

for f in \
  Stage1_Instances/THM-M-0044/instance.json \
  Stage1_Instances/THM-M-0044/obligation-registry.json \
  Stage1_Instances/THM-M-0044/typed-graphs.json \
  Stage1_Instances/THM-M-0044/validation-specs.json \
  Stage1_Instances/THM-M-0044/obligation-tree-receipt.json \
  .stage1-worker-selftest.json
do
  python3 -m json.tool "$f" >/dev/null || exit
done
  exit 0; every structured artifact parses

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0044-obligation-pycache \
  python3 -m py_compile \
    Stage1_Instances/THM-M-0044/build_obligation_artifacts.py \
    Stage1_Instances/THM-M-0044/check_obligation_tree.py
  exit 0

if rg -n '\b(sorry|admit|sorryAx|axiom|unsafe|opaque|implemented_by|native_decide|extern)\b' \
  Stage1_Instances/THM-M-0044/ObligationTree.lean
then
  exit 1
else
  echo 'HYGIENE PASS: no prohibited constructs'
fi
  exit 0; HYGIENE PASS: no prohibited constructs

git diff --check -- Stage1_Instances/THM-M-0044 .stage1-worker-selftest.json
  exit 0; no whitespace diagnostics
```

The structural checker deterministically rebuilds the generated JSON in memory, verifies statement
and anchor freeze hashes, the immutable denominator and all eligibility projections, mandatory
S/N/B/C/L/X/T layers, complete node schemas and concrete ledgers, separate graph types, adjacency,
acyclicity, reciprocal proof edges, root reachability, structured recipe coverage, pinned mathlib
source hashes/markers, placeholder hygiene, open closure, receipt fields, and worker-packet parity.

Lean re-elaborates the exact statement and checks only the empty-dimension package and conditional
composition into the exact root. It does not prove either positive-dimensional field package, the
spectral-to-SVD construction, source/readability/trust closure, audit completion, or theorem
completion. This is warm, unsigned, nonrelease worker evidence pending dependency-ordered master
acceptance.
