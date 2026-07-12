# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` identifies Craig Tracy and Harold Widom, gives 1994, and supplies
only the phrase `随机矩阵与KPZ` (random matrices and KPZ). `Docs/Stage0_Blueprint.md` repeats it and
labels the item verified. This is metadata-level discovery input. It gives no ensemble, KPZ model,
normalization, limiting formula, primary proof locator, or machine-check claim.

## Candidate primary sources

- Craig A. Tracy and Harold Widom, "Level-Spacing Distributions and the Airy Kernel,"
  *Communications in Mathematical Physics* 159 (1994), 151-174,
  DOI `10.1007/BF02100489`. This is the candidate source for the beta-2 Airy-kernel distribution
  and random-matrix soft edge.
- Gideon Amir, Ivan Corwin, and Jeremy Quastel, "Probability distribution of the free energy of the
  continuum directed random polymer in 1+1 dimensions," *Communications on Pure and Applied
  Mathematics* 64 (2011), 466-537, DOI `10.1002/cpa.20347`. This is a candidate source for the
  narrow-wedge KPZ one-point formula and its long-time Tracy-Widom asymptotics.

These bibliographic anchors are not `H0`. A source auditor must inspect immutable editions, locate
the exact theorem/equation/pages, reconcile notation and normalizations, identify any needed
finite-`N` GUE edge source or KPZ-to-polymer bridge, and check corrections and errata.

## Crosswalk

| Intake phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| random matrices | source-normalized `N x N` complex Hermitian GUE law | matrix-valued random variable and probability law | GUE selected; constants open |
| largest eigenvalue | top ordered real eigenvalue | Hermitian spectral API and measurable `lambda_max` | included; API open |
| soft-edge limit | centered/scaled CDF or weak convergence as `N -> infinity` | pushforward laws and distributional convergence | included; encoding open |
| KPZ | narrow-wedge solution of the normalized 1+1 dimensional KPZ equation | white noise, renormalized solution, and height random variable | model selected; construction open |
| long-time fluctuation | centered `T^(1/3)` height at the origin as `T -> infinity` | real scaling and distributional convergence | included; constants open |
| common Tracy-Widom law | both branches converge to beta-2 `F_2` | one shared concrete probability law | included; construction open |
| Airy-kernel formula | `F_2(s) = det(I - K_Ai)` on `L2(s,infinity)` | Airy function, integral operator, trace class, determinant | included; formal API open |

## Existing formal boundary

The neighboring dossier `THM-M-1107` is discovery evidence for a GUE-only target, not proof credit
or a substitute for this two-branch claim. The intake found no repo-local theorem artifact for
`THM-M-1562`; a later anchor audit must search pinned mathlib and external Lean projects under a
precommitted discovery protocol. Before `H0`, an independent reviewer must approve every source
premise, conclusion, normalization, bridge, and erratum. Before any machine status above `M4`, an
exact Lean declaration or independently checkable formal candidate must be located and audited.

