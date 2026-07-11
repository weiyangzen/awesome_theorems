# THM-M-0418 Anchor-Audit Validation

Item: `S56-M-0418-ANCHOR_AUDIT`  
Base revision: `d76396d014ed07f02b5e64944c3eafca7d453d40`

## Result

The frozen target has an exact terminal candidate in pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`:
`NumberField.exists_ideal_in_class_of_norm_le` in
`Mathlib.NumberTheory.NumberField.ClassNumber`. Its universe-polymorphic field and class binders,
nonzero integral ideal subtype, represented-class orientation, weak norm endpoint, and explicit
real Minkowski constant match the canonical target. `AnchorAudit.lean` checks that match through an
exact repo-local wrapper, without changing or strengthening the statement.

The terminal declaration has an explicit `by` proof in the immutable source. Lean reports exactly
`propext`, `Classical.choice`, and `Quot.sound` for both the terminal and wrapper. The inspected
terminal body contains no `sorry`, bodyless axiom, `unsafe`, external implementation, or oracle
marker. The proof body remains upstream under Apache-2.0; the local adapter is a wrapper, so the
exact machine classification is `M0-W`, not `M0-L`. Acceptance of those standard axioms against
the target's eventual foundation profile remains a later validation gate.

The existing legacy `S1_M_073.statementShape_of_mathlib` is another wrapper over the same terminal
body and earns no duplicate proof credit. Bounded public searches found no additional candidate;
GitHub code search required authentication, so that lane is recorded as blocked rather than
negative.

## Commands And Results

Commands ran on 2026-07-12 in this worker clone. Lean used only the existing pinned `.lake`
artifacts; no update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0418/AnchorAudit.lean` | 0 | Exact wrapper elaborated; terminal and wrapper each reported `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0418/Statement.lean` | 0 | Frozen target and statement transport re-elaborated |
| `python3 Stage1_Instances/THM-M-0418/check_anchor_audit.py` | 0 | Exact candidate, statement fingerprint, manifest pin, clean installed mathlib tree, source/license hashes, body scan, and status boundary agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-0418/anchor-audit.json` | 0 | Valid JSON |
| `rg -n -i 'Minkowski...|exists_ideal_in_class_of_norm_le' ...` | 0 | Located the terminal mathlib theorem and duplicate repo-local wrappers; no distinct local terminal body |
| Sourcegraph exact and alias queries | 0 | Both completed with `matchCount=0`; response hashes are recorded in `anchor-audit.json` |
| GitHub repository metadata query | 0 | HTTP 200, `total_count=0`, complete response; hash recorded |
| GitHub code API query | 0 | Response captured as HTTP 401; explicitly not counted as a negative result |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 standard and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0418` | 0 | Rank 73, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0418` | 0 | No whitespace errors |

## Status Boundary

This is a completed, bounded anchor audit pending master acceptance. Although the exact root has a
checked `M0-W` candidate, the theorem is not rev-5.6 complete: the obligation registry, typed
graphs, human-source and readability audits, trust closure, hermetic release, and independent
verification remain later phases.
