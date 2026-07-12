# Source-statement crosswalk

## Repository record and source genealogy

The repository inventory supplies John Cardy, 1992, and the gloss "crossing probability for
percolation". Its `已验证` field is untrusted under rev-5.6 and supplies neither a formula nor a
rigorous theorem locator.

The original formula candidate is John L. Cardy, *Critical percolation in finite geometries*,
**Journal of Physics A: Mathematical and General** 25 (1992), L201-L206,
DOI `10.1088/0305-4470/25/4/009`. It is the physics derivation/prediction that gives the entry its
name; intake does not treat it as the later rigorous convergence proof.

The principal rigorous-source candidate is Stanislav Smirnov, *Critical percolation in the plane:
conformal invariance, Cardy's formula, scaling limits*, **Comptes Rendus de l'Academie des Sciences,
Serie I** 333 (2001), 239-244, DOI `10.1016/S0764-4442(01)01991-7`. A fuller source candidate is
Smirnov, *Critical percolation in the plane: conformal invariance, Cardy's formula, scaling limits*,
**C. R. Physique** 8 (2007), 243-253, DOI `10.1016/j.crhy.2007.04.004`. These are discovery
anchors only: this intake has not accepted an immutable edition, theorem/page pinpoint, errata
review, or independent source review.

## Crosswalk

| Claim component | Source role | Required Lean component | Intake status |
|---|---|---|---|
| Critical percolation crossing | Cardy 1992 derives the predicted formula; Smirnov supplies the rigorous triangular-lattice theorem candidate | mesh-indexed probability spaces and an explicitly measurable crossing event | family identified; exact definitions open |
| Simply connected marked domain | rigorous formulation uses a domain with ordered boundary data and discrete approximations | planar domain, four boundary prime ends/points, approximation relation | source assumptions and Lean representation open |
| Scaling limit | discrete crossing probabilities tend to a continuum value | sequence/filter limit in `Real` with exact quantifier order | convergence mode open |
| Conformal invariance | limit depends only on normalized conformal data | conformal equivalence/map plus checked invariance statement | exact source strength open |
| Cardy function | cross-ratio hypergeometric form or triangle-coordinate form | explicit real/special-function expression and normalization | candidate encodings only; no checked transport |
| Model scope | commonly rigorous for critical site percolation on the triangular lattice | lattice, site states, independence, `p = 1/2`, boundary convention | must be frozen from selected theorem |

## Human and machine boundary

The original prediction, the rigorous theorem, and convenient modern restatements must remain
separate provenance nodes. Before `H0`, an independent reviewer must inspect immutable source
copies; select an exact theorem/displayed statement and pinpoint pages; map every model, domain,
boundary, convergence, and normalization assumption; check corrections and errata; and approve the
crosswalk. In particular, the later proof must not be attributed to Cardy's paper merely because
the limiting function bears his name.

This intake does not perform the dependent exhaustive mathlib/external Lean audit. Before statement
credit, the selected rigorous proposition must map to one elaborated Lean target without broadening
the model, weakening equality to an assumed limit, or replacing the explicit formula by an opaque
definition. Before machine completion, a terminal proof body must be integrated and checked under
the pinned environment; a citation or theorem name alone receives no proof credit.
