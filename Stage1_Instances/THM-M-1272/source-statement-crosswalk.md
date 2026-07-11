# Source-statement crosswalk

## Candidate primary sources

- Thomas Bartsch, *Infinitely many solutions of a symmetric Dirichlet problem*, Nonlinear Analysis
  20 (1993), 1205-1216. This is an original-era source candidate for the Fountain construction;
  exact theorem numbering, wording, assumptions, and accessible errata have not yet been inspected.
- Michel Willem, *Minimax Theorems*, Progress in Nonlinear Differential Equations and Their
  Applications 24, Birkhauser (1996), the Fountain theorem in the symmetric minimax chapter. This
  is a standard exposition candidate, but exact theorem/page and edition wording remain open.

These are discovery anchors, not `H0` evidence. The statement phase must inspect a stable copy and
select one exact classical variant.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Fountain theorem" | symmetric minimax multiplicity theorem | exact source theorem wrapper | included, variant open |
| even `C1` functional | `Phi (-u) = Phi u` with Frechet differentiability | `ContDiff`/derivative API and evenness | included, exact regularity open |
| finite/tail splitting | increasing finite-dimensional directions and complementary tails | concrete subspaces, closure, decomposition | included, object model open |
| Fountain geometry | two radius families and opposing energy bounds | quantified sphere/ball inequalities | included, inequality conventions open |
| compactness | convergence of relevant Palais-Smale sequences | sequence, derivative residual, subsequence convergence | included, global/levelwise open |
| many critical points | critical values escape to positive infinity | derivative-zero witnesses and limit/unboundedness | included, conclusion form open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_165.lean` is discovery evidence for Frechet
derivatives, critical values, Palais-Smale sequence shapes, and Hilbert-space APIs. Its
`FountainGeometry` and `FountainHypotheses` contain proposition-valued assumptions for the hard
geometry, compactness, and minimax construction. Consequently its wrappers do not establish the
source theorem and receive no proof credit. Its repo-local anchor observations must be repeated at
the pinned revision during anchor audit.

Before `H0`, an independent reviewer must verify the selected source copy, theorem/page, definitions,
all hypotheses, variant identity, and errata, then approve the row-by-row source-to-Lean mapping.
