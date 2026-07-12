# THM-M-0474 obligation-tree validation

Item: `S56-M-0474-OBLIGATION_TREE`

Base revision: `531673f2e97293dd22e5727b12fc7e13eca7d6e5`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen Result

Registry version 1 freezes 21 unique obligations before proof-phase installation. The canonical
ten-field projection has SHA-256
`28dd518db2fe79a5006cbeb3fdd51b379f67cf388960c3f5fafdf2a7ad8b6a9e`.
The bundle contains 43 edges across separate proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. Its proof DAG expands the visible pinned source route from the
natural wrapper through the integer and `ZMod` theorems, finite-field unit construction, and finite
group cardinality theorem. Each proof requirement has a reciprocal composition edge, and all
semantic ledgers have budgets at most 60 steps.

The exact validation commands and results are recorded below after the scoped self-test. Validation
uses only the existing manifest-pinned Lake artifacts. No Lake update or build, dependency clone or
fetch, or other `.lake` mutation is permitted or performed.

## Commands And Results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0474
  exit 0: rank 938, planned, L0/rework_required, theorem_complete false

python3 Stage1_Instances/THM-M-0474/build_obligation_artifacts.py
  exit 0: wrote 21 obligations and 43 typed edges
  denominator: 28dd518db2fe79a5006cbeb3fdd51b379f67cf388960c3f5fafdf2a7ad8b6a9e
  a second run produced byte-identical registry, graph, and recipe files

python3 Stage1_Instances/THM-M-0474/check_obligation_tree.py
  exit 0: PASS THM-M-0474 obligation tree: 21 obligations, 43 typed edges
  root closure: open (H1/M3/R4); exact pinned anchor remains the proof-phase cut

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0474
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean Statement.ilean
  exit 0: the canonical statement re-elaborated; the exact Nat theorem type printed;
  root_of_exactNatAnchor elaborated and reported [propext]; temporary outputs removed

python3 Stage1_Instances/THM-M-0474/check_anchor_audit.py
  exit 0: seven immutable candidates, exact source chain, pins, hashes, trust boundary,
  and fail-closed status passed under the downstream handoff

cd Formalizations/Lean &&
  python3 ../../Stage1_Instances/THM-M-0474/check_statement.py
  exit 0: expression and source fingerprints, checked transport, minimal imports, and four
  statement mutations passed

python3 Stage1_Instances/THM-M-0474/check_intake.py
  exit 0: planned H1/M3/R4 dossier with six open local tasks passed

python3 -m json.tool <each owned JSON and .stage1-worker-selftest.json>
  exit 0: all structured artifacts are valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0474-obligation-pycache \
  python3 -m py_compile <five owned Python files>
  exit 0: validators and generator compile outside the repository tree

rg -n -i --glob '*.lean' <prohibited proof/oracle markers> \
  Stage1_Instances/THM-M-0474/ObligationTree.lean
  exit 1: expected no-match result

git diff --check -- Stage1_Instances/THM-M-0474 .stage1-worker-selftest.json
  exit 0: no tracked whitespace diagnostics; per-new-file no-index checks were also empty
```

The structural checker additionally validates the authoritative item identity and ownership,
frozen input hashes, canonical denominator, pending-review exclusion reasons, every required node
field, node/obligation bijection, all graph adjacency indices, edge endpoint legality, acyclicity,
reciprocal proof edges, exact proof-DAG reachability, recipe coverage, open closure, owned artifact
inventory, provisional receipt, and root handoff changed-path equality.

## Status Boundary

`ObligationTree.lean` validates only a conditional composition theorem whose exact natural anchor
is an explicit premise. It does not install the audited mathlib theorem. The root therefore remains
`[H1, M3, R4]`; accepted proof state is empty, and H0, R0, complete provenance/trust, audit
completion, validation, independent verification, release, and theorem completion remain open.
This worker packet is provisional and still requires dependency-ordered master acceptance.
