# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1389`, the label `Weyl渐近公式`, Hermann Weyl, the year
1911, the gloss `特征值的渐近分布`, and an untrusted `已验证` status. Intake preserves that
spectral-asymptotics family boundary. It does not assume that the surrounding ordinary-differential-
equations category selects a Sturm-Liouville theorem, or that the historical attribution silently
selects a multidimensional PDE/Laplacian law.

## Proposition-changing decisions

An approved source decision must freeze all of the following before statement elaboration:

- the operator: Dirichlet or Neumann Laplacian, a variable-coefficient elliptic operator, a regular
  or singular Sturm-Liouville operator, a compact self-adjoint operator, or another source-fixed
  model;
- the geometric and analytic carrier: interval, bounded Euclidean domain, compact Riemannian
  manifold, boundary regularity, dimension, measure, metric, coefficients, operator/form domain,
  and scalar field;
- ellipticity, self-adjointness, semiboundedness, compact resolvent, coefficient regularity and
  positivity, domain regularity, and every hypothesis making the relevant spectrum discrete;
- boundary conditions and the treatment of zero modes, negative spectrum, disconnected domains,
  repeated eigenvalues, multiplicities, and index origin;
- whether the root uses ordered eigenvalues `lambda_n`, a counting function `N(lambda)`, a heat
  trace, or another checked encoding, and the exact relationships among alternate encodings;
- the asymptotic variable and filter, normalization, exponent, volume/geometric factor, Fourier
  convention, unit-ball constant, and equality/equivalence/limit notation;
- whether only the leading Weyl term is asserted or also a remainder, second term, boundary term,
  uniformity statement, multiplicity clause, or inverse eigenvalue asymptotic; and
- exact ordered binders, all hypotheses, the conclusion, exceptional cases, and which claims are
  proved by the selected source rather than added from later generalizations.

These choices produce materially different propositions. This list is a resolution ledger, not a
canonical theorem claim.

## Candidate families not credited

- A multidimensional Dirichlet-Laplacian counting law on a bounded Euclidean domain,
  `N(lambda) ~ (omega_d / (2*pi)^d) * volume(Omega) * lambda^(d/2)` under source-fixed assumptions.
- The equivalent ordered-eigenvalue growth formula for that same operator.
- A Weyl law for the Laplace-Beltrami operator on a compact Riemannian manifold, with or without
  boundary.
- A leading eigenvalue asymptotic for a regular one-dimensional Sturm-Liouville problem.
- A variable-coefficient elliptic-operator law with a phase-space-volume leading term.
- A strengthened two-term or remainder estimate, heat-trace law, or other Tauberian equivalent.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor and substitution boundaries

- `THM-M-1384` Sturm-Liouville theory and `THM-M-1388` the eigenvalue problem may supply future
  definitions, but do not determine this target's asymptotic law.
- `THM-M-1385` Sturm comparison, `THM-M-1386` Sturm separation, `THM-M-1387` oscillation theory,
  `THM-M-1390` Courant's min-max principle, and `THM-M-1391` the Pruefer transformation are distinct
  results. They may appear in a future proof architecture but cannot replace the asymptotic root.
- A finite-dimensional eigenvalue list, eigenbasis, compactness theorem, Rayleigh quotient, or
  generic `IsEquivalent` interface is substrate, not a Weyl asymptotic theorem.
- A one-dimensional formula cannot substitute for a multidimensional PDE law, and the converse is
  equally invalid, unless an admitted source and checked relationship select the specialization.
- A heat-trace or phase-space statement requires a checked equivalence to the source-selected
  eigenvalue or counting formulation before receiving root credit.
- Numerical spectra, finite-element convergence, plots, sampled ratios, or floating-point volume
  constants are not proof of the asymptotic statement.
- The catalog label `已验证` supplies neither human-source fidelity nor kernel evidence.

## Boundary cases

The statement phase must decide dimension zero or one; empty, point, disconnected, nonsmooth, or
unbounded domains; manifolds with or without boundary; Dirichlet, Neumann, Robin, mixed, periodic,
or singular endpoint conditions; zero and negative eigenvalues; multiplicity and enumeration;
finite versus infinite spectra; compact-resolvent failure and essential spectrum; degenerate or
nonsymmetric coefficients; zero volume; normalization at `lambda = 0`; integer-valued counting
functions versus real-valued coercions; powers at zero; asymptotic filters through natural or real
parameters; and whether any remainder is uniform over a family.

No case is excluded before one proposition is selected.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks generic asymptotic-equivalence
and finite-dimensional self-adjoint spectrum APIs. A bounded exact-topic search found no Weyl-law,
spectral-counting, or eigenvalue-asymptotic declaration in pinned mathlib or repo-local Lean. This is
intake discovery only, not an exhaustive anchor audit or a global absence claim.
