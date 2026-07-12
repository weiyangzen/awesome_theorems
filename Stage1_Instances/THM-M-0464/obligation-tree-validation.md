# Obligation-tree validation receipt

Item: `S56-M-0464-OBLIGATION_TREE`  
Base revision: `345fe5a69ba9559544340ea64c754f3fb53f2fcf`

The registry is frozen against `Statement.lean` SHA-256
`17f12ef1ddf29bd25ef0928243339acd452b7d1534aa7a73efca01686ae81917` and
`anchor-audit.json` SHA-256
`f1ba60e8ff4ee2085e42f27a7bfda831034fabebb7e5b207fd624f4740d31045`.
The deterministic generator and fail-closed checker bind all sixteen obligation identities,
eligibility denominators, complete node schemas, seven typed graph families, reciprocal adjacency,
proof acyclicity/reachability, and the open closure boundary.

## Validation

Commands were run from this worker clone. Lean used existing pinned artifacts selected from
`Formalizations/Lean`; no Lake dependency operation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0464/build_obligation_artifacts.py` | 0 | generated 16 obligations; denominator `91ec52d8f1edc34961cc95a24b77b3d4c396a74330c734aa85d20cbc700ed940` |
| `python3 Stage1_Instances/THM-M-0464/check_obligation_tree.py` | 0 | PASS: 16 obligations, 75 typed edges; root open (`M3`) |
| `{ printf '%s\n' 'import Mathlib'; cat ../../Stage1_Instances/THM-M-0464/Statement.lean ../../Stage1_Instances/THM-M-0464/ObligationTree.lean; } \| lake env lean /dev/stdin` from `Formalizations/Lean` | 0 | exact root and conditional composition elaborated; axiom report: `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and uniform L0/rework baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0464` | 0 | rank 310; planned; theorem incomplete |
| `python3 -m json.tool` on both generated JSON artifacts | 0 | both artifacts parsed as JSON |
| `rg -n '\b(sorry\|admit\|axiom\|sorryAx)\b' Stage1_Instances/THM-M-0464 --glob '*.lean'` | 1 | no prohibited declaration or placeholder token found |
| `git diff --check -- Stage1_Instances/THM-M-0464 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test creation |

## Boundary

The checked Lean theorem only unfolds the root from a hypothesis already supplying the full
counting conclusion. It does not construct that hypothesis. All mathematical packages,
source-node review, terminal provenance, trust closure, proof execution, and release evidence
remain open. This supports the obligation freeze only; master acceptance is still required.
