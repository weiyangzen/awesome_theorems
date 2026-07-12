# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1392`, the title `Green函数`, the gloss `边值问题的积分表示`,
the attribution to George Green, and the year 1828. Its catalog category is ordinary differential
equations. Importance `high` and status `已验证` are metadata, not human-source or kernel evidence.

The received wording constrains the target to a Green-function integral representation for an ODE
boundary-value problem. It does not identify one proposition. Catalog adjacency to boundary-value,
Sturm--Liouville, spectral, and Prüfer entries is discovery context only and cannot supply missing
hypotheses.

## Candidate interpretations not credited

1. A regular second-order Sturm--Liouville problem on a compact interval whose nonresonant inverse
   is an integral operator with a piecewise Green kernel.
2. A scalar linear second-order two-point boundary-value problem represented using left- and
   right-adapted fundamental solutions and their Wronskian.
3. A first-order linear system or higher-order scalar equation represented by a matrix-valued
   Green kernel.
4. Existence or uniqueness of a Green function, rather than the representation identity itself.
5. A resolvent-kernel identity at a spectral parameter, possibly together with left- and
   right-inverse statements.

These possibilities differ in domains, binders, hypotheses, conclusions, and degenerate cases.
None is selected or asserted at intake.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- the exact theorem or source-defined conjunction, incorporated definitions, and proof boundary;
- scalar field, finite interval and endpoint order, state dimension, universes, and typeclasses;
- differential order and operator sign convention; coefficient functions, regularity, positivity,
  and weight or measure;
- separated or coupled boundary functionals and Dirichlet, Neumann, Robin, periodic, or other
  endpoint conditions;
- forcing-data space, solution space, classical or weak solution notion, and equality convention;
- existence, uniqueness, invertibility, or nonresonance hypotheses, including whether a spectral
  parameter is excluded from the spectrum;
- normalized fundamental solutions, Wronskian orientation, Green-kernel sign, piecewise branch,
  diagonal convention, continuity, and derivative-jump condition;
- the exact integral measure and whether the result is pointwise, almost everywhere, in norm, or
  an operator equality;
- whether the conclusion is one representation formula, both inverse identities, existence and
  uniqueness, or an equivalence; and
- ordered quantifiers, all hypotheses, all alternate encodings and checked transports, historical
  attribution, edition, translation, corrections, errata, and source-node mapping.

## Degenerate and boundary cases

The selected source must resolve an empty or zero-length interval, reversed endpoints,
zero-dimensional or scalar carriers, zero forcing, homogeneous boundary data, a zero coefficient
or weight, a vanishing Wronskian, an eigenvalue or zero mode, singular endpoints, endpoint atoms,
the kernel diagonal, repeated eigenvalues, complex versus real parameters, incompatible boundary
data, and kernels defined only almost everywhere. No case may be discarded merely to fit an API.

## Neighbor and substitution exclusions

- `THM-M-1383` owns the generic ODE boundary-value-problem target and `THM-M-1384` owns the broader
  Sturm--Liouville theory target. Neither can silently become this Green-function root.
- `THM-M-1391` (Prüfer transform) and `THM-M-1393` (Fredholm alternative) are adjacent but distinct
  ODE claims.
- `THM-M-1163` is the separately scheduled PDE Green-function target. `THM-M-1164` and
  `THM-M-1165` separately own symmetry and eigenfunction-representation phrases.
- Green's identities, a fundamental solution on the whole space, heat or probability kernels,
  abstract resolvent existence, spectral expansion, symmetry, positivity, a numerical solver, or a
  convenient Dirichlet special case cannot substitute for the source-selected root.
- A structure field, hypothesis, or axiom containing the desired representation is not a proof.
- The untrusted catalog label and the discovery-only Lean probe carry no source or proof credit.
