# THM-M-1396 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Runge-Kutta方法` (Runge-Kutta method). The catalog supplies only the gloss `ODE的数值积分`
(numerical integration of ODEs), attributes the item to Carl Runge and Martin Kutta, gives the
year 1895, and labels it `已验证`. Those fields identify a numerical-method family, not a
truth-valued proposition with ordered binders, hypotheses, and a conclusion.

## Intake result

Runge-Kutta methods include explicit and implicit schemes with different tableaux, stage counts,
orders, error estimates, convergence hypotheses, and stability properties. Even the phrase
"classical RK4" requires a selected update formula and a theorem about it. The catalog does not
choose a method definition, an initial-value problem, an exact-arithmetic model, consistency or
order conditions, a local or global error statement, a convergence result, or a stability claim.
Selecting one from memory would invent or substitute mathematics.

Carl Runge's 1895 article, *Ueber die numerische Aufloesung von Differentialgleichungen*, is an
inspected primary historical discovery lead. Its bibliographic identity and issue scan agree with
the catalog attribution and year. The repository does not cite the article, select an exact result
from it, or explain how a historical construction maps to a modern Runge-Kutta theorem. Kutta's
1901 paper and Butcher's modern monograph remain bibliographic leads only. None supplies an
accepted canonical root or `H0` evidence at intake.

The provisional vector is `[H5, M4, R4]`. Here `H5` says that the supplied method label and gloss
are not yet a stable proposition; it does not say that Runge-Kutta results are false or open.
Pinned mathlib supplies analytic ODE and error-bound ingredients, but the bounded intake search
found no named Runge-Kutta declaration. `IntakeProbe.lean` checks adjacent pinned APIs only and
states no target theorem.

The structured scope authority is `instance.json`. `scope-map.md` records proposition-changing
choices and prohibited substitutions, while `source-statement-crosswalk.md` maps every repository
phrase and the inspected source leads to the open statement decisions. All six downstream phases
remain open in `task-dag.json`. No canonical proposition, accepted source, exact Lean statement,
proof body, H0, M0, R0, accepted execution state, audit completion, theorem completion, or master
acceptance is claimed.
