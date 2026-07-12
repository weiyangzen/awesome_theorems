# Source-statement crosswalk

## Primary sources identified

- B. Gross and D. Zagier, "Heegner points and derivatives of L-series,"
  *Inventiones Mathematicae* 84 (1986), pp. 225-320,
  DOI `10.1007/BF01388809`.
- V. A. Kolyvagin, "Euler systems," in *The Grothendieck Festschrift*,
  Volume II, Progress in Mathematics 87, Birkhauser (1990), pp. 435-483,
  DOI `10.1007/978-0-8176-4575-5_11`.

These are discovery-level bibliographic anchors, not immutable evidence
receipts and not `H0`. The anchor-audit phase must obtain fixed copies, hash
them, locate exact result numbers and pages, map every assumption, check
corrections and translation issues, and independently review the composite
argument. In particular, the modern all-elliptic-curves-over-`Q` statement
also requires an audited modularity/generalization genealogy rather than a
silent projection of the original papers' hypotheses.

## Crosswalk

| Claim component | Source-side anchor | Frozen target meaning | Intake assessment |
|---|---|---|---|
| central derivative and Heegner height | Gross-Zagier (1986) | a bridge between a simple central zero and non-torsion of a suitable Heegner point | exact normalization, constants, hypotheses, theorem locator, and both logical directions require audit |
| Euler-system descent | Kolyvagin (1990) | control of Mordell-Weil/Selmer rank and finiteness of Sha from a non-torsion Heegner point | exact curve, field, prime, reduction, and Sha conclusions require audit |
| analytic rank zero branch | Kolyvagin-family descent together with the relevant nonvanishing input | `ord_(s=1) L(E,s) = 0` implies rank zero and finite Sha | source genealogy and whether additional cited work is required remain open |
| analytic rank one branch | Gross-Zagier plus Kolyvagin | `ord_(s=1) L(E,s) = 1` implies rank one and finite Sha | composite premise-by-premise mapping remains open |
| every elliptic curve over `Q` | later modularity theorem and any auxiliary quadratic-field/twisting reductions | remove a modularity-only or Heegner-hypothesis-only restriction without weakening the root | exact primary sources and checked transports remain open |
| BSD content | comparison with the BSD conjecture | rank equality and Sha finiteness only when analytic rank is at most one | does not include the leading-coefficient formula |

## Lean crosswalk

No exact Lean declaration is credited at intake. Repo-local files concerning
the Gross-Zagier formula (`S1_M_044`), Kolyvagin Euler systems (`S1_M_090`),
and Rubin-Kolyvagin BSD consequences (`S1_M_091`) are discovery inputs only.
They explicitly describe missing APIs or abstract statement boundaries and do
not supply an exact terminal proof of this target. The statement phase must
select native definitions and elaborate the canonical proposition before any
machine candidate can be measured against it.

## Fidelity risks

The label "Kolyvagin-Gross-Zagier theorem" is used for several nearby
statements. A Heegner-point conditional, a modular-elliptic-curve statement,
the analytic-rank-one branch, and the combined analytic-rank-at-most-one BSD
consequence are not interchangeable. This dossier chooses the last because
the repository metadata calls the target an elliptic-curve BSD partial
result. Any source evidence for a narrower version must be connected by
checked hypotheses and transports rather than substituted for the root.
