# THM-M-0402 validation-phase evidence

Item: `S56-M-0402-VALIDATION`. Base revision:
`4dabab14860067cbb1220d76c5a1bd9abd87d624`. Validation timestamp:
`2026-07-11T19:56:32Z`.

The run reused the canonical pinned `.lake` symlink without updating, building, cloning, fetching,
or otherwise mutating dependencies. `Validation.lean` reconstructs the proof phase's normalization
facts without importing or invoking `Proof.lean`. `check_validation.py` binds frozen source and pin
hashes, checks all ten registry identities and the authoritative open `M3` boundary, scans local Lean
sources, validates the obligation graph, and elaborates the statement, proof, and independent probe
through temporary local artifacts.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0402` | 0 | rank 15, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0402/validate_obligation_tree.py` | 0 | 10 obligations and 19 typed edges passed; root open M3 |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0402/check_proof.sh)` | 0 | statement and partial proof bodies elaborated; printed axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0402/check_validation.py` | 0 | frozen inputs, pins, graph boundary, hygiene, Lean replay, and independent probe passed; root remains open M3 |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |

This validates partial normalization work, not Evertse's theorem. The conditional composition accepts
the entire missing finiteness result as a premise. The frozen authority still records no closed
obligations and no composition certificate. S-unit finite generation, the nondegenerate unit-equation
core, the group adapter, the projective quotient/class bijection, specialization, terminal composition,
and root trust/provenance remain open. Release-only empty-cache replay, a distinct signed runner,
independent H0/R0 review, SBOM/licenses, and a deterministic bundle are absent. Consequently
`audit_complete=false`, `theorem_complete=false`, and the root vector remains `[H1, M3, R4]`.
