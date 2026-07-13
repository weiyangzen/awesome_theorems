# Scope map

## Received Scope

The repository fixes the title `巨分量定理`, the gloss `随机图中巨分量的出现`, the attribution
Erdos/Renyi, the year 1960, and the untrusted label `已验证`. This identifies the classical
random-graph giant-component family, not a truth-valued proposition.

An eventual statement may concern a component whose size is macroscopic relative to the vertex
count only after a reviewed source fixes all of the following:

- the probability model: uniform fixed-edge `G(n,m)`, independent-edge `G(n,p)`, or a coupled
  random graph process;
- finite labelled simple undirected graphs and the precise vertex carrier;
- the scaling of `m` or `p`, including every fixed or varying parameter and its binder order;
- the conclusion strength: existence, uniqueness, asymptotic size/density, bounds on the second
  largest component, or a joint collection of these claims;
- whether the root is supercritical only, includes a subcritical contrast, or treats a critical
  window;
- the probability mode: positive probability, convergence in probability, probability tending to
  one, an explicit limiting distribution, or a process stopping-time statement;
- the precise meaning of "giant," including constants, error terms, rounding, and tie conventions;
- boundary cases such as the critical parameter, small `n`, `p = 0` and `p = 1`, empty carriers,
  and strict versus nonstrict inequalities.

These are candidate scope components, not a selected canonical claim.

## Material Ambiguities

1. Historical Erdos-Renyi work uses a uniform fixed-edge graph process, whereas mathlib's
   `SimpleGraph.binomialRandom` implements the independent-edge law and explicitly distinguishes
   the two models.
2. Supercritical existence alone is weaker than uniqueness plus a limiting component density and
   control of every remaining component.
3. A paired theorem contrasting `c < 1` and `c > 1` is not interchangeable with the appearance
   half alone.
4. The critical case or critical window has different scales and conclusions from either fixed
   off-critical regime.
5. "Appearance" does not choose a finite probability bound, a with-high-probability limit, a
   convergence statement, or a process hitting-time formulation.
6. Component size may be stated through the largest component, an existential component witness,
   or a density equation. These need explicit transports rather than textual identification.

## Explicit Exclusions

- The general Erdos-Renyi random-graph model (`THM-M-0848`), phase-transition target
  (`THM-M-0849`), connectivity threshold (`THM-M-0851`), or Hamilton-cycle threshold
  (`THM-M-0852`), each of which has its own catalog identity.
- The near-duplicate phase-transition and giant-component records `THM-M-1113` and
  `THM-M-1114`; their artifacts and evidence cannot be inherited or used to collapse target IDs.
- A deterministic fact saying that a particular graph has a large connected component.
- A branching-process survival theorem without checked transport to the selected random-graph
  proposition.
- A weaker unbounded-size, positive-probability, expected-size, or nonempty-component conclusion
  substituted for a linear-size high-probability claim.
- The definition of `G(n,p)` or connected components by itself.
- A finite computation, Monte Carlo observation, asymptotic heuristic, or unchecked certificate.
- A structure, hypothesis, axiom, or opaque predicate that assumes the desired conclusion.
- The catalog label `已验证` as human-source or machine-proof evidence.

## Formal Boundary

No canonical Lean expression, minimal import set, expression hash, or environment fingerprint is
frozen at intake. The two probed mathlib modules provide an independent-edge measure and finite
connected-component vocabulary, but do not select the probability model or asymptotic theorem.
Measurability of a selected component-size event, asymptotic filters, source-model transports,
statement equivalences, and mutation tests belong to the dependent statement phase after one
proposition-level source is selected.

At minimum, later mutations must remove the regime hypothesis, change the probability law or edge
scale, move the probability limit across a parameter quantifier, weaken linear size to
nonemptiness, drop uniqueness where present, and exercise the critical boundary. Non-equivalent
mutations must receive no statement or proof credit.
