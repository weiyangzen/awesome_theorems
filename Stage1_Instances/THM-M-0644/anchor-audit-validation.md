# Anchor-audit validation

Item: `S56-M-0644-ANCHOR_AUDIT`  
Base revision: `34b51889997c961b0ad69413dae1dc249a8cf744`  
Audit date: 2026-07-12

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains an exact Lean 4
candidate in `Mathlib.ModelTheory.Satisfiability`:
`FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable`. Its binders and conclusion
match the frozen target without transport. The source body proves the restriction direction by
monotonicity and the compactness direction by an ultraproduct indexed by finite subtheories.

`AnchorAudit.lean` checks the upstream declaration and a repo-local exact-type wrapper. Lean reports
the axiom profile `[propext, Classical.choice, Quot.sound]` for both. The installed source has
SHA-256 `0abb92d5...43edb`; its header records Apache-2.0 and Aaron Anderson as author. A scoped scan
found no `sorry` or `admit`. These facts make the declaration an `M0-L` candidate already available
through the pinned dependency, rather than anchor-only integration debt.

Public external searches found no additional candidate. Sourcegraph returned no indexed exact-name
match, and GitHub repository search returned zero complete results. GitHub code search was blocked
by its unauthenticated rate limit, so no negative claim is made for that lane. Search responses are
content-hashed dated discovery records, not immutable proof evidence.

This phase audits and locally checks the formal anchor only. Accepted root `M0`, human-source `H0`,
obligation/composition closure, full transitive trust and provenance, hermetic replay, and
independent validation remain later gates; theorem completion is false.

## Commands and results

All commands ran inside this worker clone. No Lake update/build, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0644/AnchorAudit.lean` | 0 | Exact upstream declaration and wrapper elaborated; both axiom profiles were `[propext, Classical.choice, Quot.sound]` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/.lake/packages/mathlib/Mathlib/ModelTheory/Satisfiability.lean` | 0 | `0abb92d531851a57909945b740981d79a4cbb29238f2a3d21cb5fa57aa143edb` |
| `rg -n '(sorry\|admit)' Formalizations/Lean/.lake/packages/mathlib/Mathlib/ModelTheory/Satisfiability.lean` | 1 | Expected no-match status |
| Sourcegraph exact-name API search | 0 | `matchCount=0`; response SHA-256 `fb2c109b...741201` |
| GitHub REST repository search | 0 | `total_count=0`, `incomplete_results=false`; response SHA-256 `08c082fd...2600b2` |
| GitHub REST code search | 0 | Rate-limit blocker recorded; response SHA-256 `1db366a2...5e386e` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0644` | 0 | Rank 690, planned, theorem incomplete |
| JSON parse and scoped invariant checks | 0 | Item identity, pins, hashes, candidate selection, and incomplete boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0644 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Next gate

The obligation-tree phase must freeze the proof/provenance/trust denominators and decompose the
ultraproduct body before proof credit is accepted. Later validation must resolve the complete
transitive declaration closure and independently replay the exact wrapper.
