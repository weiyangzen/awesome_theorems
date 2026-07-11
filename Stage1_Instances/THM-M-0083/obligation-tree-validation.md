# THM-M-0083 obligation-tree validation

Item: `S56-M-0083-OBLIGATION_TREE`  
Date: 2026-07-12 (Asia/Shanghai)  
Base revision: `168aae8f6c98f025672f9f8fcfedb2a74785e4b9`

## Result

The registry freezes 11 unique semantic obligations and the denominator digest
`7b39d289b02d6b5e59b40043779eee5c5556875db249c4b7e440e43a0c859e96`.
Seven separately typed graphs contain 30 edges. Proof requirements have
reciprocal composition edges, the root reaches both directed branches and both
central mathlib bridges, and provenance, trust, documentation, and workflow
edges carry no proof credit.

The Lean harness checks both directions and their exact composition. The final
candidate depends on `propext`, `Classical.choice`, and `Quot.sound`, matching
the anchor audit. It has no `sorryAx`. This is candidate `M0-W` evidence only;
master acceptance and later source, readability, provenance/trust, replay,
independent-verification, and release gates remain open.

## Commands

All commands ran from the repository root unless a `cwd` is shown. Existing
pinned Lake artifacts were reused; no dependency update, fetch, clone, or build
was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0083/build_obligation_artifacts.py` | 0 | generated the registry, graph bundle, and specs; printed the denominator digest above |
| `python3 Stage1_Instances/THM-M-0083/check_obligation_tree.py` | 0 | `PASS`: 11 obligations and 30 typed edges; root candidate checked and release boundary open |
| `python3 -m json.tool` on each generated JSON artifact | 0 | all three structured artifacts parse as JSON |
| `lake env lean ../../Stage1_Instances/THM-M-0083/ObligationTree.lean` (`cwd=Formalizations/Lean`) | 1 | retained expected first attempt: local `Statement` module was not on Lean's module path; no proof evidence claimed |
| pinned `lake env which lean` plus `lake env printenv LEAN_PATH`; compile `Statement.lean` to a temporary local `Statement.olean`, then elaborate `ObligationTree.lean` with `LEAN_PATH=.:$LEAN_PATH` (`cwd=Stage1_Instances/THM-M-0083`) | 0 | exact root and both directions elaborated; final axiom report was `[propext, Classical.choice, Quot.sound]`; temporary `.olean` removed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0083` | 0 | rank 139, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n '\b(sorry\|axiom\|admit)\b' Stage1_Instances/THM-M-0083/ObligationTree.lean` | 1 (expected) | no prohibited declaration or placeholder in the Lean harness |
| `git diff --check -- Stage1_Instances/THM-M-0083 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

This self-test supports only the obligation-tree node, pending master
acceptance. The frozen registry and typed graphs do not assert audit or theorem
completion. Human-source H0, accepted R0 reconstruction, full provenance and
trust closure, hermetic replay, independent verification, and deterministic
release receipts are later phases.
