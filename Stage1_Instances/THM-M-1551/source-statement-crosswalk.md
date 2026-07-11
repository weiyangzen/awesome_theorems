# Source-statement crosswalk

## Candidate primary sources

- V. E. Zakharov and A. B. Shabat, "A scheme for integrating the nonlinear equations of
  mathematical physics by the method of the inverse scattering problem. I," *Functional Analysis
  and Its Applications* 8 (1974), 226-235 (English translation). This is a primary candidate for
  the auxiliary-system compatibility construction; the original/translation equation numbering,
  hypotheses, and errata have not yet been inspected for statement freeze.
- M. J. Ablowitz, D. J. Kaup, A. C. Newell, and H. Segur, "The inverse scattering transform-Fourier
  analysis for nonlinear problems," *Studies in Applied Mathematics* 53 (1974), 249-315. This is a
  primary candidate for a concrete compatibility representation; exact equations, assumptions,
  edition pagination, and errata remain to be inspected.

These bibliographic anchors are discovery leads, not `H0` evidence. "Zero-curvature representation"
names a method/family rather than one uniquely determined theorem, so source selection is a genuine
statement gate.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| zero-curvature representation | compatibility of two auxiliary evolutions | mixed-action/operator compatibility theorem | included; exact equations open |
| connection potentials | source matrices or Lie-algebra-valued coefficients | typed functions and multiplication/bracket | included; model open |
| curvature | derivative difference plus commutator | derivatives and sign-correct algebraic expression | included; convention open |
| spectral parameter | parameter in the auxiliary problem | explicit domain and quantifier | conditional on source |
| integrable equation | coefficient conditions equivalent to compatibility | concrete PDE and checked bidirectional bridge | source/equation open |

## Existing Lean boundary

The legacy `S1_M_210.lean` chooses an abstract Lie algebra `L`, linear maps `Dx` and `Dt`, and
elements `U` and `V`. Its checked wrappers establish algebraic rearrangement and constant-transform
facts at that abstraction boundary. They do not identify a primary-source auxiliary problem,
derivatives of coefficient functions, spectral dependence, or a concrete nonlinear equation.
Consequently they cannot determine or close the canonical rev-5.6 statement.

Before `H0`, an independent reviewer must verify the chosen source edition, exact equation/theorem
anchor, all assumptions and conventions, errata, and every row of the source-to-Lean mapping.
