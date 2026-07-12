# THM-M-1395 rev-5.6 intake

`THM-M-1395` is the ordinary-differential-equations catalog item `有限差分法` (finite
difference method). The repository supplies only the gloss `ODE的数值解法` (a numerical method
for ODEs), an attribution to many mathematicians, the twentieth century, and an untrusted
`已验证` label. These fields name a method family; they do not state a truth-valued theorem.

## Intake result

This dossier creates a fail-closed `planned` instance and preserves that ambiguity. For an ODE,
"finite difference method" may mean a difference-quotient approximation, a concrete initial- or
boundary-value recurrence, a consistency or truncation-error estimate, a stability result, a
convergence theorem, or a global error bound. Each choice changes the variables, hypotheses,
conclusion, proof architecture, and even the discrete problem being studied.

The same-name catalog item `THM-M-1465` has the distinct gloss `偏微分方程的差分离散` (finite-
difference discretization of PDEs). Its scope and any eventual evidence remain separate. Nearby
items for shooting, Runge-Kutta, Adams, stiffness, and backward differentiation likewise grant no
statement or proof credit to this target.

## Source and formal boundary

No primary or authoritative source is cited by the repository. A modern finite-difference textbook
was inspected only as a subject-family guide: its chapter structure separates ODE initial-value,
zero-stability/convergence, absolute-stability, stiff-ODE, and boundary-value results. It therefore
confirms the material ambiguity but does not select a canonical proposition.

`IntakeProbe.lean` elaborates only adjacent pinned APIs: the algebraic forward-difference operator
and Newton identities, ODE integral-curve predicates, and a generic Taylor remainder bound. These
interfaces neither define a numerical ODE scheme nor state its consistency, stability,
convergence, or error theorem. A bounded exact-topic search found no such result in repo-local Lean
or pinned mathlib; this is intake discovery only, not the later anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H5, M4, R4]`: `H5` classifies the supplied method label as not yet a stable proposition; it
does not refute correctly stated finite-difference theorems. No exact formal artifact or source-
faithful proof reconstruction is identified. All six downstream tasks remain open. No H0, M0, R0,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
