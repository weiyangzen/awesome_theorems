# Obligation-tree validation record

Item: `S56-M-0087-OBLIGATION_TREE`  
Base revision: `b614452f9bb46017d5423ccca0a5c196ba91be22`

## Result

Registry version 1 freezes 17 unique obligations, their eligibility sets, and
the denominator projection. Seven separate typed graphs contain reciprocal
proof/composition edges plus refinement, provenance, evidence, trust,
documentation, and workflow edges. The checker confirms graph references,
acyclic root reachability, per-node semantic ledgers and budgets, structured
validation recipes, source fingerprints, and the fail-closed closure boundary.

`ObligationTree.root_of_packages` kernel-checks exact conjunction assembly from
four explicit premises. Lean reports `propext`, `Classical.choice`, and
`Quot.sound`, inherited through the categorical types in those premises. This
does not accept the imported mathlib candidate bodies and does not close the
root.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Lean used the existing pinned
`.lake` artifacts; no update, build, clone, or fetch occurred.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0087/build_obligation_artifacts.py` | 0 | Deterministically generated registry, graph bundle, and 17 structured recipes |
| `python3 Stage1_Instances/THM-M-0087/check_obligation_tree.py` | 0 | 17 obligations and typed edges validated; denominator and source fingerprints agree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0087/ObligationTree.lean` | 0 | Exact conditional composition elaborated; axiom closure is `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0087/Statement.lean` | 0 | Frozen target re-elaborated in the pinned environment |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard consistent; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0087` | 0 | Rank 133; planned; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0087/obligation-registry.json >/dev/null` | 0 | Registry is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0087/typed-graphs.json >/dev/null` | 0 | Typed graph bundle is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0087/validation-specs.json >/dev/null` | 0 | Recipes are valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0087 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Open gate

The proof phase must resolve the four-package root cut set and bind unique
terminal bodies without alias credit. Human-source, trust, readability,
hermetic release, freshness, and independent-verification gates remain open.
The theorem is not complete.
