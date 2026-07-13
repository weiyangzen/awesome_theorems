# Intake validation

## Scope

This record validates only the `planned` intake: manifest membership, repository-source
provenance, source-statement ambiguity, scope and non-substitution boundaries, the open downstream
task DAG, and elaboration of adjacent pinned Lean APIs. It does not validate a canonical
mathematical statement, a singular-integral operator or kernel, a proof body, H0/M0/R0, audit
completion, theorem completion, or release assurance.

The worker environment is nonrelease because the automation-provided `Formalizations/Lean/.lake`
symlink and the owned intake files are untracked. The existing canonical pinned `.lake` artifacts
were used read-only. No update, build, clone, fetch, or dependency mutation was performed. Network
was used only for bibliographic discovery before the reproducible denied-network validation
recipes; its mutable response is not source-paper or release evidence.

## Structured recipes

```json
{
  "recipe_id": "S56-M-0299-INTAKE-RECIPE-STRUCTURE",
  "cwd": ".",
  "argv": ["python3", "-B", "Stage1_Instances/THM-M-0299/check_intake.py", "--worker-packet", ".stage1-worker-selftest.json"],
  "env_allowlist": {},
  "timeout_seconds": 120,
  "network_policy": "denied",
  "expected_exit": 0,
  "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact_bytes_sha256"}],
  "covered_obligation_ids": ["S56-M-0299-INTAKE"],
  "covered_declarations": []
}
```

```json
{
  "recipe_id": "S56-M-0299-INTAKE-RECIPE-LEAN-PROBE",
  "cwd": "Formalizations/Lean",
  "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0299/IntakeProbe.lean"],
  "env_allowlist": {},
  "timeout_seconds": 120,
  "network_policy": "denied",
  "expected_exit": 0,
  "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact_bytes_sha256"}],
  "covered_obligation_ids": ["S56-M-0299-INTAKE"],
  "covered_declarations": [
    "MeasureTheory.Measure",
    "MeasureTheory.Measure.restrict",
    "MeasureTheory.MemLp",
    "MeasureTheory.Lp",
    "MeasureTheory.integral",
    "ContinuousLinearMap",
    "ContinuousLinearMap.mk"
  ]
}
```

## Results

Validation on 2026-07-13 Asia/Shanghai used repository base
`940588d30669014430d5a1beb187f2bca118e816`, Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0299` | 0 | rank 1303, planned, no accepted legacy artifact, theorem incomplete |
| `curl -L --fail --silent --show-error -H 'Accept: application/vnd.citationstyles.csl+json' 'https://doi.org/10.1007/BF02392130'` | 0 | bibliography identifies Calderon/Zygmund, title, *Acta Mathematica* 88 (1952), pages 85-139; response SHA-256 `5af86351...8602`; article text was inaccessible, and no paper-content evidence is claimed |
| `rg -n -i 'calder[oó]n\|zygmund\|singular.?integral\|weak.?type\|riesz.?transform\|maximal.?trunc\|hilbert.?transform' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1, expected no match | no name-level exact-topic declaration; not an exhaustive anchor audit |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0299/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated; no target or proof body declared |
| `python3 -B Stage1_Instances/THM-M-0299/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | planned identity, pins, null formal target, boundaries, receipt, worker packet, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0299 --glob '*.lean'` | 1, expected no match | no prohibited declaration or proof escape |
| `git diff --check` and `for f in Stage1_Instances/THM-M-0299/* .stage1-worker-selftest.json; do test -z "$(git diff --no-index --check /dev/null "$f" 2>&1 \|\| true)" \|\| exit 1; done` | 0 | no whitespace diagnostics in tracked or new files |

The structural checker and final artifact hashes are represented in the provisional node receipt.
That receipt is mutable worker evidence, not content-addressed master acceptance.

## Open gates

An approved immutable source snapshot and exact theorem passage, source identity and errata audit,
independent review, operator/kernel/domain/scalar/truncation/hypothesis/exponent/conclusion/constant
and boundary choices, canonical Lean expression and environment fingerprint, checked transports,
statement mutations, exhaustive anchor audit, obligation registry, typed graphs, proof,
composition, provenance/trust closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, and master acceptance remain open. These gates do not invalidate
a truthful self-tested `planned` intake.
