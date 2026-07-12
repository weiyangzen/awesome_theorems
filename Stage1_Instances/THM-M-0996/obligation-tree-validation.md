# THM-M-0996 obligation-tree validation

Item: `S56-M-0996-OBLIGATION_TREE`  
Base revision: `eb5f7c9057a60dace86040954ad22ca44a040954`  
Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 19 obligations and 53 edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs.
Sixteen obligations are root-relevant machine obligations; three are assurance
overlays with no proof credit. The denominator projection digest is
`8d3affee638ef1cc6e3fbb2ee9d52fc76212b0a91327f7b42ecba1b4ae8b6e9e`.

## Commands and results

All commands ran at repository root unless explicitly prefixed.

| Command | Exact result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0996` | exit 0; rank 276, planned lifecycle, theorem_complete false |
| `python3 Stage1_Instances/THM-M-0996/build_obligation_artifacts.py` | exit 0; wrote 19 obligations and 53 typed edges; digest as above |
| `python3 Stage1_Instances/THM-M-0996/check_obligation_tree.py` | exit 0; schemas, frozen hashes and denominators, all seven graph classes, reciprocal proof edges, acyclicity, node ledgers, open-root boundary, and cut-set reachability passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0996/obligation-registry.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0996/typed-graphs.json` | exit 0; valid JSON |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0996/Statement.lean` | exit 0; exact selected target and transport elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0996/ObligationTree.lean` | exit 0; conditional composition elaborated; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound` |
| `! rg -n '\b(sorry\|admit\|axiom)\b\|sorryAx' Stage1_Instances/THM-M-0996/ObligationTree.lean Stage1_Instances/THM-M-0996/{obligation-registry.json,typed-graphs.json}` | exit 0; no placeholder or declared-axiom token found |
| `git diff --check -- Stage1_Instances/THM-M-0996` | exit 0; no output |

The existing pinned `.lake` closure was reused. No update, build, clone, fetch,
or other dependency mutation was performed. The pre-existing untracked `.lake`
link makes this nonrelease evidence.

## Status boundary

This receipt self-tests only the frozen obligation registry, typed graphs, and
conditional composition harness. The harness explicitly assumes both central
profile inequalities. `M0996-L-HALFSPACE` and `M0996-L-GENERAL` are the
remaining root cut set; no obligation is marked closed. Primary-source fidelity,
exact proof bodies, readable reconstruction acceptance, transitive trust and
provenance, hermetic replay, independent validation, `AUDIT-Z`, `THEOREM-Z`,
and master acceptance remain open.
