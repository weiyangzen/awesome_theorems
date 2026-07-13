# THM-M-0741 proof-phase validation

Item: `S56-M-0741-PROOF`. Base revision:
`72e9e8092182121a6794921f61fcc9cae22f726d`.

## Implemented proof

`Proof.lean` installs pinned mathlib's `ComputablePred.rice` at the frozen
`RiceBridge` interface and checks the fixed-input theorem both directly through
`ComputablePred.halting_problem 0` and by replaying the frozen Rice/witness
composition. It constructs the computable section `code -> (code, 0)`, restricts
both components of a hypothetical `ComputablePred` pair decider, and consumes
the frozen child-to-parent compositions to prove the exact
`HaltingProblemUndecidable` target from `Statement.lean`.

All seven required-machine obligations in registry version 1 therefore have
provisional proof bodies. The direct fixed-input wrapper and the explicit Rice
replay deduplicate to one pinned terminal route. This supports an `M0-W` route
proposal after master acceptance, but the accepted state remains `H1/M3/R4`.
This proof phase does not claim theorem completion: `M0741-S-FOUNDATION` and
the source, provenance, trust, readability, workflow, validation, and release
gates remain open.

## Commands and results

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). The isolated
Lean runner copied only the three target modules to a temporary directory,
compiled temporary `Statement.olean` and `ObligationTree.olean` files, placed
that directory before the pinned `LEAN_PATH`, and removed it on exit. Existing
canonical pinned `.lake` artifacts were reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation ran.

```text
bash Stage1_Instances/THM-M-0741/check_proof.sh
  exit 0: ComputablePred.rice, ComputablePred.halting_problem, all four
  target-local bridge/reduction declarations, and both exact roots elaborated;
  all eight declarations were sorry-free and reported exactly
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0741/check_proof.py
  exit 0: exact source markers, frozen target and graph, receipt/input hashes,
  mathlib pin/body hashes, worker packet, placeholder policy, and dirty-scope
  boundary passed

python3 -B Stage1_Instances/THM-M-0741/check_obligation_tree.py
  exit 1: the predecessor checker remains bound to its original worker base
  revision; the integration lane has since advanced HEAD while preserving the
  statement, registry, graph, and obligation-tree hashes rechecked above

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets and ranks passed

python3 scripts/stage1_target.py show THM-M-0741
  exit 0: rank 1329, planned, L0/rework_required, theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-0741/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured artifacts parse

git diff --check -- Stage1_Instances/THM-M-0741 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The receipt is provisional worker evidence only. The integration lane must
independently re-elaborate and accept it in dependency order before changing
authoritative state.
