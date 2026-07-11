# Source-statement crosswalk

## Candidate primary sources

- Werner Heisenberg, "Ueber den anschaulichen Inhalt der quantentheoretischen Kinematik und
  Mechanik," *Zeitschrift fuer Physik* 43 (1927), 172-198, DOI
  `10.1007/BF01397280`. This is the historical principle source; the exact inequality, conventions,
  and relevant pages have not yet been inspected from a stable scan.
- H. P. Robertson, "The Uncertainty Principle," *Physical Review* 34 (1929), 163-164, DOI
  `10.1103/PhysRev.34.163`. This is the candidate source for the general commutator form; exact
  wording, hypotheses, and page-level crosswalk remain to be inspected.

These bibliographic records are discovery anchors, not `H0` evidence. The statement phase must
inspect stable copies and check corrections or errata rather than reconstruct a theorem from its
modern name.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "conjugate variables' uncertainty" | position-momentum standard deviations | variance and nonnegative square root | included; convention open |
| observable | self-adjoint, generally unbounded operator | closed/densely defined operator model and domains | included; API open |
| commutator | `AB - BA` on a common product domain | typed operator products and common-domain proof | included; exact domain open |
| normalized state | unit vector in all required domains | `psi` plus norm and membership hypotheses | included |
| uncertainty lower bound | Robertson inequality | exact real inequality with complex expectation norm | included; orientation open |
| canonical pair | `[Q,P] = i hbar I` | checked CCR hypothesis and specialization | included; scope open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_192.lean` supplies a useful historical candidate:
it defines observables as complex linear maps and states Robertson and CCR-specialized shapes. That
bounded/everywhere-defined model does not by itself match physical position and momentum. Its exact
types, proof bodies, imports, axioms, and relationship to the selected source must be audited later;
this intake grants it no closure credit.

Before `H0`, an independent reviewer must verify the chosen source edition, page/theorem location,
notation, every analytic and domain assumption, errata, and the row-by-row source-to-Lean mapping.
