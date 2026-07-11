# Source-statement crosswalk

## Candidate sources

- A. W. van der Vaart, *Asymptotic Statistics*, Cambridge University Press (1998), Chapter 3,
  Theorem 3.1, is a modern standard-source candidate for a finite-dimensional delta method.
- Aad van der Vaart and Jon Wellner, *Weak Convergence and Empirical Processes*, Springer (1996),
  the functional delta-method section, is a candidate only if the broader Hadamard-differentiable
  variant is selected.

These bibliographic leads are discovery anchors, not `H0` evidence and not claims of historical
primacy. The next phase must inspect a stable edition, reproduce its exact statement, check errata,
and either identify a primary mathematical source or explicitly classify the accepted modern
source boundary. No theorem wording or assumptions are inferred merely from the name.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "Delta method" | differentiable mapping transfers a scaled weak limit | derivative plus mapping theorem bridge | included; variant open |
| "random variable transformation" | `g(X_n)` centered at `g(theta)` | measurable composition and subtraction | included; spaces open |
| "asymptotic distribution" | convergence in distribution after scaling | laws or bounded-continuous test formulation | included; encoding open |
| first-order approximation | derivative applied to limit `Z` | continuous linear map evaluated at `Z` | included; derivative notion open |
| scaling | common `r_n` on input and output deviations | scalar action and sequence hypotheses | included; assumptions open |

## Repository evidence boundary

The manifest and Stage1 legacy prose supply only the Chinese name, the broad phrase "asymptotic
distribution of transformations of random variables", and an untrusted source-status label. They
contain no exact source, formal statement, or proof artifact. A later mathlib/external search must
record exact declarations and immutable revisions; intake performs no anchor or proof credit.

Before `H0`, an independent reviewer must verify the chosen theorem/page, definitions, all
hypotheses, dimensional conventions, derivative notion, boundary cases, and errata, and approve a
row-by-row mapping to the canonical Lean statement.
