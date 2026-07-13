# Intake validation

## Scope

This record validates only the `planned` intake: manifest membership, repository-source
provenance, source-statement ambiguity, scope and non-substitution boundaries, the open downstream
task DAG, and elaboration of adjacent pinned Lean APIs. It does not validate a canonical
mathematical statement, a hyperbolic-triangle encoding, a proof body, H0/M0/R0, audit completion,
theorem completion, or release assurance.

The worker environment is nonrelease because the automation-provided `Formalizations/Lean/.lake`
symlink and the owned intake files are untracked. The existing canonical pinned `.lake` artifacts
were used read-only. No update, build, clone, fetch, or dependency mutation was performed.

## Structured recipes

```json
{
  "recipe_id": "S56-M-0215-INTAKE-RECIPE-STRUCTURE",
  "cwd": ".",
  "argv": ["python3", "-B", "Stage1_Instances/THM-M-0215/check_intake.py", "--worker-packet", ".stage1-worker-selftest.json"],
  "env_allowlist": {},
  "timeout_seconds": 120,
  "network_policy": "denied",
  "expected_exit": 0,
  "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact_bytes_sha256"}],
  "covered_obligation_ids": ["S56-M-0215-INTAKE"],
  "covered_declarations": []
}
```

```json
{
  "recipe_id": "S56-M-0215-INTAKE-RECIPE-LEAN-PROBE",
  "cwd": "Formalizations/Lean",
  "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0215/IntakeProbe.lean"],
  "env_allowlist": {},
  "timeout_seconds": 120,
  "network_policy": "denied",
  "expected_exit": 0,
  "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact_bytes_sha256"}],
  "covered_obligation_ids": ["S56-M-0215-INTAKE"],
  "covered_declarations": [
    "Real.sinh",
    "Real.cosh",
    "Real.cosh_sub",
    "Real.cosh_sq_sub_sinh_sq",
    "UpperHalfPlane",
    "UpperHalfPlane.dist_eq",
    "UpperHalfPlane.cosh_dist",
    "InnerProductGeometry.norm_sub_sq_eq_norm_sq_add_norm_sq_sub_two_mul_norm_mul_norm_mul_cos_angle"
  ]
}
```

## Results

Validation on 2026-07-13 Asia/Shanghai used repository base
`62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`, Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0215` | 0 | rank 1230, planned, no accepted legacy artifact, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0215/IntakeProbe.lean` | 0 | eight adjacent pinned APIs elaborated; no target or proof body declared |
| `python3 -B Stage1_Instances/THM-M-0215/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | planned identity, pins, null formal target, boundaries, receipt, worker packet, and six open tasks agree |
| scoped prohibited-token scan of `*.lean` | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace/diff check | 0 | no whitespace errors |

The structural checker and final artifact hashes are represented in the provisional node receipt.
That receipt is mutable worker evidence, not content-addressed master acceptance.

## Open gates

An approved exact source proposition, source identity, historical and errata audit, independent
review, model and curvature normalization, triangle and angle definitions, cyclic packaging,
degenerate-case policy, canonical Lean expression and environment fingerprint, checked transports,
statement mutations, exhaustive anchor audit, obligation registry, typed graphs, proof,
composition, provenance/trust closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, and master acceptance remain open. These gates do not invalidate
a truthful self-tested `planned` intake.
