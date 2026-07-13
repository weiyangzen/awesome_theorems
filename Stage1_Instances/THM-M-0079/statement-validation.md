# Statement validation

Item: `S56-M-0079-STATEMENT`
Base revision: `d266c6f5ce5732e1fccd687e2f9ce9aa2a0ed1fe`

## Frozen target

`Stage1Instances.THM_M_0079.NielsenSchreierTarget` quantifies over an arbitrary
universe-polymorphic `G` with `[Group G]` and `[IsFreeGroup G]`, and over every
`H : Subgroup G`; its conclusion is `IsFreeGroup H` using the inherited subgroup structure. No
finite-generation, finite-index, normality, nontriviality, rank, or cardinality premise is added.

The literal `Subgroup (FreeGroup X)` formulation and the definition-level existence of some
same-universe `FreeGroupBasis` for `H` are both kernel-checked equivalent to the canonical target.
These transports use only statement vocabulary and transport along `IsFreeGroup.mulEquiv`; they do
not invoke a Nielsen-Schreier proof.

## Direct import

The sole declared direct import is the defining module
`Mathlib.GroupTheory.FreeGroup.IsFreeGroup`. It provides all statement vocabulary and the literal
free-group instance; deleting it makes this module fail. The proof-bearing
`Mathlib.GroupTheory.FreeGroup.NielsenSchreier` module is absent, and the statement run checks that
`subgroupIsFreeOfIsFree` is unavailable.

## Commands and results

All commands ran in this worker clone. Lean used the automation-provided pinned `.lake` symlink
read-only; no update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0079` | 0 | rank 1105; planned; no legacy slot; theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0079/Statement.lean)` | 0 | exact target, four transports, four expected mutation rejections, three boundary specializations, anchor exclusion, axiom reports, and explicit expression elaborated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0079/check_statement.py)` | 0 | expression `bb109f77...a553`; source `fdacf7f7...78c5`; output `87cb8af0...221d`; sole import deletion failed; mutations, transports, boundaries, authority, metadata, packet, pins, and dependency cleanliness agreed |
| `python3 -B Stage1_Instances/THM-M-0079/check_intake.py` | 1 | expected historical failure: the checker pins the pre-statement base, intake authority state, and nine-file inventory; it is not cited as current evidence |
| `python3 -m json.tool <path>` separately for owned JSON and `.stage1-worker-selftest.json` | 0 | all finalized structured artifacts parsed |
| `rg -n '<prohibited declaration pattern>' Stage1_Instances/THM-M-0079 --glob '*.lean'` | 1 | expected no match; no forbidden declaration or placeholder in target-owned Lean source |
| `git diff --check -- Stage1_Instances/THM-M-0079 .stage1-worker-selftest.json` | 0 | no whitespace errors; the scoped checker also validates final newlines and trailing whitespace |

## Result boundary

This self-tested worker handoff proposes `[_]` pending master acceptance. It freezes only the exact
statement and environment. It supplies no accepted primary-source review, proof-bearing anchor
audit, obligation registry, proof body, composition evidence, readable reconstruction, hermetic
replay, independent validation, accepted state, audit completion, or theorem completion.
