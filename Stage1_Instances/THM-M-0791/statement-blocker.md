# Exact-statement gate: blocked

Item: `S56-M-0791-STATEMENT`  
Theorem: `THM-M-0791`  
Base revision: `1c5adf59c0f8176526cb4c9fb281b3ff340c9eeb`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `伍丁基数的性质` ("properties of Woodin cardinals"). It supplies no
proposition, ordered binders, hypotheses, conclusion, primary-source edition, theorem or definition
number, page, or errata disposition. Stage0 explicitly leaves the exact definition, assumptions,
proof route, dependencies, and evidence type open.

Several materially different roots fit that wording: a function/closure-point and elementary-
embedding definition, a subset/strongness definition, an equivalence between characterizations, an
existence statement, or a reflection, determinacy, or consistency-strength consequence. They do
not have the same quantifiers or conclusion. They also require choices of ambient set theory and
representations for cardinals, rank segments, subsets or functions, elementary embeddings,
critical points, strongness, and extenders. Selecting one from the topic label would invent or
substitute mathematics, contrary to the rev-5.6 exact-statement gate.

Consequently there is no canonical expression to elaborate or hash and no sound removed-hypothesis,
changed-domain, binder-scope, or boundary mutation test. Introducing a fresh predicate named
`IsWoodin`, assuming it, or replacing Woodin cardinals by mathlib's regular or inaccessible
cardinals would be a fake or weakened target. No such declaration was added. Machine state remains
`M4`; statement acceptance, audit completion, and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.SetTheory.Cardinal.Regular` and
`Mathlib.SetTheory.ZFC.Cardinal`. It checks `Cardinal`, `Ordinal`, `Cardinal.IsRegular`,
`Cardinal.IsInaccessible`, `ZFSet`, and `ZFSet.card`. The probe re-elaborates in the pinned
environment, but these declarations are nearby encoding ingredients only and receive no Woodin
statement or proof credit. A bounded case-insensitive search found no `woodin` occurrence in pinned
mathlib.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` link and artifacts were
used read-only. No update, build, clone, fetch, or dependency mutation was run. The worktree's
untracked `Formalizations/Lean/.lake` entry predated this statement work and was not modified.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0791` | 0 | rank 796, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'woodin\|woodin cardinal\|伍丁基数\|THM-M-0791' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json Stage1_Instances/THM-M-0791` | 0 | only underspecified source metadata and the fail-closed intake artifacts identify a target; no exact proposition was found |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0791/IntakeProbe.lean` | 0 | six nearby cardinal/ZFC APIs elaborated; no canonical theorem target asserted |
| `rg -n -i 'woodin' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match exit in the bounded pinned-mathlib search |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0791 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom occurs in the target's Lean source |

## Retry condition and status boundary

An accountable reviewer must preserve and inspect an immutable primary-source edition, select and
transcribe one exact proposition with all incorporated definitions and assumptions, dispose of
errata, and independently approve the mapping. It must freeze the characterization, ambient
theory, embedding or extender conventions, every binder and hypothesis, conclusion, and boundary
case. A later statement run can then encode that same claim, minimize its pinned imports, serialize
and hash the elaborated expression, check alternate transports, and execute all required mutation
classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is
emitted. The root remains `[H3, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`.
