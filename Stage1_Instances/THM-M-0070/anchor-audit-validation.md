# THM-M-0070 Anchor-Audit Validation

Item: `S56-M-0070-ANCHOR_AUDIT`

Base revision: `d266c6f5ce5732e1fccd687e2f9ce9aa2a0ed1fe`

Base tree: `e77c8d6d5b41cb13d9d8acab2753ac37c4ebd6b4`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

The immutable pinned mathlib inventory supplies `IsSolvable`, the derived-series definition,
closure lemmas, and strict commutative, nilpotent, and Z-group special cases. It supplies no
declaration that obtains solvability from finite odd cardinality. The `docs/1000.yaml` entry is a
title without a declaration. The target-owned Lean probe elaborates the exact statement interface,
derived-series transport, and commutative special case; all three checked witnesses report only
`propext`, `Classical.choice`, and `Quot.sound`. It deliberately contains no root inhabitant.

The external Lean project `ianklatzco/odd-order-lean` has a pointwise exact declaration at immutable
commit `0f4a5daeaf6f26efd5af808ecd05e4744d8a2924`, but the body is `by sorry`. Its README and
`.sorry-budget` identify that root as the project's one permitted placeholder, and none of the 34
Coq theorem files is ported. This is `M5`, not `M1` or machine closure. The similarly named Formal
Conjectures declaration is an unrelated open prime divisibility conjecture and also contains
`sorry`.

The official MathComp `Feit_Thompson` source at commit
`6afa795b9018c64ab5c7cd2f9b3c9ab5dd45d93f` has the mathematically exact Coq statement and a named
body. It is classified as an `E3` other-prover source anchor: Coq/Rocq objects cannot be imported by
Lean, and this run had neither Coq tools nor an approved cross-kernel bridge. Therefore the root
remains `H1/M3/R4`. Neither `AUDIT-Z` nor theorem completion is claimed.

## Commands And Results

All local validation ran in this worker clone against the automation-provided canonical `.lake`
symlink read-only. No `lake update`, `lake build`, dependency clone/fetch/install, or `.lake`
mutation ran. Network commands only inspected public metadata and downloaded immutable source
archives into `/tmp`; they were discovery evidence, not dependencies or validation closure.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0070` | 0 | rank 1101; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned dependency worktree clean |
| immutable `git grep` and odd-vocabulary/solvability-vocabulary file-set intersection over pinned mathlib | 1 / 0 | no exact root; 177 odd-vocabulary and 24 solvability-vocabulary files had zero intersection; title-only docs entry classified separately |
| Sourcegraph exact-name and normalized-type searches | 0 | only the unrelated formal-conjectures prime statement for the name query; normalized target query had zero matches; response SHA-256 `1a571f...580` and `66af10...b2c` |
| GitHub REST repository search for quoted aliases and Lean | 0 | HTTP 200; zero results in that bounded query; response SHA-256 `08c082...00b` |
| GitHub metadata plus immutable codeload/raw inspection of `ianklatzco/odd-order-lean@0f4a5dae...2924` | 0 | exact Lean declaration has `by sorry`; tree `95e696...7441`, source archive SHA-256 `15fcc5...c9d`, toolchain 4.32.0-rc1, mathlib `360da6...b56` |
| immutable raw/codeload inspection of `math-comp/odd-order@6afa795b...d93f` | 0 | exact Coq `Feit_Thompson` source found; archive/PFsection14 SHA-256 `c0287e...dd3` / `8153cf...19f`; no Lean credit |
| grep.app query for `Feit_Thompson` | 0 transport, HTTP 429 | Vercel Security Checkpoint; response SHA-256 `8d9505...4c0e` |
| `lake env lean ../../Stage1_Instances/THM-M-0070/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact interface target and eight APIs printed; derived-series and commutative witnesses elaborated; three axiom reports matched; stdout SHA-256 `37c228...818` |
| `python3 -B Stage1_Instances/THM-M-0070/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | pins, blobs, hashes, statement fingerprints, candidates, receipt, packet, and narrow Lean replay agreed offline |
| `python3 -m json.tool` on all target JSON artifacts and root packet | 0 | structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` | 1 (expected no match) | no proof gap, custom axiom, unsafe/opaque body, TODO, FIXME, or placeholder in the target-owned Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0070 .stage1-worker-selftest.json` plus new-file checks | 0 | no whitespace diagnostics |

## Discovery Boundary

The frozen inventory classifies six candidate groups and records exact aliases, surfaces, access
policy, response/archive hashes, and access failures in `anchor-discovery-protocol.json` and
`anchor-audit.json`. Sourcegraph had not indexed the very recent exact Lean placeholder project;
GitHub metadata discovery located it. These results justify the bounded inventory classification,
not an internet-wide absence or saturation claim.

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. The
obligation registry, a placeholder-free proof-phase implementation, full transitive trust/TCB
closure, primary-source and readable reconstruction review, hermetic and independent validation,
deterministic release bundle, `AUDIT-Z`, and theorem completion remain open.
