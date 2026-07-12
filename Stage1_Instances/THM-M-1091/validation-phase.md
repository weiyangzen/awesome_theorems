# THM-M-1091 validation-phase evidence

Item: `S56-M-1091-VALIDATION`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `9562952daaa9a03ced35f2b4f4a336345b0ea802`

## Verdict

`self_tested_pending_master_acceptance`. The fail-closed validator replayed the exact frozen
statement, obligation composition module, proof root, integral transport, and an independently
assembled exact root in fresh temporary output space. All checked roots report exactly `propext`,
`Classical.choice`, and `Quot.sound`. Frozen local inputs, the clean pinned mathlib revision, and
the terminal source hash agree. No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe`
mechanism was found in the checked local modules or terminal source.

This is deliberately nonrelease evidence. The pinned dependency artifacts are a shared warm cache,
the typed graph still records its pre-proof open state pending master reconciliation, and the
independent proof ran in this same worker rather than on a distinct signed runner. Thus hermetic,
freshness, and independent-runner gates remain fail-closed; theorem completion is false.

## Commands and results

All Lean commands were launched by the structured Python validator with network unused and the
existing pinned `.lake` artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1091` | 0 | rank 533; planned; hard mathlib anchor/wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1091/check_validation.py` | 0 | exact statement/composition/proof/integral/independent roots replayed; allowed axiom profile and pinned provenance passed; release blockers reported |
| `python3 -m json.tool Stage1_Instances/THM-M-1091/validation-phase-spec.json` | 0 | validation specification parses |
| `python3 -m json.tool Stage1_Instances/THM-M-1091/validation-receipt.json` | 0 | provisional node receipt parses |
| `git diff --check -- Stage1_Instances/THM-M-1091 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The validation implementation itself is self-tested and ready for master inspection. It does not
accept a receipt or alter authoritative workflow state. The first failed node gate is graph
freshness pending master reconciliation; the first failed release gate is the section 10.6 cold
empty-cache hermetic build. Primary-source `H0`, readable `R0`, a distinct runner, release, and
master acceptance also remain open.
