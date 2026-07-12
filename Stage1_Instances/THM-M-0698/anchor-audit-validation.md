# Anchor-audit validation record

Item: `S56-M-0698-ANCHOR_AUDIT`  
Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`

## Result

Pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact theorem
`FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable` in
`Mathlib.ModelTheory.Satisfiability`. Its type is the statement-gate target. The forward implication
is monotonicity to finite subtheories; the reverse implication constructs an ultraproduct indexed
by finite subtheories and packages the satisfying structure as a `ModelType`.

`AnchorAudit.lean` checks a standalone exact wrapper against the pinned compiled dependency.
`#print axioms` reports `propext`, `Classical.choice`, and `Quot.sound` for both the upstream theorem
and wrapper, with no target-specific axiom. The source has SHA-256
`0abb92d531851a57909945b740981d79a4cbb29238f2a3d21cb5fa57aa143edb` and Apache-2.0 license.
Immutable blame traces the principal terminal body to mathlib commit
`4a1f49bf7cc9dd32cb1dffe3687870901edc4193` (2023-05-25).

The bounded external search found only mathlib4 for the exact declaration name. The GitHub code
lane was rate-limited and is recorded as a blocker, not a negative result. No external integration
is needed because the exact candidate is already in the manifest-pinned dependency closure.

This phase records an `M0-W` candidate pending the ordered obligation-tree and proof gates. It does
not promote the root, accept proof credit, or claim audit/theorem completion.

## Commands and results

Commands ran on 2026-07-12 inside the worker clone. Existing `.lake` artifacts were used read-only;
no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0698` | 0 | rank 739; planned; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386...ea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0698/Statement.lean` | 0 | prerequisite exact target re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0698/AnchorAudit.lean` | 0 | exact wrapper and four probes elaborated; both axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0698/check_anchor_audit.py` | 0 | exact anchor, pin, workflow boundary, and schema passed |
| `rg -n -i 'compactness\|isFinitelySatisfiable' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | exact pinned model-theory theorem located; unrelated uses were not credited |
| Sourcegraph API query in `anchor-audit.json` | 0 | six matches, all in mathlib4; response hash `fa646503...fd0e7` |
| GitHub REST repository query in `anchor-audit.json` | 0 | complete zero-result response; hash `08c082fd...2600` |
| GitHub REST code query in `anchor-audit.json` | 0 | HTTP 403 rate-limit blocker; response hash `1db366a2...e386e` |
| `python3 -m json.tool Stage1_Instances/THM-M-0698/anchor-audit.json` | 0 | valid JSON |
| forbidden-token scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, or `axiom` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0698 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open gates

Master acceptance is still required. Later phases must freeze the typed obligation and provenance
graphs, decide proof credit independently, and run the full trust, hermetic, readability, source,
and independent-validation gates before any theorem-completion claim.
