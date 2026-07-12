# THM-M-1333 validation-phase record

Item: `S56-M-1333-VALIDATION`. Base revision:
`e9252b1cfdc99a094324c8a10d260769df2eca15`.

## Validated scope

The validator replays `Statement.lean`, `ObligationTree.lean`, and `Proof.lean`
from copied sources in a fresh temporary module directory. It checks the
frozen statement, registry denominator, proof-receipt input hashes, proof-body
hash, pinned clean mathlib revision, placeholder/axiom/unsafe hygiene, and
reported axiom closure. `Validation.lean` independently reconstructs the
zero-dimensional branch and conditional dimension assembly without importing
`Proof` or `ObligationTree`.

This is narrow worker validation, not independent release verification. The
positive-dimensional proof is absent, the exact root is open, and the run
uses the shared warm pinned `.lake` cache.

## Commands and results

All commands ran from the worker-clone root on 2026-07-12. No update, build,
fetch, clone, network access, or `.lake` mutation was performed.

```text
python3 Stage1_Instances/THM-M-1333/check_validation.py
  exit 0
  PASS narrow kernel replay
  PASS trust observation: propext, Classical.choice, Quot.sound; no sorryAx
  PASS local provenance and clean pinned mathlib
  PASS same-worker differential probe
  OPEN exact root: positive-dimensional route has no proof body
  BLOCKED hermetic and distinct-runner release gates

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1333
  exit 0: rank 874, planned, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-1333/validation-spec.json \
  Stage1_Instances/THM-M-1333/validation-receipt.json
  exit 0: both JSON artifacts parse

git diff --check -- Stage1_Instances/THM-M-1333 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Failed gates and boundary

The first failed theorem gate is `proof.root_kernel_closure`. The minimal
mathematical cut contains delayed-Euler construction, invariants, compact
extraction, passage to the integral equation, and derivative recovery. The
frozen graph also predates proof-phase partial closure and awaits master-only
reconciliation.

Cold empty-cache offline replay, full TCB/SBOM and license closure, archive
restoration, a second platform, distinct verifier identity, independently
provisioned runner, second signature, and an independently implemented release
verifier were not available in this worker clone. Accordingly `audit_complete`
and `theorem_complete` are both false; this receipt is nonrelease provisional
evidence only.
