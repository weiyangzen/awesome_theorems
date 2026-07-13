# THM-M-0072 Anchor-Audit Validation

Item: `S56-M-0072-ANCHOR_AUDIT`

Base revision: `56cce0660d633175f8e66c4a538e5c7dce64652e`

Base tree: `94920deccabd41cd711821885fe08d62eed67a4e`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

No exact Lean 4 proof candidate was located. Pinned mathlib transfer and focal-subgroup declarations
are relevant `M3` substrate, and Burnside's normal-complement theorem is an `M5` statement mismatch,
not a substitute. The target-owned probe checks thirteen interfaces, rejects the two strongest
non-substitutes at the exact target type, reports the expected foundation axioms for five inspected
proof-bearing declarations, and reports all five sorry-free. The root remains `[H1, M3, R4]`.

All local validation used the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake` mutation ran.

## Commands And Results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0072` | 0 | rank 1102; planned; no accepted legacy artifacts; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision `8a178386...ea95`, tree `bdc39a...5c2b`, clean worktree |
| bounded `rg` over repository-local and all manifest-pinned Lean sources | 1 (expected no match) | no exact/named Thompson candidate, 2-/p-perfect predicate, or target-shaped declaration outside the target |
| pinned-ancestry `git log -G` queries | 0 | no spelling-matched Thompson or target-shaped declaration in the pinned revision's ancestry |
| eleven Sourcegraph query families with archives/forks included | 0 | ten completed with zero matches; `transferFocal` returned only mathlib; response hashes are in `anchor-audit.json` |
| five GitHub REST repository queries | 0 | HTTP 200, `total_count=0`, `incomplete_results=false` |
| five GitHub REST code queries | 0 | HTTP 401 authentication requirement recorded; no negative code result claimed |
| five grep.app queries | 0 | HTTP 429 checkpoint responses recorded; no negative result claimed |
| GitHub recursive-tree API for `google-deepmind/formal-conjectures@b2e608fc...` | 0 | nontruncated 1204-entry immutable path inventory; only unrelated Feit-Thompson and perfect-number paths |
| `lake env lean ../../Stage1_Instances/THM-M-0072/AnchorAudit.lean` from `Formalizations/Lean` | 0 | thirteen candidate types, two expected type mismatches, five expected axiom sets, five sorry-free reports, and exact target printed; stdout SHA-256 `8b19682c...d86` |
| `python3 -B Stage1_Instances/THM-M-0072/check_anchor_audit.py` | 0 | identities, pins, hashes, source markers, classifications, receipt, worker packet, and narrow Lean replay agreed |
| `python3 -m json.tool` on anchor JSON artifacts and worker packet | 0 | all JSON parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` | 1 (expected no match) | no sorry, admit, sorryAx, custom axiom, unsafe/opaque declaration, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0072 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. It does not
freeze the obligation tree, establish an exact proof route, accept full transitive trust closure,
close human-source or readable-reconstruction debt, complete `AUDIT-Z`, or complete the theorem.

