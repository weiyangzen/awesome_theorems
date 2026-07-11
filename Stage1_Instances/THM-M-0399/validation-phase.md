# THM-M-0399 validation-phase record

Item `S56-M-0399-VALIDATION`, based on commit
`680081e6eeda70901a966224430acff134050176` and tree
`ff131b19fc9c8794fe8a0189dc35117892f40d52`.

The local kernel replays pass for the exact statement and for
`rothStatement_of_strongFinite`. The axiom probe reports exactly `propext`,
`Classical.choice`, and `Quot.sound` for that composition declaration. Source hygiene finds no
`sorry`, `admit`, `axiom`, `unsafe`, or `sorryAx` in either owned Lean file. Provenance remains
explicit: the checked theorem is a local composition body whose premise is
`StrongFiniteStatement`; it is not a terminal proof body for Roth's theorem.

The validation verdict is **blocked** at exact-root kernel closure. `M0399-STRONG-FINITE` is still
the minimal root cut set, so `RothStatement` has no proof body and remains `M4`. In consequence,
release-grade hermetic, full-TCB, and independent gates cannot validate theorem completion. They
were not simulated: this worker uses the canonical pre-existing `.lake` symlink, hence a warm
shared cache, and no second independently provisioned runner or attestor was available.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0399` | exit 0; rank 12, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0399/check_statement.py` | exit 0; exact expression hash `d63a586...2389`; four mutations killed |
| `python3 Stage1_Instances/THM-M-0399/check_anchor_audit.py` | exit 0; immutable pins and six non-closing candidates verified |
| `python3 Stage1_Instances/THM-M-0399/check_obligation_tree.py` | exit 0; 11 obligations, 11 nodes, seven typed graph families |
| `python3 Stage1_Instances/THM-M-0399/check_proof_phase.py` | exit 0; one composition body closed; exact root open |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0399/RothStatement.lean` | exit 0; printed the exact canonical proposition |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0399/RothComposition.lean` | exit 0; checked `StrongFiniteStatement -> RothStatement` |
| Lean stdin probe with `#print axioms Stage1Instances.THM_M_0399.rothStatement_of_strongFinite` | exit 0; `[propext, Classical.choice, Quot.sound]` |
| `rg -n --glob '*.lean' '\\b(sorry\|admit\|axiom\|unsafe)\\b\|sorryAx' Stage1_Instances/THM-M-0399` | exit 1 as expected; no match |

No `lake update`, build, fetch, clone, or `.lake` mutation was performed. Exact inputs, toolchain,
gate outcomes, retry condition, and the nonrelease boundary are machine-readable in
`validation-phase.json`.
