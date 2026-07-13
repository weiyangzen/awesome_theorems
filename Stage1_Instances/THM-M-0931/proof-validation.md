# THM-M-0931 proof-phase validation

Item: `S56-M-0931-PROOF`. Base revision:
`5931467f7eefac7a6e57777cc3082e4a2edc03d4` (tree
`45a10c953e5dc79c1eb9ae7d755ee84866717775`).

## Implemented proof

`Proof.lean` installs manifest-pinned mathlib's `Int.erdos_ginzburg_ziv` at the
frozen indexed interface, composes it through the target-owned occurrence
enumeration to obtain the at-least-count multiset anchor, and consumes the
frozen root and exact-count compositions to prove
`Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget`. A second wrapper checks the
same exact target directly through `Int.erdos_ginzburg_ziv_multiset` and the
equality-to-lower-bound implication. The two root wrappers share one pinned
proof route and do not duplicate proof-body credit.

Lean reports the three public upstream declarations and all six target-owned
declarations sorry-free. Every axiom report is exactly `propext`,
`Classical.choice`, and `Quot.sound`. The proof source contains no `sorry`,
`admit`, added axiom, `sorryAx`, opaque or unsafe declaration, native oracle,
external implementation, or weakened target.

This is provisional proof-phase evidence for an `M0-W` exact-root proposal. It
does not claim theorem completion. The exact checked proof graph maps the root,
terminal composition, count transport, multiset anchor, occurrence enumeration,
and indexed engine. The six internal prime/composite source-body decomposition
plans still lack separate abstract-child composition certificates; this receipt
therefore gives them no individual closure credit. The accepted dossier remains
`[H1, M3, R4]` with zero accepted obligations.

## Commands and results

Validation ran on 2026-07-13 (`Asia/Shanghai`) using the automation-provided
canonical pinned `.lake` symlink read-only. No `lake update`, `lake build`,
dependency clone/fetch, network access, or `.lake` mutation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0931
  exit 0: rank 1470, planned, L0/rework_required,
  theorem_complete=false

bash Stage1_Instances/THM-M-0931/check_proof.sh
  exit 0: temporary isolated Statement.olean and ObligationTree.olean built;
  Proof.lean elaborated; all nine declarations were sorry-free and reported
  exactly [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0931/check_proof.py
  exit 0: exact target, source/body pins, graph and composition boundary,
  receipt hashes, placeholder policy, and worker packet passed

python3 -B Stage1_Instances/THM-M-0931/build_obligation_artifacts.py --check
  exit 0: frozen 32-obligation registry, 46 typed edges, and validation
  specification matched deterministic regeneration

python3 -B Stage1_Instances/THM-M-0931/check_obligation_tree.py
  exit 1: the historical predecessor checker pins its original base revision
  b243ebc0... rather than the integrated proof-task base 5931467f...; it
  stopped at that revision assertion before its scoped checks. The frozen
  artifacts were instead checked by deterministic regeneration above and by
  the proof checker without modifying this predecessor-owned receipt checker.

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0931-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0931/check_proof.py
  exit 0: checker syntax compiled outside the repository

python3 -m json.tool Stage1_Instances/THM-M-0931/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for both structured artifacts

git diff --check -- Stage1_Instances/THM-M-0931 \
  .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The prerequisite obligation-tree packet and this proof packet still require
dependency-ordered master acceptance. H0, R0, complete transitive provenance
and TCB acceptance, validation, cold hermetic replay, independent verification,
release, `AUDIT-Z`, and `THEOREM-Z` remain open.
