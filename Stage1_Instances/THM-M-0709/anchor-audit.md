# Anchor audit

Item: `S56-M-0709-ANCHOR_AUDIT`  
Base revision: `136ebf643dcdcbc42cef34e415177189578060ef`

## Result

No exact or partial Post correspondence problem declaration was found in the complete pinned
mathlib tree, the repository's other pinned Lean 4 packages, or tracked repo-local sources. The
only useful pinned surface is generic computability infrastructure in
`Mathlib.Computability.Halting`: `ComputablePred`, its Boolean characterization, the map to
`REPred`, Rice's theorem, and `ComputablePred.halting_problem`. These declarations do not mention
PCP, construct PCP tiles, or prove a reduction to `HasSolution`; they receive no root proof credit.

The authoritative machine-readable inventory is `anchor-audit.json`. Mathlib is fixed at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; its `Halting.lean` content hash is
`c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de`. The manifest fixes every
other package revision and has SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## External Lean 4 discovery

Bounded GitHub repository searches for the exact title and common PCP/Lean 4 query variants
returned no repositories. GitHub code search was unavailable without authentication. Five
Lean-filtered grep.app queries returned HTTP 503, and bounded DuckDuckGo/Sourcegraph exact-phrase
queries yielded no candidate. These failures are recorded rather than converted into a claim that
no external formalization can exist. In particular, there is no immutable external revision,
module, declaration, proof body, toolchain, or license to integrate from this pass.

This completes the requested candidate audit, not the theorem. The current debt is
`formalization_debt`, not `repo_local_integration_debt`: no external Lean 4 closure was identified.
The root remains `[H1, M4, R3]`. A future proof needs a checked reduction (for example from the
pinned halting theorem) whose construction lands in the exact binary, structured `PCPInstance`
statement. Modified PCP or an unpinned external anchor cannot substitute for that obligation.

## Validation

Commands ran without updating, fetching, cloning, or building dependencies. The `.lake` package
tree was pre-existing worker infrastructure, so this is node-scoped nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pinned commit `8a178386...a95` |
| `rg -n -i --glob '*.lean' --glob '*.md' 'post.?s? correspondence\|post correspondence\|\\bPCP\\b\|modified PCP' . Formalizations/Lean/.lake/packages` | 0 | only this dossier and the unrelated probabilistically checkable proofs acronym; no Lean PCP anchor |
| `rg -n 'def ComputablePred\|theorem.*ComputablePred\|ComputablePred.*iff\|Computable.*reduce\|ComputablePred.*decid' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability` | 0 | generic APIs and halting theorem inventoried |
| `lake env lean ../../Stage1_Instances/THM-M-0709/AnchorAuditProbe.lean` (cwd `Formalizations/Lean`) | 0 | all recorded mathlib declaration names and types checked |
| `lake env lean ../../Stage1_Instances/THM-M-0709/Statement.lean` (cwd `Formalizations/Lean`) | 0 | exact PCP target independently re-elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0709/anchor-audit.json` | 0 | structured receipt parses |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `git diff --check -- Stage1_Instances/THM-M-0709 .stage1-worker-selftest.json` | 0 | no whitespace errors |

External discovery details and service failures are preserved in `anchor-audit.json`. They are
discovery evidence only and are not a completeness theorem about the public internet.
