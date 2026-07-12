# Anchor-audit validation record

Item: `S56-M-1015-ANCHOR_AUDIT`  
Base revision: `2232074b8c07f74c200df9e5aabf6f2831fc83c3`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the pair-valued
Slutsky theorem, its continuous-function form, and an addition specialization. `AnchorAudit.lean`
checks exact wrappers for the frozen pair and sum branches and specializes the continuous-function
theorem to multiplication. Each wrapper's axiom report is limited to `propext`,
`Classical.choice`, and `Quot.sound`; none contains `sorryAx`.

These declarations do not close the frozen four-branch root. The quotient branch assumes only
`c != 0`, while the available continuous-function theorem requires a globally continuous map.
Real division on `Real x Real` is discontinuous at points with zero second coordinate, so applying
that theorem directly would be invalid even though the limiting denominator is nonzero. The
legacy `S1_M_294` wrapper reaches exactly the same boundary and explicitly omits quotient.

A bounded search of repository-local and all materialized pinned dependency Lean sources found no
additional exact candidate. Anonymous grep.app, GitHub code-search, and general-web lanes were
rate-limited or timed out; those are recorded as access failures, not evidence of global absence.
No dependency was fetched or installed. The root therefore remains `M3`, with the localized
quotient bridge as the first machine integration blocker.

## Commands and results

All Lean commands used the existing pinned `.lake` artifacts. No update, build, clone, fetch, or
installation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1015/AnchorAudit.lean` | 0 | three partial wrappers and four pinned declarations elaborated; all wrapper axiom reports contained no `sorryAx` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1015/Statement.lean` | 0 | exact frozen four-branch target re-elaborated |
| `python3 Stage1_Instances/THM-M-1015/check_anchor_audit.py` | 0 | target fingerprint, manifest pin, installed HEAD, module hash, candidates, and status boundary agreed |
| scoped `rg` over repository-local and all materialized pinned dependency Lean sources | 0 | only the pinned mathlib family and legacy partial wrappers matched; no exact four-branch terminal declaration was located |
| grep.app API search | 22 | HTTP 429; access failure only |
| GitHub public code-search attempts | 28 | timed out without usable results; access failure only |
| general public web-search attempts | 28 | timed out without usable results; access failure only |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1015` | 0 | rank 294, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1015/anchor-audit.json >/dev/null` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1015 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This assigned node is self-tested pending master acceptance. It is a bounded machine-anchor audit,
not an exhaustive external search or theorem proof. `H1`, `M3`, and `R3` remain truthful; source
acceptance, obligation architecture, quotient proof, full validation, and theorem completion remain
downstream.
