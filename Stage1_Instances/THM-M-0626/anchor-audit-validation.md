# Anchor-audit validation

Item: `S56-M-0626-ANCHOR_AUDIT`  
Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4`  
Base tree: `61214aa2a03c032134ddc4958b1df63df3430a85`  
Validation date: 2026-07-13 (`Asia/Shanghai`)

## Result

The frozen target is the global-continuity set-image theorem
`Stage1Instances.THM_M_0626.ConnectedImageTarget`. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the sharper theorem
`IsConnected.image`: `ContinuousOn f s` is enough to preserve `IsConnected` under the direct image.
`AnchorAudit.lean` checks a literal copy of the frozen target by applying that theorem to
`Continuous.continuousOn`. This preserves both universe-polymorphic spaces, the arbitrary subset,
the nonempty connectedness convention, the direct-image encoding, and the conclusion.

The pinned terminal body pairs image nonemptiness with `IsPreconnected.image`. The latter pulls
back relative-open sets through the continuous-on map and applies source preconnectedness. Lean
reports both declarations and the exact adapter sorry-free; all three axiom reports are exactly
`propext`, `Classical.choice`, and `Quot.sound`. The source module, manifest, toolchain, license,
source slice, package revision, package tree, and clean worktree are hash-bound in the ledger.
This is a provisional `M0-W` candidate route, not accepted proof credit; the accepted root remains
`M3`.

The external audit found a commit-pinned Lean 4 wrapper in
`google-deepmind/formal-conjectures@fdbea4653453a764aa7f952d3b45c93007356cc9`, but its entire body
calls the same `IsConnected.image` route. It is a duplicate consumer, not an independent terminal
proof. Searches over repo-local Lean, all 668 Lean files in materialized non-mathlib packages, and
bounded public indexes found no other independent body. Sourcegraph returned seven uses in four
indexed repositories; anonymous GitHub code search returned HTTP 401 and grep.app returned HTTP
429. Those are explicit limitations, so the audit claims complete classification only for the
frozen six-group inventory, not exhaustive discovery.

## Commands and results

All Lean commands used the existing pinned `.lake` artifacts read-only. No update, build, clone,
fetch, dependency installation, or dependency mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0626` | 0 | rank 1320, planned, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib revision `8a178386...ea95`, tree `bdc39a31...e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package clean |
| `cd Formalizations/Lean && LC_ALL=C LANG=C NO_COLOR=1 lake env lean ../../Stage1_Instances/THM-M-0626/AnchorAudit.lean` | 0 | exact adapter, terminal/substantive bodies, three standard axiom reports, three sorry-free reports, and explicit target elaborated; stdout SHA-256 `47b5e4d3...99932` |
| scoped `rg` over repo-local and all materialized dependency Lean sources | 0 | mathlib supplied the only declaration/terminal body; all 668 non-mathlib Lean files had no semantic match |
| manifest/installed revision and status loop over all 11 packages | 0 | every installed HEAD matched the manifest and every package worktree was clean |
| mathlib source ancestry, blob, source-slice, license, and placeholder scans | 0 | port/body commits are ancestors of the pin; hashes agree; no forbidden declaration in the inspected module |
| three GitHub repository searches | 0 | each returned `total_count=0`, `incomplete_results=false`; response SHA-256 `4af480...72a5f` |
| GitHub code search for `IsConnected.image language:Lean` | HTTP 401 | authentication failure; response SHA-256 `b7dbd1...e29e`; no negative result claimed |
| Sourcegraph `context:global lang:Lean IsConnected.image` | 0 | seven matches in four repositories; only mathlib declared the theorem; response SHA-256 `adb734...27b0` |
| grep.app query for `IsConnected.image` | HTTP 429 | security checkpoint; response SHA-256 `07a40f...e0d8`; no negative result claimed |
| immutable `formal-conjectures` commit/file/toolchain/manifest/license inspection | 0 | exact wrapper source fixed at commit `fdbea465...6cc9`; source SHA-256 `fec059...be41`; it terminates at mathlib |
| `python3 -B Stage1_Instances/THM-M-0626/check_anchor_audit.py` | 0 | assignment, target fingerprint, six candidates, all pins/hashes, exact M0-W candidate, accepted M3 root, receipt, packet, and false completion flags agreed |
| `python3 -m json.tool` on the discovery ledger, audit ledger, receipt, instance, and worker packet | 0 | all finalized structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-0626 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This node is self-tested pending predecessor and master acceptance. The accepted vector remains
`[H1, M3, R4]`: historical source identity and H0 review, obligation architecture, proof-phase
integration, full transitive provenance/trust/TCB closure, readable R0, hermetic replay,
independent verification, deterministic release evidence, `AUDIT-Z`, and theorem completion all
remain open.
