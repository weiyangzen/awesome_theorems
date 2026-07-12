# Anchor-audit validation record

Item: `S56-M-0982-ANCHOR_AUDIT`  
Base revision: `2676c4fcc9a91f3717e0ef31bd11faa45e5576fe`  
Audit date: 2026-07-12 (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains both terminal
continuity bodies in `Mathlib.MeasureTheory.Measure.MeasureSpace`. The below theorem is stronger
than the frozen branch because it needs no measurability premise. The above theorem accepts
null-measurable events and a finite member; `MeasurableSet.nullMeasurableSet` and probability
measure finiteness provide those inputs. `AnchorAudit.lean` composes these declarations into an
exact local copy of the frozen conjunction and re-elaborates it with the pinned kernel.

The legacy local wrapper is not itself an exact normalized match, although it reaches the same
terminal mathlib bodies. The external search found only mathlib and downstream uses. The one
close external exposition inspected immutably, `optpku/ReasBook@7aee054...`, specializes the laws
to Lebesgue measure and also delegates to the same mathlib declarations. It adds no independent
root body. Public search results are bounded, dated discovery evidence, not a global absence claim.

The audit therefore records the exact wrapper candidate as `M1`: it is locally kernel-checked and
ready for later proof-module integration, but this phase does not preempt the obligation-tree,
proof, validation, or release gates and does not claim theorem completion.

## Commands and exact outcomes

All commands ran in this worker clone. No Lake update, build, clone, fetch, or `.lake` mutation was
performed.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard passed for all 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-0982` | 0 | rank 262, planned, legacy unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0982/Statement.lean` | 0 | frozen target and statement probes re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0982/AnchorAudit.lean` | 0 | both anchors and the exact candidate wrapper elaborated; axiom reports recorded in command output |
| `python3 Stage1_Instances/THM-M-0982/check_anchor_audit.py` | 0 | pin, clean dependency, source bodies/hash, wrapper probes, and status boundary agreed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; dependency worktree clean |
| Sourcegraph public API exact anchor-name query | 0 | 43 exhaustive matches in 8 repositories; response SHA-256 `425156...ac37` |
| GitHub REST repository query for `"continuity of probability" lean` | 0 | zero complete results; response SHA-256 `08c082...2600b2` |
| GitHub REST code query for the below anchor | 0 | HTTP 403 rate-limit blocker; no negative claim; response SHA-256 `1db366...386e` |
| immutable raw inspection of `optpku/ReasBook@7aee054.../section02_part4.lean` | 0 | specialized propositions 7.8/7.9 found; SHA-256 `b281b2...2868b` |

## Status boundary

This node audits and classifies formal candidates. Human primary-source pinpointing remains open.
No accepted proof receipt, readable reconstruction, hermetic build, independent validation, or
theorem-completion evidence is asserted.
