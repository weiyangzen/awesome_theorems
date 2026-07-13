# THM-M-0276 obligation-tree validation

Item: `S56-M-0276-OBLIGATION_TREE`.

Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e`.

Base tree: `b4b092069141ac54ea1ab5a6ea946192a30ec78c`.

Validation date: `2026-07-13` (`Asia/Shanghai`).

## Scope

Registry version 1 freezes 29 canonical obligations before proof-phase closure credit. It follows
the literal pinned source through the Real and Complex specializations, the final open-image
argument, exact controlled preimages, residual iteration and summation, approximate preimages,
Baire category, rescaling, and paired closure witnesses. The graph bundle contains 180 edges in
seven separate graph families and 58 substantive ledger steps, all with budgets at most 100.

The narrow Lean harness exposes the polymorphic semilinear proposition, inhabits it with the pinned
`ContinuousLinearMap.isOpenMap`, specializes it to the exact same-field branches, and composes the
root. A checked `Iff.rfl` links that local root to a fully expanded expression whose serialized
SHA-256 equals the statement-phase fingerprint `0cfb9796...82fa`. This is interface and
architecture evidence, not proof-phase installation or accepted closure.

## Commands and results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  ok: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0
  ok: 1546 unique targets; execution ranks 1 through 1546; all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0276
  exit 0
  THM-M-0276 rank 1282, planned, L0/rework_required, theorem_complete=false

python3 -B Stage1_Instances/THM-M-0276/build_obligation_artifacts.py
  exit 0
  wrote 29 obligations, 180 typed edges, and 58 substantive ledger steps
  registry denominator sha256: 1437a03a...710c8
  a second generation produced byte-identical registry, graphs, specs, and Markdown

python3 -B Stage1_Instances/THM-M-0276/check_obligation_tree.py \
  --worker-packet .stage1-worker-selftest.json
  exit 0
  PASS THM-M-0276 obligation tree: 29 obligations, 180 typed edges,
  58 substantive ledger steps
  exact terminal/adapter/root and expression transport elaborated with zero closed obligations;
  accepted root remains H2/M3/R4 and theorem_complete=false

cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 \
  ../../Stage1_Instances/THM-M-0276/Statement.lean
  exit 0
  exact statement and five structural mutations re-elaborated

cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 \
  ../../Stage1_Instances/THM-M-0276/AnchorAudit.lean
  exit 0
  exact pinned candidate and helpers remained sorry-free with only
  propext, Classical.choice, and Quot.sound

python3 -m json.tool on owned JSON files and .stage1-worker-selftest.json
  exit 0
  all structured artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0276-obligation-pycache python3 -m py_compile \
  Stage1_Instances/THM-M-0276/build_obligation_artifacts.py \
  Stage1_Instances/THM-M-0276/check_obligation_tree.py
  exit 0

scoped prohibited Lean construct scan
  exit 1 (expected no match)
  no sorry, admit, sorryAx, custom axiom/constant, unsafe/opaque declaration,
  implemented_by/extern boundary, or native_decide in ObligationTree.lean

git diff --check -- Stage1_Instances/THM-M-0276 .stage1-worker-selftest.json
  exit 0; no output
  per-new-file no-index checks also returned no whitespace diagnostic
```

All Lean checks used the existing pinned toolchain and automation-provided `.lake` symlink. No
`lake update`, `lake build`, dependency clone, fetch, checkout, or `.lake` mutation ran.

## Open boundary

The exact mathlib candidate remains unaccepted `M1/E2` evidence and no obligation is closed.
Fourteen internal source-body decompositions require exact child-to-parent certificates; the root
child fingerprints remain planned signatures pending declaration-type extraction. The H2 lecture
notes retain the printed unit-ball-versus-radius-`n` Baire-cover gap. H0 correction and independent
review, readable R0, full provenance and compiled/executable TCB closure, proof installation,
hermetic replay, independent verification, deterministic release evidence, master acceptance,
`AUDIT-Z`, and theorem completion remain open.
