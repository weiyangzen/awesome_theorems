# THM-M-1054 anchor-audit validation

Item: `S56-M-1054-ANCHOR_AUDIT`

Date: 2026-07-12

Base revision: `fa403ca1dcee36895541a38891b372faf4113aab`

## Decision

At immutable mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection` is the
terminal candidate for the frozen real `L2` Koopman target. The new audit
wrapper repeats the exact target shape, obtains contractivity from
`Lp.compMeasurePreservingₗᵢ`, and explicitly handles a subsingleton `L2` space
before applying the mathlib theorem. Lean elaborates the wrapper and reports
only `propext`, `Classical.choice`, and `Quot.sound` for both it and the upstream
theorem.

The tracked legacy `S1_M_246` module also elaborates and contains a more general
Koopman wrapper, but uniform L0 rework makes it discovery input only. It is an
alias of the same terminal mathlib body, not an independent proof.

The external `cameronfreer/exchangeability` candidate was inspected through
three raw files at immutable revision
`e9c9ed5341dd8de7aac6e5575dcf3802830e0125`; their exact SHA-256 hashes are in
`anchor-audit.json`. Its general real `L2` convergence theorem also uses
mathlib's mean-ergodic theorem, while its path-space shift specialization adds
a conditional-expectation bridge. It is anchor-only because it pins Lean
`v4.27.0-rc1` and mathlib
`32d24245c7a12ded17325299fd41d412022cd3fe`, and is not in this repository's
Lake closure. No clone, fetch, update, or dependency mutation was performed.

This self-tests candidate feasibility only. The anchor node cannot grant proof
credit: obligation freezing, proof integration, transitive provenance/trust
closure, release validation, and master acceptance remain open. `H1` and `R3`
also remain unchanged.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1054` | 0 | rank 246, planned hard-mathlib-anchor lane, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned dependency checkout clean |
| `rg -ni 'mean.?ergodic|tendsto_birkhoffAverage_orthogonalProjection|von.?neumann' Formalizations/Lean/AwesomeTheorems Stage1_Instances Formalizations/Lean/.lake/packages -g '*.lean' -g '*.md'` | 0 | exact mathlib theorem, legacy aliases, and no distinct terminal body in the materialized pinned closure |
| `git -C Formalizations/Lean/.lake/packages/mathlib blame -L 89,104 -- Mathlib/Analysis/InnerProductSpace/MeanErgodic.lean` | 0 | declaration body traced to immutable commits `0948c002be15` and `c6bd63551cca` within the pinned tree |
| `lake env lean ../../Stage1_Instances/THM-M-1054/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact target-shaped wrapper elaborated; upstream and wrapper axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `lake env lean AwesomeTheorems/Stage1/S1_M_246.lean` from `Formalizations/Lean` | 0 | tracked historical wrapper elaborated from source |
| `curl -fsSL` for the three external raw-file URLs at revision `e9c9ed...` followed by `sha256sum` | 0 | immutable files matched the three recorded source hashes |
| concatenated `curl -fsSL` responses for those three files piped to `rg -n 'sorry\\b|admit\\b|axiom\\b|unsafe\\b'` | 1 | no forbidden marker found (`rg` exit 1 means no match) |
| `python3 -m json.tool Stage1_Instances/THM-M-1054/anchor-audit.json >/dev/null` | 0 | structured candidate ledger parsed |
| `rg -n 'sorry\|admit\|sorryAx\|axiom\|placeholder' Stage1_Instances/THM-M-1054/AnchorAudit.lean` | 1 | no forbidden Lean declaration or proof escape (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1054 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The assigned immutable anchor inventory is self-tested pending master
acceptance. The exact candidate is ready for the dependent obligation-tree and
proof phases, but this receipt does not claim those phases, overall audit
completion, or theorem completion.
