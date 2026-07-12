# THM-M-1188 obligation-tree validation

Item: `S56-M-1188-OBLIGATION_TREE`  
Base revision: `a2044374af8048c248b7f7eecf9440b4d4e00485`  
Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 17 obligations and 40 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Fifteen obligations
are machine-required; the human-source and release-provenance overlays cannot earn proof credit.
The frozen denominator SHA-256 is
`2c191411ea8f03dd1a2dcd2e206e72315fb39f01c51f6e6c146efbbe93b55ffd`.

The Lean harness restates the exact canonical binder structure and checks that an explicitly typed
`AnalyticMaximumEngine` composes into the root. It does not provide that engine. No obligation is
credited closed; the root remains `M3`, and the eight-node analytic cut set is compactness,
attainment, strict perturbation, spatial and temporal derivative signs, interior exclusion,
boundary identification, and epsilon removal.

## Commands and results

Commands ran from the repository root unless a working directory is stated. Existing pinned
`.lake` artifacts were reused; no update, build, clone, fetch, or dependency mutation occurred.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1188/build_obligation_artifacts.py` | 0 | deterministically wrote 17 obligations and 40 typed edges; denominator `2c1914...55ffd` |
| `python3 Stage1_Instances/THM-M-1188/check_obligation_tree.py` | 0 | input hashes, denominator projections, node schemas, seven graph classes, reciprocal composition edges, proof acyclicity, recipes, budgets, prohibited Lean tokens, open-root boundary, and a combined Lean `Iff.rfl` check between the canonical statement and architecture root passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1188/ObligationTree.lean` | 0 | conditional `root_compose` elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1188/Statement.lean` | 0 | canonical target, checked transport, four mutations, and initial-face theorem re-elaborated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1188` | 0 | rank 383; planned; theorem incomplete |
| `python3 -m json.tool` on all three generated JSON artifacts | 0 each | valid JSON |
| `sha256sum` on `ObligationTree.lean`, registry, and graphs | 0 | `ae2044...b959`, `2edda8...a608`, and `02fc0a...dda6` |
| `git diff --check -- Stage1_Instances/THM-M-1188 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This self-test supports only the version-1 registry, typed graphs, validation recipes, readable
architecture, and conditional composition harness, pending master acceptance. It does not support
analytic proof closure, primary-source acceptance, `R0`, transitive trust closure, independent
replay, `AUDIT-Z`, `THEOREM-Z`, or release.
