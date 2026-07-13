# THM-M-1003 proof-phase validation

Item: `S56-M-1003-PROOF`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`.

## Implemented proof

`Proof.lean` closes the exact
`Stage1Instances.THM_M_1003.LpMartingaleConvergenceTarget` frozen by
`Statement.lean`. It first derives a uniform `L^1` bound from the supplied
uniform `L^p` bound and uses the pinned martingale convergence declarations to
construct the common almost-everywhere `MemLp` limit. For norm convergence it
reconstructs arbitrary finite-exponent conditional-expectation contraction
from conditional Jensen, proves the increasing-filtration approximation by
bounded simple-function density, and supplies the uniform-integrability bridge
needed for the conditional-expectation representation. Almost-everywhere
uniqueness transports the result from mathlib's canonical `limitProcess` to
every candidate consumed by the frozen composition theorem.

The resulting local declaration `Proof.target` has exactly the canonical root
type. All thirteen checked declarations are sorry-free and report only
`propext`, `Classical.choice`, and `Quot.sound`. This is therefore a provisional
`M0-L` proof route pending master acceptance. This proof phase does not claim
theorem completion: foundation/TCB, source, provenance, readable
reconstruction, hermetic replay, independent validation, and release remain
later gates.

## Commands and results

Commands ran in this worker clone on 2026-07-14 (Asia/Shanghai). The isolated
Lean runner copied only `Statement.lean`, `ObligationTree.lean`, and
`Proof.lean` to a temporary directory. It used Lake only to locate the pinned
Lean executable and `LEAN_PATH`, invoked Lean directly with
`LEAN_NUM_THREADS=1`, and removed the temporary output. The canonical `.lake`
symlink and pinned artifacts were reused without mutation. No update, build,
clone, fetch, or network operation ran.

```text
bash Stage1_Instances/THM-M-1003/check_proof.sh
  exit 0: isolated Statement, ObligationTree, and Proof elaboration passed;
  all thirteen declarations were sorry-free and reported exactly
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-1003/check_proof.py
  exit 0: frozen target/registry/graph identity, source markers, input hashes,
  mathlib pin, receipt, worker packet, hygiene, and dirty-scope checks passed

python3 Stage1_Instances/THM-M-1003/check_statement.py
  exit 0: canonical statement and all four structural mutations elaborated and
  retained distinct explicit-expression hashes

python3 Stage1_Instances/THM-M-1003/check_obligation_tree.py
  exit 0: 16 frozen obligations and 37 typed edges passed; its pre-proof M4
  observation remains immutable and is not used as current proof status

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets and ranks passed

python3 scripts/stage1_target.py show THM-M-1003
  exit 0: rank 283, planned, L0/rework_required, theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1003/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured artifacts parse

git diff --check -- Stage1_Instances/THM-M-1003 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The integration lane must independently rerun and accept this provisional
packet in dependency order before changing authoritative state.
