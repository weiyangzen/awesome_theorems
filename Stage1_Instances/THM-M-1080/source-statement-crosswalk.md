# Source-statement crosswalk

## Candidate sources

- Kazuoki Azuma, "Weighted sums of certain dependent random variables," *Tohoku Mathematical
  Journal*, Second Series 19 (1967), 357-367, DOI `10.2748/tmj/1178243286`. This is the historical
  primary-paper candidate. Its exact theorem number, original hypotheses, notation, page span, and
  correction history require direct inspection in the statement phase.
- Colin McDiarmid, "On the method of bounded differences," in *Surveys in Combinatorics 1989*,
  London Mathematical Society Lecture Note Series 141, Cambridge University Press, 1989,
  pp. 148-188. This is a later bounded-differences comparison source, not authority for attributing
  an exact statement to Azuma; its relation to the selected martingale formulation must be audited.

These bibliographic records are discovery anchors only. Intake does not promote the untrusted
repository label to `H0` or infer the primary paper's exact proposition from modern textbook usage.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Azuma inequality" | exponential concentration for bounded martingale increments | one canonical finite-time tail declaration | included; exact source variant open |
| martingale | adapted integrable real process with conditional expectation law | probability space, filtration, adaptedness, integrability, conditional expectation | included; API open |
| bounded increments | deterministic `c_k` controls `|X_k-X_{k-1}|` almost surely | finite family of nonnegative bounds and a.e. inequalities | included; quantifier encoding open |
| concentration | upper-tail exponential estimate | measurable event, probability, finite sum, real exponential | included; coercions open |
| exponent constant | `1 / (2 * sum c_k^2)` for symmetric absolute bounds | checked arithmetic normalization | intended; must be source-checked |
| lower tail | apply upper tail to the negated martingale | checked negation transport | derived, open |
| two-sided tail | union of upper and lower events, factor `2` | checked event decomposition and union bound | derived, open |

## Variant firewall

The source audit must not silently conflate the symmetric increment bound with the stronger
predictable interval form. If increments lie in intervals of width `b_k-a_k`, the usual Hoeffding
normalization has a different presentation; conversion to `|increment| <= c_k` changes the width
to `2*c_k` and must reproduce the intended exponent. Maximal, conditional-variance, Banach-valued,
and bounded-difference-function variants are candidates or descendants, not automatically exact
matches.

## Evidence boundary

No repo-local or upstream Lean theorem has been inspected or accepted in this intake. Before `H0`,
an independent reviewer must inspect a fixed primary-source copy, record exact theorem/page,
assumptions, normalization, and errata, and approve a row-by-row source-to-Lean map. Before any
`M0-*` status, the anchor audit must record the exact module, declaration type, immutable revision,
toolchain, axioms, placeholders, transitive provenance, and proof-body location.
