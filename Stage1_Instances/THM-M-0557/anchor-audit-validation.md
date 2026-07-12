# Anchor-audit validation record

Item: `S56-M-0557-ANCHOR_AUDIT`  
Base revision: `2534080bb6434bc903d482fcebdf9e0a05b94398`

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the exact formal
route. `HomotopyGroup.group` gives the group structure for a nonempty index type, hence for
`Fin (n + 1)`. `HomotopyGroup.commGroup` gives the commutative structure for a nontrivial index
type, hence for `Fin (n + 2)`. `AnchorAudit.pinnedMathlibCandidate` checks the entire frozen target
by direct instance synthesis.

The terminal source constructs the group by transferring the fundamental-group structure through
`homotopyGroupEquivFundamentalGroup`. Its commutative instance proves independence of two coordinate
directions using `transAt_distrib`, then invokes Eckmann-Hilton. The pinned module has an explicit
Apache-2.0 source header and contains none of the scanned placeholder, bodyless, unsafe, tactic
oracle, or external-code markers. This node does not claim the later transitive trust audit.

No independent external completion was admitted. Bounded Sourcegraph searches returned no indexed
matches, while GitHub repository metadata exposed `jzxia/WhiteheadTheorem`, an adjacent Whitehead
project rather than an apparent group-construction proof. GitHub code/API access was rate-limited
and git transport timed out, so it remains an unverified near miss without an immutable revision.
Those access failures are not reported as evidence of global absence.

The exact root therefore remains `M3` after this phase: the eligible `M0-W` route is located and
kernel-probed, but integration belongs to the later obligation-tree and proof nodes. No H status,
proof acceptance, audit completion for the whole theorem, or theorem completion is claimed.

## Commands and results

All commands ran on 2026-07-12 in this worker clone. Lean reused the existing manifest-pinned
environment. No Lake update/build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0557/AnchorAudit.lean` | 0 | exact target probe and six route declarations elaborated; no `sorryAx` reported |
| `python3 Stage1_Instances/THM-M-0557/check_anchor_audit.py` | 0 | audit identity, manifest pin, installed mathlib HEAD, source digest, root boundary, and Lean probe agreed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib hash-object Mathlib/Topology/Homotopy/HomotopyGroup.lean` | 0 | source blob `02446f9239282c4353dba6bcb50655767d91e3f0` |
| `rg -n '\\bsorry\\b|\\badmit\\b|^\\s*(axiom|unsafe)\\b|native_decide|run_tac' .../HomotopyGroup.lean` | 1 | expected no-match result for the terminal source |
| three Sourcegraph public Lean queries | 0 | each returned `matchCount=0`; response hashes recorded in `anchor-audit.json`; forks/archives excluded |
| GitHub repository/code search and immutable inspection attempts | mixed | adjacent Whitehead repository discovered; code search HTTP 403 and git/archive access timed out, explicitly retained as an access blocker |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0557` | 0 | rank 605, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0557 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open gates

Freeze the obligation registry before using the candidate for proof credit. The proof phase must
then integrate the exact wrapper and the validation phases must close terminal-body provenance,
transitive imports and axioms, composition, hermetic replay, readability, independent verification,
and master acceptance. Until then, `M0-W` and theorem completion are not accepted states.
