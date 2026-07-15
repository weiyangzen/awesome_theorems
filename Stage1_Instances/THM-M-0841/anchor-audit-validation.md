# THM-M-0841 anchor-audit validation

Item: `S56-M-0841-ANCHOR_AUDIT`

Base revision: `b4319ef6d039de12cec559f173287d541c238d70`

Base tree: `0b0762ebd01405d33218c3bcbcb24d4544b0fad0`

Validation date: 2026-07-15 (`Asia/Shanghai`)

## Result

No exact Lean 4 proof candidate was found for the frozen page-1087 statement. Pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the complete-equipartite encoding and
general Turan-density containment infrastructure, but no named Erdos-Stone declaration and no
theorem computing the density needed to close this target. `AnchorAudit.lean` checks these support
interfaces at the pin, machine-checks five of them as recursively sorry-free, and records their
standard `propext`, `Classical.choice`, and `Quot.sound` footprint. It intentionally defines no
inhabitant of the canonical target.

A later mathlib commit and the theorem author's external project contain genuine formal
Erdos-Stone variants. Both prove dense, fixed-part containment statements. The canonical target is
the sparse complementary-graph form with an existential part size growing at least as the square
root of an iterated logarithm. Converting the located variants requires a nontrivial checked
complement/density-slack and growing-part diagonal transport; none was located. The variants are
therefore immutable research anchors, not exact target bodies or repo-local closure.

The external project was inspected at commit
`fd0134209519a72b59462f796e957981bb322e7c`, tree
`4cc782dc121d40030432320fd23542698ab39b40`, using a 46,260-byte immutable archive with SHA-256
`f8aa6d33638b139b96c553b063395cd3ba3ef02061863ea77fa4b818aad811a5`. It uses Lean
`v4.16.0-rc2`, mathlib `15f16b1ec50f425147926be1aede7b4baa725380`, and Apache-2.0. Source
inspection found no prohibited proof marker, but the incompatible external dependency closure was
not installed or built. No source-only observation is promoted to kernel evidence.

## Commands and exact outcomes

Commands ran from the repository root unless the table gives a different working directory.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0841` | 0 | rank 1398, planned lifecycle, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the scheduler-provided untracked `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | repository base revision and tree matched this record |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `git ... status --short` | 0 | exact mathlib revision/tree matched and the dependency worktree was clean |
| case-insensitive `rg` over repo-local Lean for Erdos/Erdos-Stone aliases | 0 | 11 target-owned statement hits, no proof body; normalized output SHA-256 `60a1f806b8e6c7e3bb43f93419c83efa5d872cd38f8b86ea1c5d44a817d97f8c` |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -n -i ... HEAD -- '*.lean'` | 1 (expected no match) | no Erdos-Stone alias at the pin; empty-output SHA-256 `e3b0c442...b855` |
| bounded `rg` over all other installed pinned-package Lean files | 1 (expected no match) | no candidate; empty-output SHA-256 `e3b0c442...b855` |
| `(cd Formalizations/Lean && LC_ALL=C LANG=C NO_COLOR=1 lake env lean ../../Stage1_Instances/THM-M-0841/AnchorAudit.lean)` | 0 | ten pinned interfaces elaborated; the two post-pin names failed exactly under `#check_failure`; five silent `assert_no_sorry` commands passed, and five `#print axioms` commands reported the three standard axioms; stdout SHA-256 `3f12cf995da28ccc798c2360ae52704a639b75ca0548ef25b5eef79757d4fee2` |
| `git ... show b9df47...:Mathlib/.../ErdosStoneSimonovits.lean` plus immutable object metadata | 0 | post-pin minimum-degree theorem inspected without checkout; commit tree `e1dfb46...`, blob `ef28446...`, source SHA-256 `455735f5...1148` |
| immutable GitHub commit/archive and external source inspection recorded in `anchor-audit.json` | 0 | external tree, archive, file, pins, license, candidate type, and mismatch boundary recorded |
| bounded GitHub repository, Sourcegraph, GitHub code/API, and grep.app queries | transport outcomes recorded | one authored project and post-pin mathlib found; authentication/rate/index failures retained; no saturation claim |
| `python3 -B Stage1_Instances/THM-M-0841/check_anchor_audit.py` | 0 | planned replay: authority, target fingerprint, pins, immutable candidates, probe output, and H1/M3/R4 boundary passed |
| `python3 -B Stage1_Instances/THM-M-0841/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | planned packet-bound replay passed |
| `python3 -m json.tool` over the protocol, audit, receipt, and worker packet | 0 | all JSON parsed |
| `git diff --check -- Stage1_Instances/THM-M-0841 .stage1-worker-selftest.json` plus no-index checks for new files | 0 aggregate | no whitespace diagnostics |

No `lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake` mutation was performed.

## Known failures

- The statement prerequisite and this anchor-audit receipt still need dependency-ordered master
  acceptance.
- No exact terminal proof body or checked transport from either formal dense fixed-part theorem to
  the sparse complement target with growing iterated-log part size is available.
- Public search is bounded. Anonymous code/API and grep.app access failures prevent an exhaustive
  saturation claim.
- The obligation registry, typed graphs, proof bodies, composition, release-grade transitive
  provenance/trust/TCB closure, hermetic replay, and independent verification remain downstream.
- Human-source H0, readable R0, `AUDIT-Z`, and theorem completion remain open.

This self-tests only the assigned immutable anchor inventory and pinned support probe. The root
remains `[H1, M3, R4]`; neither audit completion nor theorem completion is claimed.
