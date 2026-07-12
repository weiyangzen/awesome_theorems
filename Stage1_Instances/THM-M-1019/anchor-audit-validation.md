# Anchor-audit validation record

Item: `S56-M-1019-ANCHOR_AUDIT`  
Base revision: `e8666885f0826b16099ccf37c244a7d3ee4001b2`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The exact frozen probability-measure target has a terminal theorem in pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`: `MeasureTheory.Measure.ext_of_charFun` in
`Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic`. Its theorem body reduces equality of
characteristic functions to `ext_of_integral_char_eq`. `AnchorAudit.lean` installs the two explicit
probability hypotheses as local instances and Lean accepts the upstream declaration at exactly the
frozen binders and conclusion. Both the upstream theorem and wrapper report only `propext`,
`Classical.choice`, and `Quot.sound`; neither report includes `sorryAx`.

This is an `M0-W` candidate, not an authoritative promotion. The obligation graph, full dependency
and trust closure, proof-phase integration, hermetic validation, source/readability gates, and master
acceptance remain downstream. The root therefore remains unpromoted by this node.

Repo-local and all materialized pinned-package Lean searches found no independent exact proof;
nearby mathlib Gaussian files consume the same extensionality declaration. Anonymous GitHub
repository-metadata searches found no relevant Lean 4 project. grep.app returned HTTP 429 for all
three code queries, which is recorded as an access failure rather than evidence of absence.

## Commands and results

All Lean commands used the existing pinned `.lake` artifacts. No dependency was fetched, updated,
built, cloned, or installed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1019/AnchorAudit.lean` | 0 | exact wrapper elaborated; upstream and wrapper axiom reports contained only the three listed axioms |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1019/Statement.lean` | 0 | exact frozen statement, checked integral transport, and mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-1019/check_anchor_audit.py` | 0 | target fingerprint, manifest pin, installed tree, source identities, candidates, and status boundary agreed |
| scoped `rg` over repository-local and all materialized pinned dependency Lean sources | 0 | exact pinned mathlib candidate located; no independent exact implementation found |
| three GitHub REST repository searches | 0 | two empty results and one unrelated repository; response hashes recorded in structured audit |
| three grep.app API searches | 0 | HTTP 429 responses captured; access failures only |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1019` | 0 | rank 495, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1019/anchor-audit.json` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1019 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This node is self-tested pending master acceptance. It completes only the bounded immutable anchor
audit. `H1` and `R3` remain unchanged; full `AUDIT-Z` and `THEOREM-Z` are false.
