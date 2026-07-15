# THM-M-1356 obligation-tree validation

Item: `S56-M-1356-OBLIGATION_TREE`

Base revision: `431e77db6367a2eda83060b7212cb490d11ca39f`
(tree `7ed0ffdf78a9b7a5d8d474b30aca0d8809c1d087`)

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 50 unique obligations before proof-phase closure credit. The canonical
ten-field projection has SHA-256
`300ea224caca3f6236a9f40f1d56782d498862c5f12d4e1d4b414622163e6560`. The bundle has 335
typed edges across separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. Its 122 structured ledger entries expand Barkovsky's Theorem 40 route through
Hermite root counting, Cauchy indices, Sturm/Routh construction and terminal cases, no-pivot
Gaussian elimination, the leading-minor product identity, both implications, and exact root
assembly.

`ObligationTree.lean` kernel-checks only the two final abstract-child composition layers. Both
Routh-Hurwitz directions remain explicit premises. The axiom report is `[propext,
Classical.choice, Quot.sound]`, inherited while unfolding the noncomputable statement definitions;
there is no terminal proof body and no custom axiom. All substantive proof nodes remain open.

Validation reused only the existing manifest-pinned Lake artifacts. No `lake update`, `lake build`,
dependency clone/fetch, or other `.lake` mutation was run.

## Commands and results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546
  uniform-L0 Lean 4 targets, and the execution skill passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1356
  exit 0: rank 966, planned, L0/rework_required, theorem_complete false

python3 Stage1_Instances/THM-M-1356/build_obligation_artifacts.py
  exit 0: wrote 50 obligations, 335 typed edges, and 122 ledger steps
  denominator: 300ea224caca3f6236a9f40f1d56782d498862c5f12d4e1d4b414622163e6560

python3 -B Stage1_Instances/THM-M-1356/check_obligation_tree.py
  exit 0: PASS THM-M-1356 obligation tree: 50 obligations, 335 typed edges,
  122 ledger steps; deterministic regeneration, registry/graph/recipe schemas,
  exact conditional Lean composition, pins, open H1/M3/R4 root, and receipt agree

(cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1356/Statement.lean)
  exit 0: exact target, checked coefficient adapters, definitional transport,
  four expected mutation rejections, and explicit target expression elaborated

(cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1356/AnchorAudit.lean)
  exit 0: every selected pinned polynomial/root/matrix support declaration elaborated

(cd Formalizations/Lean &&
  python3 ../../Stage1_Instances/THM-M-1356/check_statement.py)
  exit 0: expression hash 7901eb74686f457348ec06812b8584c69eb09649779637cbb28b2e7bd84b98bf,
  all four mutations, three minimal imports, and pinned mathlib revision passed

python3 -B Stage1_Instances/THM-M-1356/check_anchor_audit.py
  exit 0: exact local statement only; pinned mathlib topic inventory empty;
  external candidate inventory empty; root M3
```

The obligation checker additionally obtains the pinned Lean executable and `LEAN_PATH` via
`lake env`, compiles `Statement.lean` to a temporary directory, elaborates `ObligationTree.lean`
against that temporary module, checks all three axiom reports, and deletes the directory. It checks
the current repository commit/tree, clean pinned mathlib commit/tree, statement and anchor input
hashes, 50 canonical records and frozen denominator lists, every required node field, unique
substantive step IDs, readable anchors, all adjacency indexes, graph endpoint namespaces,
graph-specific acyclicity, reciprocal proof edges, the exact three checked `composes` edges, 31
explicitly unverified internal decomposition plans, structured per-node recipe coverage, and a
comment-aware prohibited-construct scan.

Final JSON, Python compilation, deterministic-regeneration, hygiene, and whitespace commands are
recorded in the worker receipt and root self-test after their exact final runs.

## Status boundary

This is dirty-tree, warm, nonrelease worker evidence pending dependency-ordered master acceptance.
No obligation is accepted closed. The root stays `[H1, M3, R4]`; the two exact directional packages
are the open root cut. Source `H0`, readable `R0`, proof bodies, internal composition certificates,
provenance/foundation/TCB closure, hermetic replay, independent verification, audit completion,
release validation, and theorem completion remain open.
