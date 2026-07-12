# S56-M-0652-VALIDATION worker evidence

Item: `S56-M-0652-VALIDATION`  
Base revision: `2cc51d958aa855ad8f827ea8097a66a0ba94c616`  
Validation time: `2026-07-12T10:23:02+08:00`

## Result

The fail-closed validator copied the four Lean modules into a fresh temporary module directory,
re-elaborated the frozen statement, conditional composition, and proof-phase boundary bodies, and
then elaborated two separately written boundary proofs from `Validation.lean`. The independent
probe imports only `Statement`; it neither imports nor invokes `Proof` or `ObligationTree`.
All reported declarations were free of `sorryAx`; their observed axiom output was `Quot.sound`.
The validator also bound the source and pin hashes, required a clean pinned mathlib checkout, ran
the 15-node/36-edge obligation validator, and confirmed that the graph still reports an open `M3`
root.

This is a truthful partial validation result, not validation of the general Craig interpolation
theorem. There is no unconditional `Statement` proof body. The remaining root cut set is
`M0652-B-COMPLETENESS`, `M0652-T-SYNTACTIC`, and `M0652-B-SOUNDNESS`; consequently root provenance
and trust cannot close. The first failed node gate is the unfinished proof dependency. The warm
shared-cache run is also not the release cold-hermetic protocol, and the same-workspace independent
probe is not a distinct signed runner.

## Commands and exact results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0652` | 0 | rank 298, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0652/check_obligation_tree.py` | 0 | 15 obligations and 36 typed edges passed; root open M3 |
| `python3 Stage1_Instances/THM-M-0652/check_validation.py` | 0 | hashes, pins, clean mathlib, placeholder scan, temporary-directory Lean replay, trust output, independent boundary reconstruction, and open-root check passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0652/validation-spec.json` | 0 | structured recipe parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0652/validation-receipt.json` | 0 | structured provisional receipt parsed |
| `git diff --check -- Stage1_Instances/THM-M-0652 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` write was performed. Exact hashes,
environment identity, declarations, result boundaries, invalidation inputs, and retry conditions are
recorded in `validation-receipt.json`.
