# Statement-gate blocker

Item: `S56-M-0784-STATEMENT`  
Base revision: `444819795285695894ff7b29af5c2419e0e000fa`

## Decision

The Lean 4 statement gate is **blocked**, not self-tested as complete. No canonical declaration or
expression can truthfully be added from the repository source record. The only source wording is
`PFA及其推论` ("PFA and its consequences"). It does not select a unique proposition: it could mean
the Proper Forcing Axiom itself, a relative-consistency result, one consequence under a PFA
hypothesis, or an unspecified collection of consequences.

This is a hard blocker under sections 5 and 5.1 of the rev-5.6 blueprint. Choosing a familiar PFA
formulation would still require unsupported decisions about the ambient set theory, internal
coding of proper partial orders, forcing-order orientation, dense-family cardinality convention,
and filter versus directed-set encoding. Choosing any particular consequence would substitute a
broader source label with a new theorem. Consequently there is no exact target to elaborate, no
normalized expression to hash, and no sound mutation suite to run.

No `theorem`, `axiom`, `sorry`, placeholder, assumed-PFA projection, or broadened/substituted target
was introduced. `IntakeProbe.lean` remains only an elaboration check for generic encoding APIs and
does not claim to state PFA.

## Evidence

Commands were run from the repository root unless the command contains an explicit subshell.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets validated |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0784` | exit 0; rank 789, planned, theorem_complete false |
| `rg -n -C 3 '适当力迫公理\|PFA及其推论\|PFA and its consequences\|Proper Forcing Axiom' Docs` | exit 0; only inventory/Stage0 metadata and generated Stage1 projections found; the substantive source wording is only `PFA及其推论` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0784/IntakeProbe.lean)` | exit 0; seven generic API checks elaborate with the pinned Lean environment |

The preflight worktree contained only the expected untracked `Formalizations/Lean/.lake` symlink to
the canonical pinned artifacts. It was used read-only; no dependency update, fetch, clone, or build
was run.

## Retry condition

Provide and independently inspect an immutable primary source passage that selects one exact
proposition and fixes all assumptions and boundary conventions. Then encode that proposition with
minimal pinned imports, record its elaborated expression and environment fingerprint, and run the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

Until then the root remains `[H3, M4, R4]`, the statement node remains open, and no audit or theorem
completion is claimed.
