# THM-M-0045 proof-phase validation

Item: `S56-M-0045-PROOF`. Base revision:
`9a1ce196889e32911beeeffa685084b48a969866`.

## Implemented proof route

`SchurPort.lean` ports the audited 300-line Schur construction from immutable mathlib branch
revision `0a539f0ce764fd16726509b62ed7b870461070eb` to the repository's current mathlib pin. It keeps
the recursive eigenvalue/eigenspace split, orthogonal-complement compression, strict finrank
descent, collected orthonormal basis, four below-diagonal entry cases, unitary basis matrix, and
final factorization. Compatibility changes replace APIs removed since the historical branch; the
target and mathematical construction are unchanged. The historical Apache-2.0 header is retained.

`Proof.lean` specializes the construction to `Matrix (Fin n) (Fin n) Complex`, supplies the exact
frozen `SchurEquationPackage`, and applies `ObligationTree.root_of_equationPackage` to derive the
unchanged `SchurTriangularizationTarget`. The local terminal body realizes all 31 required-machine
obligations in registry version 1. Wrappers and projections do not receive duplicate body credit.

This proof phase provides a repo-local kernel-closed exact-root candidate. `M0-L` still requires
the downstream validation node and dependency-ordered master acceptance. This proof-phase receipt
does not claim theorem completion.

## Commands and results

Validation ran on 2026-07-13 (`Asia/Shanghai`). The existing pinned `.lake` symlink was reused
read-only. No Lake update/build, dependency clone/fetch, checkout, or `.lake` mutation was run.

```text
bash Stage1_Instances/THM-M-0045/check_proof.sh
  exit 0: isolated Statement, ObligationTree, SchurPort, and Proof elaboration passed; both proof
  declarations were sorry-free and reported exactly [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0045
  exit 0: rank 1085, planned, L0/rework_required, theorem_complete=false

python3 -B Stage1_Instances/THM-M-0045/check_proof.py
  exit 0: exact source, target, denominator, lineage, pins, receipt, worker packet, and status passed

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0045/Proof.lean Stage1_Instances/THM-M-0045/SchurPort.lean
  exit 1 with empty output: expected pass, no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0045/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both files are valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0045-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0045/check_proof.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-0045 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The accepted instance remains `[H1, M3, R4]` with empty accepted proof state until integration.
`M0045-S-FOUNDATION`, H0, R0, complete transitive provenance and trust, validation, hermetic replay,
independent verification, release, `AUDIT-Z`, and `THEOREM-Z` remain downstream.
