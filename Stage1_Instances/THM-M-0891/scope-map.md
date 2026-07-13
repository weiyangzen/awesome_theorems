# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0891`, the name "Wilf theorem", Herbert Wilf, the year 1967,
and the gloss `色数的谱下界`. Intake preserves that spectral graph-coloring family without
silently correcting the wording or inheriting the untrusted `已验证` status.

The strongest statement lead currently available is the familiar finite simple-graph inequality

```text
chi(G) <= 1 + lambda_1(A(G)),
```

equivalently `lambda_1(A(G)) >= chi(G) - 1`. Here `A(G)` is the real adjacency matrix and
`lambda_1` is its largest eigenvalue. A modern source also reports equality exactly for complete
graphs or odd cycles. These are candidate components, not a selected canonical claim.

## Direction ambiguity

The literal Chinese gloss says "a spectral lower bound for the chromatic number." The candidate
Wilf inequality is instead:

- an upper bound on the chromatic number in terms of the largest adjacency eigenvalue; and
- after algebraic rearrangement, a lower bound on the largest adjacency eigenvalue in terms of the
  chromatic number.

Those readings are not interchangeable with a spectral lower bound *on* the chromatic number such
as a least-eigenvalue or Hoffman-type inequality. The statement phase must admit primary text and
decide the intended orientation rather than replacing the catalog phrase by a familiar formula.

## Decisions required at statement freeze

1. Preserve a lawful immutable primary edition, identify the exact statement/proof locator and
   incorporated definitions, audit corrections or errata, and obtain independent source review.
2. Decide whether the canonical root is only the inequality, the inequality plus equality
   characterization, an equivalent spectral-radius lower bound, or another primary result.
3. Fix finite undirected simple graphs versus another graph model, the vertex carrier, `Fintype`
   and decidable-adjacency data, and whether connectedness or nonemptiness is assumed.
4. Fix the chromatic-number encoding: mathlib's `ENat`-valued `G.chromaticNumber`, a natural
   minimum obtained from finite colorability, or a universally quantified `G.Colorable k` form.
5. Fix the real adjacency matrix and largest-eigenvalue encoding, including the empty `Fin 0`
   boundary, eigenvalue ordering/indexing, coercions, and proof that the selected entry is maximal.
6. If equality is included, define complete graphs and odd cycles precisely, decide whether the
   result is componentwise or connected, and freeze graph-isomorphism and cycle-length conventions.
7. Freeze ordered binders, all hypotheses, the exact conclusion, universes, foundation/TCB/
   computation profiles, minimal imports, checked alternate forms, and the four mutation classes.

## Degenerate and boundary cases

Source and statement review must explicitly dispose of empty and singleton vertex types, edgeless
graphs, disconnected graphs, isolated vertices, complete graphs of orders zero through two,
bipartite graphs, even versus odd cycles, and graphs with multiple components attaining the same
largest eigenvalue. The natural chromatic number and the real eigenvalue cannot be compared without
an explicit coercion and finite-colorability boundary. An eigenvalue indexed by an empty type is
not available, so `Nonempty V`, a separate empty case, or a different spectral definition is a
material statement choice.

## Substitution exclusions

- The Hoffman lower bound involving the least adjacency eigenvalue is distinct target
  `THM-M-0890`; it cannot resolve the catalog's directional ambiguity for this target.
- A maximum-degree coloring bound, Brooks theorem, clique bound, Laplacian bound, signless
  Laplacian bound, or spectral-radius estimate without chromatic closure is not Wilf's target.
- The equality classification alone is not the inequality, and the inequality alone does not
  establish the equality cases unless the canonical root omits them.
- A theorem restricted to regular, connected, nonempty, or `Fin n` graphs is not credited for a
  more general source claim without a checked transport.
- Generic `Colorable`, `chromaticNumber`, adjacency-matrix, Hermitian, or eigenvalue APIs are
  representation substrate, not a proof.
- Numerical spectra, assumed colorings, unchecked computations, the catalog status, placeholders,
  axioms, or fake certificates carry no proof credit.

No canonical Lean target, expression fingerprint, alternate-encoding witness, mutation suite,
discovery protocol, obligation registry, or proof body is frozen at intake.
