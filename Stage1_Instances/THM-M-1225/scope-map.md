# Scope map

## Included source family

- Nonlinear wave equations in an energy-critical regime, attributed in repository metadata to
  Terence Tao and dated 2006.
- A concrete Cauchy-problem theorem whose equation, spatial dimension, sign/nonlinearity, initial
  data class, solution notion, and conclusion must all be stated explicitly.
- The first source candidate to inspect is Tao's 2006 preprint arXiv:math/0601164, *Global
  regularity for a logarithmically supercritical defocusing nonlinear wave equation for
  spherically symmetric data*. Its title is not itself an energy-critical theorem, so it cannot be
  adopted without locating a theorem that matches the repository phrase.

## Statement-phase decisions

Primary-source inspection must determine whether the intended result is (a) a theorem in the
energy-critical three-dimensional defocusing quintic theory, (b) Tao's nearby logarithmically
supercritical radial result, or (c) another 2006 Tao source. It must freeze the exact theorem/page,
equation and sign convention, dimension, critical exponent, radial assumptions, data spaces,
regularity, existence interval, uniqueness, scattering or bounds, and all boundary cases.

Only after that decision may the work assign ordered Lean binders, universes, concrete derivative
and Laplacian encodings, an environment fingerprint, or an exact-statement hash.

## Explicit exclusions

- Substituting the distinct Grillakis regularity target `THM-M-1224` or Ginibre-Velo local
  well-posedness target `THM-M-1222`.
- Silently replacing energy-critical with logarithmically supercritical, or omitting a radial
  hypothesis found in the selected source.
- Focusing/defocusing, dimensional, exponent, local/global, regularity/well-posedness, or
  scattering variants not supported by the selected theorem.
- An abstract structure that assumes the PDE solution or desired conclusion as a field.
- Energy identities, Strichartz estimates, metadata records, or finite-dimensional analogues
  presented as the terminal theorem.
