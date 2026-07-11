# THM-M-0107 validation-phase record

Item: `S56-M-0107-VALIDATION`

Base revision: `76372ddac1d95a5ffa1297c04b611369fc9c9843`

Validation timestamp: `2026-07-11T20:15:34Z`

## Scope and verdict

The structured recipe reruns the exact statement, conditional composition, and
the proof phase's open-factor and factorization-equation bodies. It checks the
frozen hashes, mathlib pin and cleanliness, local placeholder policy, and the
Lean axiom reports. The fresh temporary module directory prevents target-local
`.olean` reuse, while the canonical pinned mathlib cache is reused unchanged.

This is warm, node-scoped kernel evidence only. The exact root remains open:
`exactTarget_of_normalization_finite` requires the family
`IsFinite f.fromNormalization`, and the pinned closure supplies integrality but
does not discharge the frozen integral-to-finite bridge. Consequently
`M0107-L-FINITE` and `M0107-L-INTEGRAL-TO-FINITE` remain the root cut set and
the root machine debt remains `M3`.

## Commands and results

Commands ran in the worker clone on 2026-07-12 (Asia/Shanghai). No update,
build, clone, fetch, or dependency mutation was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0107
  exit 0: execution rank 31; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0107/check_validation.py
  exit 0: statement, composition, and proof declarations re-elaborated;
  frozen hashes, prohibited-token scan, allowed axioms, pinned clean mathlib,
  and explicit open-root boundary passed

python3 -m json.tool Stage1_Instances/THM-M-0107/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0107/validation-receipt.json
  exit 0: both structured artifacts are valid JSON

git diff --check -- Stage1_Instances/THM-M-0107 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The cold empty-cache/offline hermetic gate cannot pass in this worker protocol,
which explicitly reuses the shared canonical `.lake` artifacts. The independent
release gate also cannot pass in one mutable workspace: there is no separately
provisioned runner, distinct verifier identity, independently implemented
minimal release verifier, or second signed attestation. These are recorded as
failed gates rather than simulated. `audit_complete=false` and
`theorem_complete=false`; no release or master acceptance is claimed.
