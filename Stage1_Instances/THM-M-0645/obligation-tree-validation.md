# Obligation-tree validation

Item: `S56-M-0645-OBLIGATION_TREE`  
Base revision: `e563272fab7f96449273f34f500e415657ffbc72`

Registry version 1 freezes fifteen obligations and denominator SHA-256
`ade5c7f404980300aed3c54b9ac7289122562478f2866babd794986ddf37fc01`. The typed bundle contains
43 edges across seven separately typed graphs. Proof requirements are reciprocal, acyclic, and
root-reachable; every node budget is at most 100.

## Commands and results

Commands ran on 2026-07-12 in the worker clone. The automation-provided `.lake` link reused the
canonical pinned artifacts and was not modified. No update, build, clone, fetch, or network access
was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and uniform rework baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | rank 691, planned lifecycle, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0645/build_obligation_artifacts.py` | 0 | deterministically wrote 15 obligations, 43 typed edges, and the frozen denominator |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | hashes, denominator, node schemas, graph typing, reciprocity, acyclicity, reachability, recipes, and open-root boundary passed |
| `cd Formalizations/Lean; tmp=$(mktemp -d -p . stage1-m0645-XXXXXX); cp ../../Stage1_Instances/THM-M-0645/{Statement,ObligationTree}.lean "$tmp"/; LEAN_PATH="$(lake env printenv LEAN_PATH):$(realpath "$tmp")" lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean"; LEAN_PATH="$(lake env printenv LEAN_PATH):$(realpath "$tmp")" lake env lean "$tmp/ObligationTree.lean"; rm -rf "$tmp"` | 0 | exact statement and conditional assembly elaborated; reported axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 -m json.tool` on registry, graphs, and validation specs | 0 | all JSON artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-0645` | 0 | no whitespace errors |

An initial combined command was run from the wrong directory: repository-relative Python commands
exited 2, while the direct statement check exited 0 and the obligation import exited 1 because no
temporary `Statement.olean` existed. The isolated two-step Lean command above is the corrected,
successful evidence recipe; the failed attempt grants no evidence.

## Status boundary

This self-test validates the registry freeze, typed graphs, and conditional final composition only.
It supplies no inhabitant of `CompletenessDerivationBuilder`, no Henkin construction, no term-model
truth lemma, and no transport of the external Foundation proof. The root remains `[H2, M4, R4]`;
audit and theorem completion are false pending proof work, node-specific assurance receipts, and
master acceptance.
