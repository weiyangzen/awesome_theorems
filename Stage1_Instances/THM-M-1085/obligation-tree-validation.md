# Obligation-tree validation record

Item: `S56-M-1085-OBLIGATION_TREE`  
Base revision: `d96dc535bc8d589c9aef8df34b25d348f6d53f2c`

## Result

Registry v1 freezes 17 obligations and seven separate typed graphs for the covariance-interpolation
proof route. The frozen denominator digest is
`c0367c009b2f628b52c7cf782f7785730d0207f7e90ec30afa47c1523a8a4dc4`; 15 obligations are
machine-required and the source/provenance overlays cannot earn proof credit. Every required node
reaches the exact root in the acyclic proof graph, all reciprocal edge indices validate, and all
semantic ledgers remain below the 100-step split threshold.

`ObligationTree.lean` kernel-checks only the exact child-to-root composition interface. Its
`PointwiseComparison` premise is intentionally uninhabited here. No mathematical proof body,
closed obligation, `M0`, audit completion, or theorem completion is claimed. The root remains `M4`.

## Commands and results

Commands ran in the worker clone. Lean ran from `Formalizations/Lean` against the existing pinned
`.lake`; no update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1085/build_obligation_artifacts.py` | 0 | built 17 obligations; denominator digest above |
| `python3 Stage1_Instances/THM-M-1085/check_obligation_tree.py` | 0 | PASS; 17 obligations, 65 typed edges, root open at M4 |
| `lake env lean -R ../.. -o ../../Stage1_Instances/THM-M-1085/Statement.olean ../../Stage1_Instances/THM-M-1085/Statement.lean` followed by `LEAN_PATH=../.. lake env lean -R ../.. ../../Stage1_Instances/THM-M-1085/ObligationTree.lean`, then removal of temporary oleans | 0 | exact composition declaration elaborated |
| `python3 Stage1_Instances/THM-M-1085/check_statement.py` | 0 | four mutations killed; target digest `2af285ae...d43315` unchanged |
| `python3 -m json.tool` on both generated JSON artifacts | 0 each | valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1085` | 0 | rank 527, L0/rework_required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1085 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

The main remaining root cut set is law reduction, singular covariance interpolation, the Gaussian
derivative identity, the mixed-derivative sign, and the indicator limit. Primary-source pinpointing,
terminal proof provenance, trust closure, hermetic replay, and independent acceptance also remain
downstream. Only the integration lane may accept this provisional phase receipt.
