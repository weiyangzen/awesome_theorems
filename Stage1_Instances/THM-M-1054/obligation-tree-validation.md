# THM-M-1054 obligation-tree validation

Item: `S56-M-1054-OBLIGATION_TREE`

Date: 2026-07-12

Base revision: `ff4e83f798358bf80798541f0b3f627121e1e617`

## Decision

The registry and typed graph bundle freeze thirteen root-relevant obligations, their independent
machine/source/readability eligibility, risk classes, semantic ledgers, and seven graph kinds. The
Lean composition checks the subsingleton branch, Koopman norm extraction, and exact root assembly
while retaining the nontrivial mean-ergodic result as an explicit premise. Thus the architecture is
self-tested without taking proof credit from the anchor-audit phase.

The root remains `[H1, M3, R3]`. The minimal proof cut is
`M1054-L-ABSTRACT-MEAN-ERGODIC`; proof integration, source and readable review, provenance/trust
closure, release validation, independent verification, and master acceptance remain open.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1054` | 0 | Rank 246, planned hard-mathlib-anchor lane, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1054/build_obligation_artifacts.py` | 0 | Deterministically generated registry denominator `f7c35de0112294744fa63038e000e1a2e550e44a12536e4a50961e4eaaef2aa8`. |
| `python3 Stage1_Instances/THM-M-1054/check_obligation_tree.py` | 0 | 13 unique obligations, 24 typed edges, reciprocal proof composition, root reachability, recipe coverage, and open-root boundary passed. |
| concatenate `Statement.lean` and `ObligationTree.lean` without the latter's import into a temporary owned-path file, then `cd Formalizations/Lean && lake env lean ../../<temporary-file>` | 0 | Conditional exact-root composition elaborated; Lean reported only `propext`, `Classical.choice`, and `Quot.sound`. Temporary source was removed. |
| `python3 -m json.tool` on the four generated JSON artifacts | 0 | Registry, typed graphs, structured validation specifications, and state record parsed. |
| `rg -n 'sorry\|admit\|sorryAx\|axiom \|placeholder' Stage1_Instances/THM-M-1054/ObligationTree.lean` | 1 | No forbidden proof escape or placeholder marker; exit 1 means no match. |
| `git diff --check -- Stage1_Instances/THM-M-1054 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

No command updated, fetched, or otherwise mutated a Lake dependency. The clone's untracked
`Formalizations/Lean/.lake` link was pre-existing worker infrastructure and is not a changed path.

## Status boundary

Only the assigned obligation-tree node is proposed as `[_]` pending master acceptance. This is not
proof-node completion, audit completion, or theorem completion.
