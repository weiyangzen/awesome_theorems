# Intake validation record

Base revision: `93c99233108bb249d1bca807a3a56a2b63e0cd54`.

The pre-existing worktree contained the untracked symlink `Formalizations/Lean/.lake`, pointing to
the canonical pinned artifacts. This intake did not modify it. The run is therefore scoped worker
evidence, not clean release evidence.

## Commands and results

The following commands were run from the repository root on 2026-07-12 (Asia/Shanghai):

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
[exit 0]

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
[exit 0]

$ python3 scripts/stage1_target.py show THM-M-0164
{
  "execution_rank": 663,
  "legacy_priority_slot": null,
  "theorem_id": "THM-M-0164",
  "name": "雅可比场理论",
  "category": "几何学 / 微分几何",
  "source_status_untrusted": "已验证",
  "baseline": "L0",
  "rework_required": true,
  "legacy_artifacts_accepted": false,
  "target_lane": "hard_statement_first_partial_verification",
  "intake_score": 130,
  "lifecycle_mode": "planned",
  "theorem_complete": false
}
[exit 0]
```

The dossier-local syntax, identity, reference, and whitespace checks are recorded after creation in
the final section below. No `lake env lean` command is claimed: intake creates a planned target, and
the exact Lean expression and minimal imports are intentionally the dependent statement phase's
open gate. Running an unrelated Lean theorem would not validate this intake.

## Status boundary

These checks validate the intake artifact shape and target membership only. Accepted receipt IDs:
none. First failed theorem gate: exact statement elaboration and environment fingerprint. Remaining
root cut set begins with `STATEMENT`; audit and theorem completion are both false.

## Dossier-local checks

```text
$ python3 -m json.tool Stage1_Instances/THM-M-0164/intake.json >/dev/null
[exit 0]

$ python3 <scoped assertions over intake identity, planned/open state, root vector, and referenced files>
intake-local-check: ok (planned scope, open statement gate, 3 referenced public/evidence artifacts)
[exit 0]

$ git diff --check -- Stage1_Instances/THM-M-0164
[no output; exit 0]
```
