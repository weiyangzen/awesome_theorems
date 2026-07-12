# Obligation-tree validation record

Item: `S56-M-1036-OBLIGATION_TREE`  
Base revision: `ff4e83f798358bf80798541f0b3f627121e1e617`

## Verdict

Registry version 1 freezes 18 obligations and seven separate typed graphs.
The proof graph has reciprocal `proof_requires`/`composes` edges and reaches
every proof-relevant analytic node. The machine denominator includes the Ito
integration boundary, Picard construction and estimates, limit passage,
uniqueness estimate, Gronwall bridge, indistinguishability upgrade, both
terminal packages, and exact-root composition. Source and provenance overlays
cannot receive machine credit.

Lean elaborated the exact conditional composition. Its axiom report is
`[propext, Classical.choice, Quot.sound]`; no new axiom or proof placeholder is
declared. This does not close the root: the integral-semantics bridge, strong
existence package, and pathwise-uniqueness package have no proof bodies.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1036/build_obligation_artifacts.py` | 0 | generated registry/graphs/specs; denominator SHA-256 `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69` |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | `PASS`: 18 obligations, 47 typed edges, open M3 root |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | rank 229, planned, L0/rework-required, theorem incomplete |
| `lake env lean -R ../.. -o ../../Stage1_Instances/THM-M-1036/Statement.olean ../../Stage1_Instances/THM-M-1036/Statement.lean && LEAN_PATH=../.. lake env lean -R ../.. ../../Stage1_Instances/THM-M-1036/ObligationTree.lean` from `Formalizations/Lean` | 0 | exact statement and composition elaborated; composition axioms are `propext`, `Classical.choice`, `Quot.sound`; temporary owned `.olean` removed afterward |
| `python3 -m json.tool` on all three generated JSON files | 0 | valid JSON |
| `rg -n 'sorry\|admit\|axiom \|sorryAx' Stage1_Instances/THM-M-1036/ObligationTree.lean` | 1 | no forbidden declaration token (1 is ripgrep's no-match result) |
| `git diff --check -- Stage1_Instances/THM-M-1036 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

No network or dependency operation was used. The existing pinned `.lake`
closure was read only; no Lake update, build, clone, or fetch was run.

## Boundary

This self-tests only the obligation-tree phase pending master acceptance. Root
status remains `[H2, M3, R3]`; theorem completion is false. In particular, the
two `standard_*` fields in the frozen statement are opaque propositions and do
not themselves expose integral laws. The proof phase must supply a real checked
construction/transport or version the statement rather than assume those laws.
