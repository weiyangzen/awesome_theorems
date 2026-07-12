# Obligation-tree validation record

Item: `S56-M-0508-OBLIGATION_TREE`  
Base revision: `e9252b1cfdc99a094324c8a10d260769df2eca15`

## Result

Version 1 freezes 17 stable obligations and denominator SHA-256
`79ff122b736335e90938cf7304db0b680dc23531e4d12d4b8c987d0ddc953bc2` before any
analytic closure is observed. Seven independently indexed typed graphs cover proof composition,
refinement, provenance, evidence, trust, documentation, and workflow. All semantic ledgers are at
most 24 steps. The checked Lean harness defines a finite ordered prime-triple count, proves that
its positivity is equivalent to the representation predicate, and conditionally composes eventual
positivity into the exact eventual target.

The axiom report for both checked bridge declarations is exactly
`[propext, Classical.choice, Quot.sound]`; it contains no `sorryAx`. This receives local bridge
credit only. The root stays M4 because the Fourier identity, arc partition, major-arc estimate,
singular-series positivity, and minor-arc bound are open. Source H0, R0, transitive trust,
independent replay, release, audit completion, and theorem completion are not claimed.

## Commands and results

Commands ran on 2026-07-12 using the existing pinned `.lake` artifacts. No update, build, clone,
fetch, or other `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0508/build_obligation_artifacts.py` | 0 | Deterministically emitted 17 obligations and seven graph indexes |
| `python3 Stage1_Instances/THM-M-0508/check_obligation_tree.py` | 0 | Hash binding, denominators, schemas, reachability, reciprocal edges, acyclicity, budgets, forbidden tokens, and open-root boundary passed; 86 typed edges |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0508/ObligationTree.lean)` | 0 | Finite-count equivalence and conditional root composition elaborated; axiom reports had no `sorryAx`; only linter warnings occurred |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0508/Statement.lean)` | 0 | Canonical target and eventual transport re-elaborated |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and uniform 1546-target baseline passed |
| `python3 scripts/stage1_target.py check` | 0 | Ordered manifest and 1546 unique targets passed |
| `python3 scripts/stage1_target.py show THM-M-0508` | 0 | Rank 882, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0508/obligation-registry.json` | 0 | Valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0508/typed-graphs.json` | 0 | Valid JSON |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0508 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean escape in owned sources |
| `git diff --check -- Stage1_Instances/THM-M-0508 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This self-test supports only the registry and typed architecture pending master acceptance. The
first open analytic cut set is `M0508-N-FOURIER`, `M0508-B-ARCS`, `M0508-L-MAJOR`,
`M0508-L-SINGULAR`, and `M0508-L-MINOR`; root debt remains `[H1, M4, R3]`.
