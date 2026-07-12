# Statement validation

Base revision: `797546bf2bab359f9fc5be515c3d4e8943c9d931`.

This receipt covers statement selection and elaboration only. The canonical target contains no
theorem declaration or proof body. The worker clone reused the canonical pinned `.lake` directory
through its pre-existing symlink and did not mutate or update dependencies.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1141` | exit 0; rank 346, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1141/Statement.lean` | exit 0; exact target and four structural mutations elaborated; `#print` emitted the canonical expression |
| `python3 -m json.tool Stage1_Instances/THM-M-1141/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1141/task-dag.json` | exit 0; valid JSON |
| forbidden-token scan of `Statement.lean` | exit 1; no forbidden token found |
| `git diff --check -- Stage1_Instances/THM-M-1141` | exit 0; no output |

The elaborated target imports only `Mathlib.Analysis.InnerProductSpace.Harmonic.Basic` for
`HarmonicOnNhd` and `Mathlib.Analysis.InnerProductSpace.PiL2` for the concrete Euclidean-space
model. The mutations remove connectedness, remove compactness, weaken positivity to
nonnegativity, and move `C` beneath the function binder; their distinct declarations confirm that
these source-sensitive changes were not silently folded into the root.

Known downstream failures are immutable anchor audit, objective obligation registry, a proof body,
trust/provenance validation, historical-source and independent review, hermetic replay, and release
acceptance. Thus this is M3 statement evidence, not theorem completion.
