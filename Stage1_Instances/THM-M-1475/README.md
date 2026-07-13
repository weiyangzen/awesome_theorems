# THM-M-1475 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the numerical-analysis catalog
label `龙格-库塔法的稳定性` (stability of Runge-Kutta methods). The repository supplies only the
gloss `RK方法的稳定性区域` (stability regions of RK methods), attributes the topic to many
mathematicians in the twentieth century, and labels it `已验证`. A topic and definition-family
gloss do not form a truth-valued proposition with ordered binders, hypotheses, and a conclusion.
The verified label is untrusted metadata and supplies neither source nor proof credit.

Runge-Kutta stability can mean the amplification recurrence for the scalar test equation, the
general tableau formula for a stability function, the definition or computation of an absolute
stability region, a region equality or inclusion for one named method, or A-, L-, B-, algebraic,
contractive, or nonlinear stability. These alternatives require different tableaux, equations,
domains, invertibility conditions, norms, boundary conventions, and conclusions. The catalog
selects none of them. In particular, writing down the familiar general-tableau rational function
or choosing Euler, RK4, Gauss, or Radau would invent proposition-changing mathematics.

Two modern source-family leads were inspected without admitting either as the target source.
Hairer and Wanner's *Solving Ordinary Differential Equations II* places explicit Runge-Kutta
stability analysis in Chapter IV.2 and implicit stability functions and A/L stability in IV.3;
its author-hosted correction sheet contains a material L-stability correction. The immutable
source of Driscoll and Braun's *Fundamentals of Numerical Computation* defines absolute stability
and stability regions and gives method-specific examples, but it covers Runge-Kutta and multistep
methods together and does not identify which proposition the catalog intended. No pinpoint
definition/theorem has been selected, transported, reviewed, or credited as `H0`.

Pinned mathlib supplies complex, finite-matrix, rational-function, and analytic ODE interfaces.
`IntakeProbe.lean` authenticates a narrow adjacent API surface only. A bounded exact-topic search
found no named Runge-Kutta stability declaration. Neither fact selects the theorem or supplies
proof credit.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received catalog topic as not yet a
stable proposition; it does not refute established Runge-Kutta stability results. All six
downstream phases remain open. No canonical mathematical or Lean statement, accepted source,
proof body, H0, M0, R0, accepted execution state, audit completion, theorem completion, accepted
receipt, or master acceptance is claimed.
