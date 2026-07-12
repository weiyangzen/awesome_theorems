# THM-M-0118 validation-phase result

Item: `S56-M-0118-VALIDATION`. Base revision:
`797546bf2bab359f9fc5be515c3d4e8943c9d931`.

Validation fails closed at the positive-root precondition. A validation module
that does not import the proof-phase module constructs a different model: all
three geometric propositions are true, dimension is zero, and every indicated
cohomology type is `ZMod 2`. The frozen target would make `ZMod 2` a subsingleton.
Lean checks the resulting contradiction and reports `propext` and `Quot.sound`;
the quotient axiom enters through `ZMod`.

This confirms the earlier `Int` countermodel without sharing its declaration or
model. It is local independent implementation evidence, not the distinct clean
runner or verifier identity required by the release gate. Cold/offline release
and second-runner gates were not run because there is no positive root proof to
validate. Repeating them could not turn the false frozen proposition into the
intended analytic theorem.

Validation ran in this worker clone on 2026-07-12 against the existing pinned
Lake closure. No update, fetch, clone, dependency build, or `.lake` mutation was
performed.

```text
python3 Stage1_Instances/THM-M-0118/check_validation.py
  exit 0
  'Stage1Instances.THMM0118.Validation.independent_root_countermodel' depends on axioms: [propext, Quot.sound]
  PASS THM-M-0118 validation: independent ZMod 2 model confirms the frozen root is false
  VALIDATION BLOCKED: no positive root exists for hermetic or release verification

python3 -m json.tool Stage1_Instances/THM-M-0118/validation-receipt.json
  exit 0

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546

test -z "$(rg -n '[[:blank:]]+$' Stage1_Instances/THM-M-0118/Validation.lean Stage1_Instances/THM-M-0118/check_validation.py Stage1_Instances/THM-M-0118/validation-phase.md Stage1_Instances/THM-M-0118/validation-receipt.json .stage1-worker-selftest.json)"
  exit 0; no trailing whitespace
```

Verdict: `blocked`. Root vector: `[H5, M5, R3]`; audit incomplete; theorem
incomplete. The first failed gate is positive exact-root eligibility. Repair
requires a native connected analytic encoding and a complete refreeze from the
statement phase onward.
