# Validation record

The intake checks below were run from base
`478034dee4145f887a572a3c645a3a2ea81bc883` on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0108` | 0 | rank 32, planned, L0, rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0108/intake.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0108` | 0 | no whitespace errors |

These are the smallest real checks for the intake phase: repository standard
conformance, exact manifest membership, structured dossier parsing, and patch
hygiene. No historical Lean artifact is accepted by these results.

## Statement self-test

Statement work is based on revision
`2dc5a410b68eff806858fd6ed0cb33d57f6209f7`. The final exact command results
are mirrored in `statement-receipt.json` and `.stage1-worker-selftest.json`.

| Command | Expected result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0108/Statement.lean` | exit 0; the target and four mutations elaborate and print fully explicit forms |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0108/check_statement.py` | exit 0; exactly one `stage1-validator-semantic-result/1.0` object with `phase_accepted: true` |
| JSON parsing, prohibited-construct scan, and scoped whitespace checks | pass |

The validator binds the exact source, statement record, crosswalk, empty
dependency ledger, provisional receipt inputs, pinned toolchain and mathlib,
canonical expression fingerprint, four mutation fingerprints, and the unique
contract-selected artifact and validator candidates. It also removes each of
the four direct imports independently and requires elaboration failure.

This is statement-phase evidence only. The intake predecessor remains
worker-provisional, and the validator did not exist at this worker's base.
Consequently the scheduler's unchanged-base validator replay requires a fresh
worker after integration. No proof, source `H0`, audit completion, theorem
completion, release, or master acceptance is claimed.
