# THM-M-0043 obligation-tree validation

Item: `S56-M-0043-OBLIGATION_TREE`

Base revision: `7d0965498598e684e3e3d0a01836c2bf36a02959`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen Result

Registry version 1 freezes 33 unique obligations before proof-phase integration. The canonical
ten-field projection has SHA-256
`1a92339af83640c1cf5d8853722d8c381b11a9d4139c4cb251cea3781d5b2af8`.
The bundle has 96 typed edges across separate proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. It expands the external Atlas body from normality through
commuting Hermitian parts, joint eigenspaces, a subordinate orthonormal basis, the unitary basis
matrix, and the final conjugated-diagonal equation. Each proof requirement has a reciprocal
composition edge and each semantic step budget is at most 80.

The run uses the existing manifest-pinned Lake artifacts only. It does not run Lake update/build,
fetch or clone a dependency, or otherwise mutate `.lake`.

## Commands And Results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0043
  exit 0: rank 1083, planned, L0/rework_required, theorem_complete false

python3 -B Stage1_Instances/THM-M-0043/build_obligation_artifacts.py
  exit 0: wrote 33 obligations and 96 typed edges; denominator 1a92339a...2af8
  a second run reproduced all three generated files byte for byte

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH_PINNED=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0043
LEAN_PATH="$LEAN_PATH_PINNED" "$LEAN_BIN" -o /tmp/.../Statement.olean Statement.lean
LEAN_PATH="/tmp/...:$LEAN_PATH_PINNED" "$LEAN_BIN" ObligationTree.lean
  exit 0: the target and conditional composition elaborated; the composition reported exactly
  [propext, Classical.choice, Quot.sound]; its stdout SHA-256 was c208c1bf...2635;
  all temporary output was removed

python3 -B Stage1_Instances/THM-M-0043/check_statement.py
  exit 0: expression a46ee239...557a, source fingerprint, minimal imports, two checked
  transports, and all four statement mutations passed

python3 -B Stage1_Instances/THM-M-0043/check_obligation_tree.py
  exit 0: PASS THM-M-0043 obligation tree: 33 obligations, 96 typed edges;
  root closure open H1/M3/R4 and external Atlas M1 route uninstalled

python3 -m json.tool <all owned JSON and .stage1-worker-selftest.json>
  exit 0: all structured artifacts are valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0043-obligation-pycache \
  python3 -m py_compile <all five owned Python validators/generator>
  exit 0: all Python files compiled outside the repository tree

rg -n -i --glob '*.lean' <prohibited proof/oracle markers> \
  Stage1_Instances/THM-M-0043/ObligationTree.lean
  exit 1: expected no-match result

git diff --check -- Stage1_Instances/THM-M-0043 .stage1-worker-selftest.json
  exit 0: no whitespace errors; no-index checks cover untracked files
```

## Status Boundary

`ObligationTree.lean` checks only a conditional adapter whose exact external child is an explicit
premise. It does not install the Atlas body. That body remains M1/E2 and requires a license/reuse
decision or independent local implementation, full transitive provenance/trust, proof-phase
integration, and master acceptance. Accepted proof state is empty and the root stays
`[H1, M3, R4]`; H0, R0, audit completion, validation, independent verification, release, and
theorem completion remain open.
