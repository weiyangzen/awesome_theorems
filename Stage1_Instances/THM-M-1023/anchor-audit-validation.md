# Anchor-audit validation record

Item: `S56-M-1023-ANCHOR_AUDIT`  
Base revision: `205d13cfc35c45883410c569709a91cb34edce16`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The audit is bound to the elaborated frozen target and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Pinned mathlib provides characteristic functions,
their convolution product law, uniqueness of finite measures from characteristic functions, the
Dirac formula, and the probability norm bound. `AnchorAudit.lean` checks these named declarations
and two typed uses. The dependency closure has no infinite-divisibility or Levy-Khinchin terminal
declaration, so these are substrate rather than root closure.

The bounded external search found one Lean 4 file:
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`,
`Atlas/TheoryOfProbability/code/InfinitelyDivisible.lean`. At that immutable revision it uses Lean
4.29.0 and the same mathlib pin. Its 41-line source defines `Measure.convPow` and
`IsInfinitelyDivisible`; it states and proves no Levy-Khinchin theorem. Its definition also omits a
separate probability assumption on the target measure that the frozen target includes. It is
therefore a definition-only anchor, not an `M0` candidate. It was not vendored or fetched into
`.lake`; the source was inspected through an immutable raw URL. Its noncommercial license with a
repository no-training rider is recorded as an additional integration constraint.

Sourcegraph's completed response returned one match in one repository with no skipped repositories.
GitHub repository search separately returned HTTP 403 after its unauthenticated quota was exhausted,
so that failure is recorded rather than treated as negative evidence. Public discovery is bounded
and cannot establish global nonexistence.

## Commands and results

All validation used the existing pinned Lake artifacts. No Lake update/build, dependency clone,
fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1023` | 0 | rank 499, planned, historical artifacts unaccepted, theorem incomplete |
| local `rg` search over repository and all pinned dependency Lean sources | expected no-match for dependencies | no terminal candidate; only metadata, this target's files, and unrelated characteristic-function uses locally |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a1783...a95`; tree `bdc39a...f2b` |
| Sourcegraph query for Levy-Khinchin and infinite-divisibility identifiers | 0 | one definition-only Atlas hit; completed with one repository, one match, and no skipped repositories; response SHA-256 `5880c9...809a` |
| immutable Atlas raw source/toolchain/manifest/license inspection | 0 | source `06331f...a711`; Lean 4.29.0; mathlib pin matches; restrictive license recorded |
| GitHub repository search | 403 | unauthenticated quota exhausted; no search result credited |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1023/AnchorAudit.lean` | 0 | six named mathlib probes and two typed examples elaborated |
| `python3 Stage1_Instances/THM-M-1023/check_anchor_audit.py` | 0 | pin/tree/hashes matched; statement and probes elaborated; zero terminal candidates |
| `python3 -m json.tool Stage1_Instances/THM-M-1023/anchor-audit.json` | 0 | receipt parsed as valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1023 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This node is self-tested pending master acceptance. Root debt remains `[H1, M3, R4]`. No primary
mathematical source pinpoint, terminal proof, representation existence/uniqueness bridge, audit
completion, or theorem completion is claimed.
