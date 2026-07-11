# S56-M-0395-STATEMENT validation

## Frozen target

`Stage1Rev56.THMM0395.Statement` is the exact Lean proposition selected from
the intake's Mordell-conjecture scope. It quantifies over a number field and a
curve datum over its spectrum, requires smoothness, properness, geometric
connectedness, dimension one, and genus at least two, and concludes finiteness
of the subtype of sections of the structure morphism.

The pinned mathlib revision does not supply a complete curve-genus object API.
Accordingly the five mathematical predicates are named fields of `CurveOver`,
and `IsFaltingsCurve` requires every field. They are not asserted, proved, or
silently dropped. `statement_iff_expanded` checks the quantifier expansion;
`finite_points_iff_finite_univ` checks the set/type finiteness encoding.

The primary-source theorem/page crosswalk remains open, so this establishes
exact elaboration of the selected intake scope, not H0 source fidelity. It
contains no proof of Faltings's theorem and grants no theorem-completion credit.

## Commands and results

Base revision: `d4f6f2514a650df5293be857999912996576c420`.

- `python3 Docs/tools/check_stage1_standard.py`: exit 0; 15 assurance groups,
  41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed.
- `python3 scripts/stage1_target.py check`: exit 0; 1546 unique targets with
  ranks 1 through 1546 passed.
- `python3 scripts/stage1_target.py show THM-M-0395`: exit 0; rank 8, L0,
  rework required, planned, theorem incomplete.
- From `Formalizations/Lean`, `lake env lean --version`: exit 0; Lean 4.29.0,
  commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- From `Formalizations/Lean`, `lake env lean ../../Stage1_Instances/THM-M-0395/Statement.lean`:
  exit 0; output `Stage1Rev56.THMM0395.Statement.{u} : Prop`.
- From `Formalizations/Lean`, removing each import in a temporary `/tmp` copy
  and running `lake env lean`: both runs exit 1; without `Properties`, `Scheme`
  and `Spec` are unavailable, and without `NumberField.Basic`, `NumberField` is
  unavailable. Thus neither of the two direct imports is removable.
- `python3 -m json.tool Stage1_Instances/THM-M-0395/statement.json`: exit 0.
- `git diff --check -- Stage1_Instances/THM-M-0395`: exit 0.

The clone's pre-existing untracked `Formalizations/Lean/.lake` link points to
the canonical already-materialized pinned cache. It was not modified. No
dependency fetch, update, build, or other `.lake` mutation was performed. This
is narrow worker evidence, not hermetic release evidence or master acceptance.
