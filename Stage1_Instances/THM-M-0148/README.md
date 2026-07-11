# THM-M-0148 Intake Dossier

`THM-M-0148` is a rev-5.6 `planned` instance for the repository entry named
"Mori minimal model program". The repository's source wording is only
"birational classification of higher-dimensional algebraic varieties". It is
not precise enough to identify one theorem, so this intake deliberately does
not manufacture a formal target or claim any proof state.

## Intake Boundary

- Manifest rank: 28; legacy slot: `S1-M-028`.
- Lane: `known_partial_branch_deepening`; baseline: `L0 / rework_required`.
- Formal system: Lean 4 + mathlib only.
- Lifecycle: `planned`; accepted execution state: none.
- Root vector: `H5 / M4 / R3`.
- Theorem complete: false; audit complete: false.

The historical module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_028.lean`
is discovery input only. Its predicates for terminal singularities,
Q-factoriality, minimal models, and Mori fibre spaces are parameters or
`Prop`-valued fields. Its compiled wrappers therefore establish object and
statement-shape boundaries, not the MMP.

## Open Task DAG

| Task | Depends on | Required output | State |
|---|---|---|---|
| `S56-M-0148-STATEMENT` | intake acceptance | Select a named theorem branch and elaborate its exact Lean target | open |
| `S56-M-0148-ANCHOR_AUDIT` | statement | Audit mathlib and external Lean candidates at immutable revisions | blocked by statement |
| `S56-M-0148-OBLIGATION_TREE` | anchor audit | Freeze semantic obligations and typed graphs | blocked by anchor audit |
| `S56-M-0148-PROOF` | obligation tree | Implement or integrate genuine proof bodies | blocked by obligation tree |
| `S56-M-0148-VALIDATION` | proof | Run kernel, trust, provenance, and replay gates | blocked by proof |
| `S56-M-0148-RELEASE` | validation | Independently decide audit and theorem completion | blocked by validation |

The first retry condition is a primary-source-backed selection of a precise,
bounded MMP theorem, including base field and characteristic, dimension,
singularity/pair assumptions, and exact output.

## Validation Record

Run from repository root at base revision
`a8d6489fd935cd71fa4499f2f3f5b051998203f4`:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0148` | exit 0; rank 28, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0148/instance.json` | required self-test; exit recorded in worker manifest |
| `git diff --check -- Stage1_Instances/THM-M-0148` | required self-test; exit recorded in worker manifest |

No Lean theorem validation is claimed at intake because no exact formal target
has been frozen.
