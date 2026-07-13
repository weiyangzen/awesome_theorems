# THM-M-0079 Anchor-Audit Validation

Item: `S56-M-0079-ANCHOR_AUDIT`

Base revision: `250f9e73cbbb3ebd2da9d0cefff78f0ab8c0d056`

Base tree: `b6e8138c58e31e82f8209cb70fbc0fb253f3654a`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

Pinned mathlib contains an exact candidate. `subgroupIsFreeOfIsFree` has the same universe,
ambient `Group` and `IsFreeGroup` premises, arbitrary `Subgroup`, and `IsFreeGroup H` conclusion as
the frozen target. The audit-local wrapper elaborates by direct application. Lean prints the
terminal body as `IsFreeGroup.ofMulEquiv (endMulEquivSubgroup H)`, reports only `propext`,
`Classical.choice`, and `Quot.sound`, and reports the terminal, three major substrate declarations,
and wrapper sorry-free.

The proof route realizes `H` as the vertex group of the free action groupoid for `G` acting on
`G/H`, uses a geodesic spanning tree to prove the vertex group free, and transports freeness across
the multiplicative equivalence. This is an exact, kernel-checked `M0-W` candidate route. It is not
accepted proof state: the accepted root remains `[H1, M3, R4]` pending obligation-tree, proof
integration, full transitive provenance/trust, validation, and master gates.

The immutable external inventory records two David Waern historical projects at commits
`99fb30c0...2ea1` and `e51a8c65...7dbe`. Their sources contain relevant Lean 3 theorems, but use
Lean 3.7.1 and 3.27.0 with Lean 3 mathlib, have no license files, and were not replayed. They are
historical `M5` research evidence, not Lean 4 integration candidates. No additional Lean 4 terminal
body was admitted from the bounded manifest and public-index searches. Search saturation is not
claimed.

All local validation used the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake` mutation ran.

## Commands And Results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0079` | 0 | rank 1105; planned; no accepted legacy artifacts; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision `8a178386...ea95`, tree `bdc39a...5c2b`, clean dependency worktree |
| bounded `rg` over repository-local and manifest-pinned Lean sources | 0/1 | only pinned mathlib's candidate module and umbrella import were found; no separate repo-local or non-mathlib candidate |
| mathlib `git log`, `blame`, `merge-base --is-ancestor`, blob and source hash checks | 0 | Lean 4 port `a39a8f5...c9cc3` and path move are ancestors; pinned source blob `08cc647c...b06f` and SHA-256 `e777c40c...c847` matched |
| GitHub REST repository query families | 0 | HTTP 200; two historical Lean 3 repositories found; Lean 4/declaration families returned zero; response hashes recorded |
| five GitHub REST code queries | 0 | HTTP 401 authentication requirement recorded; no negative code result claimed |
| Sourcegraph exact/alias query families, including forks and archives | 0 | only indexed mathlib4 matched the Lean 4 aliases and only indexed mathlib3 matched the historical snake-case alias; both phrase queries returned zero; response hashes recorded |
| five grep.app query families | 0 | HTTP 429 checkpoints recorded; no negative result claimed |
| immutable archive inspection of `dwarn/nielsen-schreier-lean@99fb30c...2ea1` | 0 | archive and four source/manifest hashes recorded; exact relevant Lean 3 theorem found; Lean 3.7.1 and mathlib pin confirmed; no license or obvious proof-hole token |
| `lake env lean ../../Stage1_Instances/THM-M-0079/AnchorAudit.lean` from `Formalizations/Lean` | 0 | six candidate/substrate types, three bodies, five expected axiom sets, five sorry-free reports, and exact target printed; stdout SHA-256 `36905ff3...aa48` |
| `python3 -B Stage1_Instances/THM-M-0079/check_anchor_audit.py` | 0 | identities, fingerprints, immutable pins, body markers, classifications, receipt, packet, and narrow Lean replay agreed |
| `python3 -m json.tool` on anchor JSON artifacts and root packet | 0 | all JSON parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` and the pinned candidate source | 1 (expected no match) | no sorry, admit, sorryAx, bodyless axiom, unsafe/opaque declaration, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0079 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status Boundary

This phase supplies provisional, self-tested anchor evidence pending master acceptance. It does not
freeze the obligation registry, install accepted proof-phase composition, accept full transitive
trust/TCB closure, close human-source or readable-reconstruction debt, complete `AUDIT-Z`, or
complete the theorem.
