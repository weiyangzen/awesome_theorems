# THM-M-1478 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the numerical-analysis catalog
label `L-稳定性` (L-stability). The repository supplies only the gloss `数值方法的稳定性`
(stability of numerical methods), attributes it to many mathematicians in the twentieth century,
and labels it `已验证`. A named property and topic gloss do not form a truth-valued proposition
with ordered binders, hypotheses, and a conclusion. The verified label is untrusted metadata and
supplies neither source nor proof credit.

In ordinary differential-equation numerics, L-stability is commonly discussed using a scalar test
equation and a stability function. Even that familiar context leaves proposition-changing choices:
the numerical-method class, stability-function construction and domain, pole policy, the exact
A-stability condition, the filter or path used for decay at infinity, and whether the target is a
definition, characterization, existence theorem, or a property of one named method. The catalog
selects none of them. Installing the remembered slogan "A-stable and decays at infinity" or proving
it for backward Euler, Radau, an SDIRK method, or a rational approximation would invent or
substitute mathematics.

Hairer and Wanner's *Solving Ordinary Differential Equations II* was inspected only as a modern
source-family lead. Its table of contents separates the stability function, A-stability, and
L-stability in Chapter IV.3, pages 40-49. The authors' correction sheet for the 2010 printing also
changes an L-stability parameter range on page 98. The catalog cites neither this book nor any
definition, theorem, method, or page. No exact proposition, complete assumption/proof/correction
crosswalk, or independent review is admitted, so the lead supplies no `H0` credit.

Pinned mathlib supplies complex limits at infinity, rational-function evaluation, finite matrices,
and analytic ODE interfaces. `IntakeProbe.lean` authenticates only that adjacent API surface. A
bounded exact-topic search found no source-selected L-stability declaration. Neither observation
selects a target statement or supplies proof credit. Mathlib's `RatFunc.eval` is total and returns
zero when the reduced denominator evaluates to zero, so a future encoding must separately preserve
the source-selected pole and implicit-stage-solvability semantics rather than treating totalized
evaluation as a stability certificate.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received catalog wording as not yet
a stable proposition; it does not refute established L-stability definitions or theorems. All six
downstream phases remain open. No canonical mathematical or Lean statement, accepted source,
proof body, H0, M0, R0, accepted execution state, audit completion, theorem completion, accepted
receipt, or master acceptance is claimed.
