# Intake validation record

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

The intake was validated in the worker automation clone. These are structural intake checks only;
there is no Lean declaration in this phase and therefore no kernel-proof claim.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed: 15 assurance groups, 1546 uniform-L0 targets, execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed with 1546 unique targets and ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Confirmed rank 100, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, and theorem incomplete. |
| `python3 -m json.tool Stage1_Instances/THM-M-0005/intake.json` | 0 | Intake JSON parsed successfully. |
| dossier-local reference check recorded below | 0 | Every path named in `public_merge_targets` exists. |
| `git diff --check -- Stage1_Instances/THM-M-0005 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Known open gates: exact Lean statement and environment fingerprint; primary-source pin and detailed
assumption/errata audit; candidate declaration audit; obligation and graph freeze; proof, trust,
provenance, hermetic replay, readability, and independent acceptance. Root remains `[H1, M4, R3]`.
