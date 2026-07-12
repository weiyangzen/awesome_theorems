# Obligation-tree validation record

Item: `S56-M-1082-OBLIGATION_TREE`  
Validation date: `2026-07-12`  
Base revision: `e545899c85e870efdef04615348353d8d5552315`

## Frozen architecture

Registry version 1 contains ten unique semantic obligations. Eight are machine-required.
`M1082-X-SOURCE` and `M1082-X-PROVENANCE` are governance overlays and cannot earn proof credit.
The denominator digest is
`76ae9dcefe964214432144f89ffd780d44d893493424b3ec549ef286ee615089`.
The registry is independently bound to the exact `Statement.lean` and `anchor-audit.json` byte
hashes.

Seven separate typed graphs contain 29 edges. The proof graph stores reciprocal
`proof_requires`/`composes` pairs and is acyclic from the root through exact forward and reverse
directions to the pinned one-field definition boundary. Refinement, provenance, evidence, trust,
documentation, and workflow relations cannot silently become proof premises. Every node owns a
four-step substantive ledger and an executable validation recipe.

`ObligationTree.lean` checks the exact constructor, projection, and child-to-parent `iff`
composition interfaces. The axiom printer reports only `propext`, `Classical.choice`, and
`Quot.sound`, matching the bounded anchor audit. This is provisional interface evidence, not a
master-accepted proof-phase or theorem-completion receipt.

## Commands and results

All successful Lean commands reused the existing pinned Lake closure. No dependency update, build,
clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1082/build_obligation_artifacts.py` | 0 | built 10 obligations; emitted denominator digest above |
| `python3 Stage1_Instances/THM-M-1082/check_obligation_tree.py` | 0 | PASS; 10 obligations, 29 typed edges, open M3 root |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1082/ObligationTree.lean` | 0 | constructor, projection, and exact `iff` composition elaborated; only the three audited axioms were printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1082/Statement.lean` | 0 | frozen canonical target re-elaborated with no output |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets and ranks 1 through 1,546 valid |
| `python3 scripts/stage1_target.py show THM-M-1082` | 0 | rank 524, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1082 .stage1-worker-selftest.json` | 0 | no whitespace errors |

One initial combined invocation ran the two root-relative Python paths after changing directory to
`Formalizations/Lean`; it exited 2 because those relative paths do not exist from that directory.
The table records the corrected commands run from their stated directories. This was a command
working-directory error, not a missing artifact or validation failure.

## Open root boundary

The architecture phase is self-tested pending master acceptance. `closed_obligations` deliberately
remains empty: proof-phase acceptance, primary human-source closure, transitive trust/provenance,
hermetic replay, independent review, and release are outside this item. The root remains `M3`, with
`H2` and `R4` debt. No `H0`, `M0`, `R0`, `AUDIT-Z`, root closure, or theorem completion is claimed.
