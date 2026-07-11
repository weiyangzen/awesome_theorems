# Source-statement crosswalk

## Repository source trail

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` attribute the item to Richard
Hamilton, date it to 1988, and give only the phrase "parabolic method for the Yamabe problem."
Neither record supplies a publication, theorem number, page, hypotheses, or a mathematical
statement. The `verified` source label is consequently not H evidence.

## Candidate primary sources

- Richard S. Hamilton, *Lectures on geometric flows* (1989 lecture notes). This is a historical
  candidate for the introduction and formulation of Yamabe flow. A stable edition, page-level
  statement, and whether it contains the intended terminal theorem have not been inspected.
- Bennett Chow, "The Yamabe flow on locally conformally flat manifolds with positive Ricci
  curvature," *Communications on Pure and Applied Mathematics* 45 (1992), 1003-1014. This is a
  primary convergence-result candidate, but the exact theorem wording, dimension and curvature
  assumptions, normalization, pages, and errata remain to be checked from the paper.

These are discovery anchors only, not `H0` evidence. Secondary surveys may help disambiguate the
historical phrase but cannot replace an inspected primary theorem and independent crosswalk review.

## Provisional crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Yamabe flow" | conformal metric evolution driven by scalar curvature | time-dependent Riemannian metric and evolution equation | included; conventions open |
| "parabolic method" | scalar quasilinear parabolic PDE for a conformal factor | positive smooth factor, Laplacian and solution notion | included; checked transport open |
| "Yamabe problem" | production of a constant-scalar-curvature conformal metric | scalar curvature, conformal equivalence and terminal limit | intended conclusion; exact theorem open |
| normalized flow | subtraction of average scalar curvature and fixed volume | volume form, integral, average and preservation | likely included; source decision open |
| convergence | global solution converges to a limiting metric | global time domain and specified convergence topology | candidate claim; hypotheses open |

## H0 requirements

An independent reviewer must verify the selected edition, theorem number and page, definitions,
all assumptions, normalization and Laplacian conventions, convergence topology, errata, and every
row of the source-to-Lean mapping. Until then the human claim remains `H3`, and no exact formal
statement or proof receives credit.
