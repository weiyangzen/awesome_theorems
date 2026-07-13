# THM-M-1465 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `有限差分法`
(finite difference method). The repository supplies only the gloss `偏微分方程的差分离散`
(finite-difference discretization of partial differential equations), attributes it to many
mathematicians in the twentieth century, and labels it `已验证`. A method-family name and purpose
are not a truth-valued proposition with ordered binders, hypotheses, and a conclusion. The
verified label is untrusted metadata and supplies neither source nor proof credit.

For PDEs, finite differences can mean an elliptic boundary-value discretization, a semidiscrete or
fully discrete parabolic method, a hyperbolic scheme, a local truncation-error theorem, discrete
solvability, stability, convergence, or a normed error estimate. These alternatives require
different equations, domains, initial and boundary data, grids, stencils, regularity assumptions,
step restrictions, norms, and conclusions. The catalog selects none of them. Choosing a familiar
five-point Poisson stencil or heat-equation convergence theorem would invent proposition-changing
mathematics.

Randall J. LeVeque's 2007 SIAM book *Finite Difference Methods for Ordinary and Partial
Differential Equations* was inspected only as a modern source-family lead. Its contents separate
elliptic, parabolic, and hyperbolic schemes and their accuracy, stability, convergence, CFL, and
von Neumann results; its errata correct material formulas. The catalog neither cites the book nor
selects a theorem or page. No immutable pinpoint proposition, assumption/proof/errata crosswalk,
or independent review has been admitted, so this lead supplies no `H0` credit.

Pinned mathlib supplies algebraic forward differences, a continuous Laplacian, and a Taylor
remainder theorem. `IntakeProbe.lean` authenticates those adjacent interfaces only. It does not
define a grid or discrete PDE scheme and supplies no canonical statement or proof credit.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received method gloss as not yet a
stable proposition; it does not refute correctly stated finite-difference results. All six
downstream phases remain open. No H0, M0, R0, exact mathematical or Lean statement, accepted proof
state, audit completion, theorem completion, accepted receipt, or master acceptance is claimed.
