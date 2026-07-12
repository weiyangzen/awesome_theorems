# Statement validation

Base revision: `760cbc73b01804753c0dfb5f84b703dff6d026de`.

The preflight worktree contained only the pre-existing untracked `Formalizations/Lean/.lake` link.
It resolves to the canonical checkout's pinned Lake artifacts. No command fetched, updated, or wrote
dependencies. This phase adds an exact `Prop` expression, not a proof of that proposition.

## Commands and results

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630, `L0`, `rework_required: true`, statement-first lane, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0590/Statement.lean` | 0 | `THMM0590.brownDouglasFillmoreTarget.{u_2, u_3} : Prop` |
| minimal-import replay: remove two initially tested imports in a `/tmp` copy, then `cd Formalizations/Lean && lake env lean /tmp/THM-M-0590-min.lean` | 0 | Same `... : Prop` output; tracked module retains only `Mathlib.Analysis.InnerProductSpace.Adjoint` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the `lakefile.lean` pin |
| `python3 -m json.tool Stage1_Instances/THM-M-0590/statement.json >/dev/null` | 0 | Statement receipt JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0590` | 0 | No whitespace errors |

The pinned mathlib snapshot has compact-operator and Hilbert-space adjoint APIs but no general
Fredholm predicate or Fredholm-index declaration. `Statement.lean` therefore defines the standard
analytic notions explicitly: finite kernel and cokernel, closed range, their dimension difference,
and the Fredholm essential spectrum. This expands the literal invariant rather than substituting an
uninterpreted interface.

The semantic mutation decisions are structured in `statement.json`. Removing an essential-normality
or infinite-dimensional premise, changing `T - lambda I`, moving the lambda binder outside its
off-spectrum scope, or weakening the unitary to a mere linear equivalence is rejected.

## Boundary

This receipt demonstrates elaboration of the exact selected target with one pinned import. It is
not a proof receipt: `brownDouglasFillmoreTarget` is a definition of a proposition and is not
inhabited here. The root remains `M3`, source fidelity remains `H1`, and theorem completion is false.
