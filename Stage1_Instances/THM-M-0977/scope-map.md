# Scope map

## Preserved catalog family

The intake preserves only what the catalog actually fixes: a result called a Chernoff bound,
attributed to Herman Chernoff and concerning tail probabilities for a sum of independent random
variables. This establishes a probability-inequality family, not a formula.

## Candidate roots, not credited

Materially different results commonly fit the catalog gloss:

1. An upper-tail exponential-moment inequality for a finite independent family at a fixed
   nonnegative tilt, optionally factored into individual MGFs or written with CGFs.
2. The corresponding lower-tail inequality at a nonpositive tilt.
3. An infimum over admissible tilts, or an equivalent convex-dual/rate-function bound.
4. Additive or multiplicative Chernoff bounds for sums of independent Bernoulli variables, with
   deviation expressed relative to the mean.
5. Binomial or Poisson-binomial specializations with explicit entropy or quadratic exponents.
6. An asymptotic large-deviation statement for independent identically distributed summands.

The intake does not choose among them. In particular, existence of a convenient pinned MGF theorem
does not make the general fixed-tilt upper bound the catalog's canonical statement.

## Proposition-changing decisions

Before statement elaboration, an admitted source and accountable duplicate-target review must fix:

- whether `THM-M-0977` and `THM-M-0993` are duplicates, intentionally distinct variants, or need a
  master-owned allocation decision;
- upper, lower, or two-sided tail, and strict versus closed tail events;
- arbitrary real summands, bounded summands, Bernoulli indicators, or a binomial law;
- finite index type/finset, a natural initial segment, or an asymptotic sequence;
- probability measure versus arbitrary finite measure and real versus extended-real probability;
- independence notion, measurability, exponential integrability, and identical-distribution or
  boundedness assumptions;
- threshold, tilt, expectation, deviation, and parameter domains, including positivity and signs;
- fixed-tilt MGF, CGF, optimized tilt, entropy/rate, additive, or multiplicative conclusion;
- empty family, zero tilt, zero expectation, endpoint deviation, impossible event, and infinite
  moment behavior;
- all ordered binders, universes, coercions, sum/product conventions, and constants.

Until these choices are source-backed and independently reviewed, ordered binders, hypotheses,
conclusion, alternate encodings, excluded degenerate cases, minimal imports, expression hash,
environment fingerprint, transports, and statement mutations remain deliberately open.

## Explicit exclusions

- Markov's inequality alone or an unfactored single-variable exponential bound presented as the
  independent-sum root without a checked relationship.
- Hoeffding, Bernstein, Bennett, Azuma-Hoeffding, McDiarmid, or a sub-Gaussian estimate substituted
  for a source-selected Chernoff statement.
- A Bernoulli/binomial corollary substituted for a general MGF statement, or conversely.
- A fixed finite numerical example, simulation, floating-point estimate, or unchecked optimizer.
- A proposition, structure, or hypothesis which stores the desired tail bound.
- The catalog's untrusted status, a theorem name or URL, pinned candidate APIs, `THM-M-0993`
  artifacts, or legacy `S1-M-273` status used as proof credit.

## Neighbor and duplicate boundary

`THM-M-0993` has the translated title `切尔诺夫界` and the identical author, year, gloss,
importance, and untrusted status. Its category and historical scheduling differ, but those facts do
not establish a different mathematical proposition. `THM-M-0975`, `THM-M-0978`, `THM-M-0979`, and
`THM-M-0980` are neighboring concentration inequalities and remain independently owned targets.

## Pinned Lean boundary

Pinned `Mathlib.Probability.Moments.Basic` contains exact-topic upper/lower MGF and CGF bounds plus
independent finite-sum integrability and factorization. Repo-local `S1_M_273.lean` and the
`THM-M-0993` dossier contain wrappers around those declarations. Intake records them as candidate
surfaces only. Exact source mapping, declaration/body provenance, trust closure, and all status
credit belong to later phases and to this target's own accepted receipts.
