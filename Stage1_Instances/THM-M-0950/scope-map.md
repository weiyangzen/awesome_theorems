# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0950`, the label `Polymath项目`, attribution to many
mathematicians, the year 2009, and the gloss `密度Hales-Jewett定理的组合证明`. This identifies the
first Polymath collaboration and its combinatorial/finitary proof program for density
Hales-Jewett. It does not provide a source locator, definitions, quantifiers, hypotheses,
conclusion, quantitative strength, or formal-proof artifact.

The matching publication is D. H. J. Polymath, "A new proof of the density Hales-Jewett theorem,"
*Annals of Mathematics* 175(3), 2012, pp. 1283-1327, DOI
`10.4007/annals.2012.175.3.6`. The inspected publisher PDF is a primary discovery source, not
accepted H0 evidence.

## Candidate roots not selected

- Published Theorem 1.4, qualitative density Hales-Jewett: for positive `k` and real `delta > 0`,
  there is a positive threshold `dhj(k, delta)` such that every subset of `[k]^n` with density at
  least `delta` contains a nondegenerate combinatorial line whenever `n` is at least that threshold.
- Published Theorem 1.5, the proof-specific quantitative strengthening: a tower-height bound of
  order `1 / delta^2` for `k = 3`, followed by an Ackermann-hierarchy comparison for `k >= 4`.
- An exact conjunction of Theorems 1.4 and 1.5 with the source's incorporated definitions and
  quantitative conventions.
- A provenance-sensitive theorem package: Theorem 1.4 together with a reconstructed elementary,
  finitary, Polymath proof graph and its checked composition.

Theorem 1.4 is the likely mathematical conclusion behind the gloss, but selecting it alone would
duplicate the proposition of neighboring `THM-M-0949` and erase the proof-route distinction that
defines this row. Theorem 1.5 is stronger and cannot be silently substituted. No candidate is
canonical at intake.

## Proposition-changing decisions

The statement phase must freeze:

- whether the root is qualitative DHJ, the quantitative result, an exact conjunction, or a
  proposition plus required proof provenance;
- the alphabet `[k]` convention, positive-integer convention, coordinate type, word-space encoding,
  and finite-subset representation;
- the definition of a combinatorial line, including a nonempty wildcard set and the relation
  between wildcard and fixed-coordinate encodings;
- whether density is `|A| / k^n` in `Real`, `NNReal`, or `NNRat`, and the checked transports between
  these representations;
- ordered quantifiers over `k`, `delta`, a threshold, `n`, and `A`, including positivity and
  threshold monotonicity;
- whether the threshold is an existential natural number, a selected function `dhj`, or an explicit
  quantitative bound;
- the meaning of the big-O tower and Ackermann comparisons if Theorem 1.5 is selected; and
- how the target differs from or shares a canonical obligation with `THM-M-0949` without sharing
  target state or proof credit.

## Boundary and degenerate cases

The statement must decide `k = 0`, `k = 1`, `delta <= 0`, `delta > 1`, `n = 0`, the empty and full
subsets, empty coordinate or alphabet types, empty wildcard sets, repeated/fixed coordinates,
strict versus non-strict density inequalities, and whether the conclusion contains the line as a
function range, a `Finset`, or the paper's partition encoding. These cases are not excluded before
a proposition is selected.

## Explicit exclusions

- `THM-M-0949` or its eventual proof evidence imported as if it settled the proof-provenance target.
- Ordinary coloring Hales-Jewett, multidimensional Hales-Jewett, van der Waerden, or Szemeredi in
  place of density Hales-Jewett.
- Only the `k = 3` case, a fixed positive density, a fixed dimension, or a finite computation.
- A structure that assumes the desired line, threshold, density increment, or proof correctness.
- A theorem asserting merely that a paper or proof exists.
- The untrusted `已验证` label, a citation, a blog archive, or the Lean API probe as human or
  machine proof credit.

## Formal boundary

Pinned mathlib provides `Combinatorics.Line`, ordinary coloring Hales-Jewett, finite word-space
cardinality infrastructure, and `Finset.dens`. It does not provide a located density Hales-Jewett
theorem or the Polymath quantitative result. The ordinary theorem is adjacent substrate, not an
anchor for this exact target. The bounded search is intake discovery only, not the later immutable
formal-anchor audit.
