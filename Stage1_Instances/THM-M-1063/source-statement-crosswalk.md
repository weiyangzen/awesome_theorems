# Source-statement crosswalk

## Repository source trail

The repo-local research entry identifies Monroe Donsker, 1951, and only the phrase "functional
convergence of a random walk." Stage0 repeats that phrase and labels the item `已验证`, while the
rev-5.6 manifest explicitly classifies that status as untrusted. These records establish identity
and intake eligibility only; they are not mathematical or machine-proof evidence.

## Candidate human sources

- Monroe D. Donsker, *An Invariance Principle for Certain Probability Limit Theorems*, Memoirs of
  the American Mathematical Society, no. 6 (1951). This is the historical primary-source
  candidate. The exact numbered result, pages, probability-space assumptions, interpolation
  convention, and corrections/errata require direct inspection.
- Patrick Billingsley, *Convergence of Probability Measures*, second edition, Wiley, 1999. The
  treatment of Donsker's theorem is a modern source candidate for the path-space formulation and
  tightness argument. Exact theorem/page, assumptions, and edition errata remain to be inspected.

These are discovery anchors, not `H0` evidence. No theorem number or page is supplied without
inspection, and no equivalence between their formulations is presumed.

## Provisional crosswalk

| Repository/source phrase | Frozen intended component | Required Lean component | Intake status |
|---|---|---|---|
| random walk | partial sums of i.i.d. real increments | probability space, random variables, independence, identical distribution, finite sums | included; encoding open |
| centering and variance | mean zero and variance `sigma^2`, `sigma > 0` | integrability, second moment/variance, positivity, normalization | included; source wording open |
| diffusive rescaling | divide partial sums by `sigma * sqrt(n)` | real coercions, square root, nonzero denominator | included; boundary encoding open |
| functional process | polygonal interpolation at mesh times `k/n` | total continuous path-valued random variable | included; formula open |
| convergence | weak convergence of path laws | pushforward measures and weak convergence on a topological measurable space | included; API open |
| limiting process | standard Brownian motion/Wiener measure | Brownian path law with covariance `min(s,t)` | included; library anchor open |
| path space | `C([0,1], R)` with uniform topology | continuous-map type, topology, Borel measurability | included; representation open |

## Statement and source obligations

Before the statement gate closes, a selected source must be inspected and every material premise,
normalization, interpolation convention, topology, and conclusion mapped to the canonical Lean
target. Any variance-one or cadlag variant needs a checked transport. Before `H0`, a qualified
independent reviewer must verify the chosen edition, pinpoint theorem/page, dependent definitions,
assumption map, and errata status.

## Evidence boundary

No repo-local Lean declaration or external formal proof has been accepted or inspected for this
intake. The anchor-audit phase must search the pinned mathlib revision and credible Lean 4 projects,
recording exact modules, declaration types, immutable revisions, toolchains, axioms, placeholders,
dependency feasibility, and terminal proof-body provenance. This dossier makes no claim that a
functional CLT or Brownian path-law API presently exists in the pinned dependency.
