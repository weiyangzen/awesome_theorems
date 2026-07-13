# THM-M-1476 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the numerical-analysis catalog
label `刚性稳定性` (stiff stability). The repository supplies only the gloss
`刚性问题的数值稳定性` (numerical stability of stiff problems), attributes it to many
mathematicians in the twentieth century, and labels it `已验证`. That wording identifies a topic
or result family, not a truth-valued proposition with ordered binders, hypotheses, and a
conclusion. The verified label is untrusted metadata and supplies neither source nor proof credit.

## Intake result

The record does not define a stiff problem or select an ODE, DAE, PDE, scalar test equation,
numerical method, stability notion, norm, time horizon, step regime, or exact conclusion. In the
literature, stiff stability can be attached to multistep or multiderivative methods and related to
several distinct A-stability variants. Choosing backward Euler, a Runge-Kutta or BDF scheme,
Dahlquist's test equation, A-stability, L-stability, or any convenient decay statement would
therefore invent or substitute proposition-changing mathematics.

Crossref metadata for Rolf Jeltsch's 1976 paper on stiff stability and its relation to
`A_0`- and `A(0)`-stability, his 1977 paper on stiff stability of multistep multiderivative
methods, and the 1979 corrigendum is recorded as source-family discovery only. The catalog cites
none of these works, and no complete paper, definition, theorem passage, assumptions, proof
boundary, or correction impact has been admitted and independently reviewed. No lead receives
`H0` credit.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned continuous-ODE, trajectory-error, and complex-decay
interfaces. A bounded exact-topic search found no source-selected stiff-stability declaration in
pinned mathlib or repo-local Lean. The probe and search are feasibility observations only, not a
canonical target, exhaustive anchor audit, proof, or absence theorem.

The canonical human statement and Lean expression remain null. The provisional root vector is
`[H5, M4, R4]`: the received catalog wording is not yet a stable proposition; no source-identical
usable formal artifact is credited; and no readable proof can attach to an unfrozen root. `H5`
does not refute established stiff-stability results. All six downstream tasks remain open. No
accepted state, audit completion, theorem completion, receipt acceptance, or master acceptance is
claimed.
