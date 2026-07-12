# Anchor audit record

Item: `S56-M-1521-ANCHOR_AUDIT`  
Base revision: `bc7ff7c864291d915984b6d9312ed0ea7d160161`

## Result

The immutable mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains an exact two-declaration route to the frozen target:

1. `MeasureTheory.MeasurePreserving.conservative` turns preservation of a finite
   measure into `MeasureTheory.Conservative f mu`.
2. `MeasureTheory.Conservative.ae_mem_imp_frequently_image_mem` proves that almost
   every point starting in each null-measurable set returns infinitely often.

`AnchorAudit.lean` composes these declarations into
`exactTargetFromPinnedMathlib`, whose proposition repeats the frozen target
verbatim. The statement-phase elaborated hash remains the identity authority;
this audit does not replace it. The candidate is feasible as a later `M0-W`
wrapper because its dependency is already in the pinned Lake closure. No proof
credit or state promotion occurs in this phase.

The stronger candidate
`MeasureTheory.Conservative.ae_frequently_mem_of_mem_nhds` adds topological,
second-countability, and measurable-open assumptions, so it is an alternate
anchor rather than a substitute for the exact root. The legacy local
`AwesomeTheorems.Stage1.S1_M_180.statementShape_from_mathlib` is only a wrapper
over the same terminal bodies and receives no duplicate provenance credit.

## Provenance and trust

The terminal source is
`Mathlib/Dynamics/Ergodic/Conservative.lean` in mathlib's Apache-2.0 repository.
The checked-out mathlib Git object equals the manifest pin and has commit date
`2026-03-30T18:47:58Z`. Inspection of the relevant source slice found concrete
theorem bodies and no `sorry`, `admit`, new `axiom`, or bodyless declarations.
Lean reports the standard mathlib logical dependencies `propext`,
`Classical.choice`, and `Quot.sound` for both terminal declarations and the
composed witness. Later trust/profile validation remains required.

## Search boundary

Repository-local Lean/Markdown, the full pinned mathlib source, and all locally
pinned dependency sources were searched. The only exact route found was the
mathlib chain above; the legacy file duplicates it. GitHub's unauthenticated
code-search API returned HTTP 403 and grep.app returned HTTP 429. Per worker
policy no dependency was cloned or fetched. Consequently, the external-project
inventory is explicitly incomplete and no claim is made that other immutable
Lean 4 formalizations do not exist.

## Commands and results

Commands ran in this worker clone and did not mutate `.lake`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-1521/check_anchor.py` | 0 | frozen statement compiled to a temporary module cache; exact wrapper elaborated against that module; all three axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-1521/check_statement.py` | 0 | frozen expression SHA-256 `3d7c202adf1f52ae3dbcdb46e7726395600cb0d89d93220d70d42b9b837f6c06`; all four statement mutations distinguished |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to `lake-manifest.json` |
| `rg` searches over repo-local and `.lake/packages` Lean/Markdown sources | 0 | exact mathlib chain plus its legacy wrapper found; topological alternate classified separately |
| GitHub code-search API request | 22 | HTTP 403; remote search not credited |
| grep.app API request | 22 | HTTP 429; remote search not credited |
| `python3 -m json.tool Stage1_Instances/THM-M-1521/anchor-audit.json` | 0 | structured audit parses |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `git diff --check -- Stage1_Instances/THM-M-1521 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Status boundary: the anchor-audit item is self-tested and awaits master
acceptance. `audit_complete=false` and `theorem_complete=false`; obligation-tree,
proof, validation, release, source acceptance, and readability gates remain open.
