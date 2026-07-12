# Scope map

## Repository claim included at intake

- Finite labelled simple undirected graphs on a vertex set of cardinality `n`.
- The classical fixed-edge construction `G(n, m)`: uniform choice among graphs with exactly `m`
  edges.
- The classical independent-edge construction `G(n, p)`: every unordered pair of distinct
  vertices is included as an edge independently with probability `p`.
- Probability-law properties may become a theorem target only after a primary source is selected.

These bullets delimit the named model family. They are not an assertion that both variants must be
conjoined into the eventual theorem.

## Decisions required at statement freeze

The next phase must choose a unique primary theorem and freeze: `G(n, m)` or `G(n, p)`; labelled or
unlabelled graphs; the concrete vertex type and its decidable equality; loop and multiple-edge
exclusion; the edge sample space; the probability codomain; the ranges `0 <= m <= n choose 2` and
`0 <= p <= 1`; independence and measurability encodings; whether a probability mass formula,
uniformity result, coupling, asymptotic property, or another theorem is the conclusion; and the
ordered limiting regime if the result is asymptotic.

Boundary cases requiring explicit treatment include `n = 0`, `n = 1`, `m = 0`, maximal `m`,
`p = 0`, and `p = 1`. The source may make some cases vacuous or exclude them, but the formal target
must not decide this implicitly.

## Explicit exclusions

- The random-graph phase transition, giant-component, connectivity-threshold, and Hamiltonicity
  theorems, which are separately named repository targets.
- The Erdos-Renyi second lemma in probability theory, which is unrelated to random graph models.
- A deterministic existence theorem obtained by discarding the probability law.
- A structure or hypothesis that contains the desired distributional conclusion as data.
- An executable sampler, numerical experiment, or repository label `已验证` as proof evidence.

No Lean expression is frozen at intake. A later expression must expose a concrete finite graph
sample space and probability law, then map row by row to the selected source statement.
