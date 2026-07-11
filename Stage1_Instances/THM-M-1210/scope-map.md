# Scope map

## Preserved source scope

- Subject: solutions of an unspecified dispersive equation.
- Claimed property: an unspecified local smoothing effect.
- Attribution and period: multiple mathematicians, twentieth century.
- Repository status label: `已验证`, treated as untrusted metadata only.

This is all that the repository source fixes. In particular, "local" might mean spatial
localization rather than short time, and "smoothing" might denote a derivative gain in a
space-time estimate; intake does not choose an interpretation.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze the equation and propagator,
dimension and scalar field, initial-data class, time interval, spatial cutoff or weight, norms,
derivative multiplier and gain, exponent range and endpoints, constant dependencies, and whether
the result is homogeneous, inhomogeneous, global, variable-coefficient, or manifold-valued.
Degenerate data and any low-dimensional or endpoint exclusions must be explicit.

## Explicit exclusions

- Substituting the separately listed Sogge wave-equation theorem or local smoothing conjecture.
- Choosing a Schrödinger, wave, Kato smoothing, Strichartz, or restriction estimate merely because
  a convenient Lean API exists.
- Treating generic Sobolev regularity or semigroup continuity as dispersive local smoothing.
- Using legacy slot `S1_M_142`, which is a Penrose-inequality artifact for another theorem ID.
- Treating `已验证` as primary-source or kernel evidence.
