# THM-M-0043 proof-phase validation

Item: `S56-M-0043-PROOF`. Base revision:
`75ab5edd624df749325d391b41b669f8d72774b2`.

## Implemented proof route

`Proof.lean` supplies a repo-local proof of the exact finite complex normal-matrix target. It first
proves that two commuting Hermitian matrices have a common orthonormal eigenbasis using the pinned
joint-eigenspace decomposition and subordinate-basis lemmas. The resulting basis matrix is unitary,
and a pointwise eigenvector calculation gives the required conjugated-diagonal equation.

For a normal matrix `A`, the local proof constructs its Hermitian real and imaginary parts `H` and
`K`, proves `A = H + I * K`, and derives `H * K = K * H` from normality. It installs this result at
the frozen `ExactConjugatedDiagonalAnchor` interface and applies
`root_of_exactConjugatedDiagonalAnchor` to close the unchanged canonical root. This realizes all 23
proof-reachable obligations in registry version 1 without changing the denominator. The audited
Atlas source is neither imported nor vendored and receives no proof-body credit.

The implementation follows the Atlas-informed architecture frozen by the prior obligation phase,
but it imports only pinned mathlib and does not vendor or import the audited Atlas file. Architecture
reuse and provenance review remain downstream. This phase establishes a repo-local kernel-closed
exact-root body. `M0-L` remains a downstream candidate pending E0 validation and dependency-ordered
master acceptance. It does not claim theorem completion.

## Commands and results

Validation ran in the worker clone on 2026-07-13 (Asia/Shanghai). The existing canonical pinned
`.lake` symlink was reused read-only; no Lake update/build, dependency clone/fetch, or `.lake`
mutation was performed.

```text
bash Stage1_Instances/THM-M-0043/check_proof.sh
  exit 0
  isolated Statement.olean and ObligationTree.olean elaborated in a temporary directory; all three
  local proof declarations were sorry-free and reported exactly
  [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0043
  exit 0: rank 1083, planned, L0/rework_required, theorem_complete=false

python3 -B Stage1_Instances/THM-M-0043/check_proof.py
  exit 0: exact source, target, denominator, pins, composition, receipt, worker packet, and status
  boundary passed

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0043/Proof.lean
  exit 1 with empty output: expected pass, no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0043/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both files are valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0043-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0043/check_proof.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-0043 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The accepted instance remains `[H1, M3, R4]` with empty accepted proof state until the integration
lane acts. `M0043-S-FOUNDATION`, H0, R0, Atlas-informed architecture reuse review, complete
transitive provenance and trust, validation, hermetic replay, independent verification, release,
`AUDIT-Z`, and `THEOREM-Z` remain downstream.
