# Scope map

## Included topic boundary

- A source-selected dispersive equation or evolution operator and its solution/propagator.
- A source-selected spatial domain, dimension, time domain, measures, and scalar field.
- The precise initial-data or forcing space and mixed space-time output norm.
- The admissibility/scaling conditions on every exponent, including all excluded endpoints.
- The exact homogeneous, inhomogeneous, retarded, local-time, or global-time conclusion selected
  from the source, with the dependence of its constant.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different targets:

1. Free wave, Schrodinger, Klein-Gordon, another concrete equation, or an abstract unitary group
   satisfying an energy bound and a dispersive decay estimate.
2. Homogeneous control of `U(t) f` or an inhomogeneous/Duhamel estimate for a forcing term.
3. Euclidean space, a manifold, or another geometry; global time or a finite interval.
4. The exponent relation, conjugate exponents, Sobolev regularity/derivative loss, radial
   assumptions, and whether endpoint pairs are included.
5. Iterated mixed norms versus a single norm on a product measure space, and strong versus weak
   endpoint spaces.

The statement phase must inspect an immutable source and freeze one proposition, ordered binders,
all norm and measurability conventions, hypotheses, conclusion, and boundary cases. It must not
silently combine classical variants.

## Explicit exclusions

- The Keel-Tao endpoint theorem, which has its own target `THM-M-0382`, as an automatic substitute.
- A Fourier restriction theorem, local smoothing estimate, dispersive pointwise decay estimate,
  or nonlinear well-posedness theorem without the selected space-time estimate.
- An abstract structure that contains the desired inequality as an assumed field followed by a
  projection theorem.
- A tautological norm inequality unrelated to the selected evolution equation.
- Legacy Stage1 interfaces mentioning Strichartz estimates as proof evidence.
- The repository label `已验证` as evidence of a human proof or kernel closure.

No canonical Lean target is frozen at intake because the repository source record does not identify
a unique equation, exponent range, norm inequality, or proposition.
