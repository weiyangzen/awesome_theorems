# Validation-phase evidence

Item `S56-M-0771-VALIDATION` was tested from base revision
`32404187d6cee70b44ae90adf8d0d765752e5149`. The executable structured recipe is in
`validation-spec.json`, and its content-bound result is in `validation-receipt.json`.

The narrow check copies the exact statement, frozen composition, proof, and separately written
validation probe to a temporary module directory. It elaborates them with the pinned Lean 4.29.0
toolchain and clean pinned mathlib revision, checks the exact root twice, observes exactly
`propext`, `Classical.choice`, and `Quot.sound`, and verifies that the conditional composition is
axiom-free. It also scans local sources and the terminal mathlib source for placeholders, added
axioms, and unsafe declarations.

| Command | Result |
|---|---|
| `python3 Stage1_Instances/THM-M-0771/check_validation.py` | exit 0; exact proof root and separate exact root kernel-replayed; pin, provenance, trust observation, and hygiene checks passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0771/validation-spec.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0771/validation-receipt.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0771` | exit 0; rank 780, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-0771 .stage1-worker-selftest.json` | exit 0; no whitespace errors |

This is deliberately nonrelease evidence. The proof dependency awaits master acceptance; the
immutable pre-proof graph remains M3; the run reused a warm shared `.lake`; and there is no cold
offline restoration, complete TCB/SBOM archive, independently provisioned runner, second identity,
or independent minimal verifier. Human-source H0 and readable R0 also remain open. Therefore the
hermetic and independent gates fail closed and theorem completion is false.
