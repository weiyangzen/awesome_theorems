# THM-M-1394 rev-5.6 intake

`THM-M-1394` is the ordinary-differential-equations catalog item `打靶法` (shooting method). The
repository supplies only the gloss `边值问题的数值方法` (a numerical method for boundary-value
problems), an attribution to many mathematicians, the twentieth century, and an untrusted `已验证`
label. These fields name a method family; they do not state a truth-valued theorem.

## Intake result

This dossier creates a fail-closed `planned` instance and preserves that ambiguity. Shooting can
refer to reducing a scalar or system boundary-value problem to an initial-value family, proving a
root of an endpoint residual exists, single or multiple shooting, choosing a root solver, proving
local convergence, or analyzing stability and numerical error. Each choice changes the variables,
hypotheses, conclusion, proof architecture, and arithmetic model.

Nearby items own generic boundary-value problems, Green representations, the Fredholm alternative,
finite differences, Runge-Kutta, and Adams methods. Their statements and evidence grant no credit
to this target. In particular, selecting a familiar scalar second-order shooting theorem would add
mathematics that is absent from the catalog.

## Source and formal boundary

No primary or authoritative source is cited by the repository. Bibliographic metadata for Bailey
and Shampine's 1968 paper on shooting methods and for Morrison, Riley, and Zancanaro's 1962 paper
on multiple shooting was inspected only as method-family evidence. The papers' exact theorem text,
definitions, assumptions, proof boundaries, corrections, and independent review were not accepted,
so they select no canonical proposition and supply no H0 credit.

`IntakeProbe.lean` elaborates only adjacent pinned APIs for exact ODE integral curves, local initial-
value existence, uniqueness, approximate-trajectory bounds, and the intermediate value theorem.
They define no boundary residual, shooting parameter, single or multiple shooting algorithm, root
solver, or method-specific convergence/error theorem. A bounded exact-topic search found no named
shooting-method declaration in repo-local Lean or pinned mathlib; this is intake discovery only,
not the downstream anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H5, M4, R4]`: `H5` classifies the supplied method label as not yet a stable proposition; it
does not refute correctly stated shooting-method theorems. All six downstream tasks remain open.
No H0, M0, R0, accepted state, audit completion, theorem completion, or master acceptance is
claimed.
