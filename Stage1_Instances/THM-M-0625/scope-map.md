# Scope map

## Preserved theorem family

The intake preserves the metrization family identified by the catalog and Bing's 1951 paper. The
strongest source-supported reading currently located is Bing, Theorem 10: a collectionwise normal
Moore space is metrizable. The paper defines a Moore space as a regular developable space. This is
a scope description only, not a frozen canonical proposition.

The literal catalog phrase "metrizability of collectionwise normal spaces" is insufficient on its
own. Bing's Example F is collectionwise normal but not fully normal; because metric spaces are
paracompact/fully normal in the setting of the paper, the phrase cannot truthfully be expanded to
an unconditional implication from collectionwise normality to metrizability.

## Decisions required at statement freeze

1. Confirm whether the catalog intends Theorem 10, another standard theorem conventionally called
   Bing's metrization theorem, or a different sourced formulation.
2. Freeze the ambient separation convention: Bing allows Whyburn topological spaces or Hausdorff
   spaces, while modern texts may build Hausdorffness or regularity into named classes.
3. Define a development exactly: a countable sequence of open covers whose stars at each point
   refine every neighborhood, including the paper's optional refinement convention.
4. Define Moore space and prove or explicitly source the equivalence with the chosen regular-
   developable encoding.
5. Define a discrete indexed family of subsets. Bing requires pairwise disjoint closures and the
   union of every subfamily of closures to be closed; modern definitions may instead use locally
   finite or neighborhood-discrete formulations, which need checked equivalences.
6. Define collectionwise normality with all domain/open-set, cover, disjointness, and
   no-cross-intersection clauses, and settle whether the input family consists of arbitrary sets
   or closed sets.
7. Decide whether the conclusion is `TopologicalSpace.MetrizableSpace X`, existence of a compatible
   `MetricSpace`, or an explicitly constructed metric, and provide checked transports.
8. Freeze universes, index types, all ordered binders and typeclass hypotheses, foundation/choice
   policy, minimal imports, and the expression/environment fingerprints.

## Boundary and degenerate cases

The statement phase must inspect empty and singleton spaces; empty and singleton indexed families;
empty members of a family; empty covers; repetitions in an indexed family; unused indices; the
empty/singleton development; discrete topologies; non-Hausdorff or non-`T1` interpretations; and
whether countability means an explicit `Nat` sequence or a merely countable family.

## Excluded substitutions

- Collectionwise normality alone implying metrizability.
- Bing Theorem 14, which proves collectionwise normality implies ordinary normality.
- Bing Theorems 3, 4, 7, or 8 with perfect/strong screenability or normal screenable Moore-space
  hypotheses, unless a checked equivalence to the selected root is supplied.
- Urysohn metrization (`T3` plus second countability), Nagata-Smirnov metrization, or Smirnov's
  locally finite basis theorem.
- Ordinary `NormalSpace`, `CompletelyNormalSpace`, pairwise-disjoint families, or a stored metric as
  substitutes for collectionwise normality plus developability.
- A structure field or hypothesis that directly assumes the requested metric or theorem.
- The catalog's `已验证` label, a `#check`, or an adjacent API as proof credit.

## Neighbor boundaries

`THM-M-0623` owns Urysohn metrization and `THM-M-0624` Nagata-Smirnov metrization. Those results may
later become explicit dependencies but cannot replace this target. `THM-M-0621` and `THM-M-0622`
own the Urysohn lemma and Tietze extension theorem; ordinary normality infrastructure from those
families is likewise not the collectionwise-normal Moore-space result.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks
regularity, normal separation, indexed pairwise disjointness, and (pseudo)metrizability. A bounded
exact-topic search found no Bing, collectionwise-normal, screenability, developability, or
Moore-space declaration. This is intake discovery evidence, not an exhaustive anchor audit and not
a global nonexistence proof.
