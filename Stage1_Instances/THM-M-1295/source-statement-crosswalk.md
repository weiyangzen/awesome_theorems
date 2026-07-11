# Source-statement crosswalk

## Candidate primary-source families

- Michael Struwe, "A global compactness result for elliptic boundary value problems involving
  limiting nonlinearities", *Mathematische Zeitschrift* 187 (1984), 511-517. This is a concrete
  historical candidate for global compactness/bubble decomposition of critical elliptic sequences.
- Pierre-Louis Lions, "The concentration-compactness principle in the calculus of variations. The
  limit case", parts 1 and 2, *Revista Matematica Iberoamericana* 1 (1985). These are candidate
  foundational sources for critical concentration analysis, not evidence that either contains the
  exact intended terminal statement.

The citations are discovery anchors only. Exact theorem numbers/pages, hypotheses, wording, edition
or scan identity, and errata have not been inspected, so they provide no `H0` credit.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "bubble decomposition" | background plus concentrated profiles | typed decomposition equality/asymptotic relation | family included; exact theorem open |
| "critical problem" | scale-invariant variational PDE | equation, domain, energy space, critical exponent | all open |
| "asymptotic" | subsequential convergence and separated parameters | filters/subsequences, scales, centers, topology | open |
| "bubble" | rescaled nontrivial limiting solution | scaling/translation action and solution predicate | open |
| decomposition | remainder and possible energy splitting | finite family, remainder limit, splitting identity | source-dependent |

## Source-fidelity gate

The statement phase must select one source theorem and record stable bibliographic identity,
theorem/page, definitions, every assumption, conclusion, boundary cases, and errata. A second reviewer
must later verify the row-by-row mapping. Searching mathlib before this selection may discover APIs,
but cannot decide which theorem the metadata means and cannot confer statement or proof credit.
