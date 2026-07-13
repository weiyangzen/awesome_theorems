# THM-M-0910 scope map

## Received claim

The repository fixes target `THM-M-0910`, the title `Caucal定理`, attribution to Didier Caucal,
the year 1996, and the gloss `图的可判定性`. It does not identify a graph family, logic,
presentation, decision problem, quantifier order, hypotheses, or conclusion. Intake preserves this
identity and ambiguity rather than manufacturing an exact root.

## Matching source family, not canonical scope

Didier Caucal's *On Infinite Transition Graphs Having a Decidable Monadic Theory* is a strong match
for author, year, and topic. Its abstract says that a family of graphs has monadic theory linearly
reducible to the theory `S2S` of complete deterministic binary trees. The full text develops more
than one candidate theorem. Among them are:

- Proposition 2.5: a conditional preservation theorem for rational inverse substitution followed
  by rational restriction;
- Corollary 2.8: every graph in the paper's class `REC_Rat` has decidable monadic theory;
- Corollary 3.7: a presentation-level decidability result for rationally restricted right closures
  of recognizable labelled word graphs;
- Corollaries 3.8 and 3.14: consequences for pushdown transition graphs and regular graphs; and
- structural closure, completeness-of-representatives, containment, and Boolean-algebra results.

The repository does not select any one of these. They differ in binders, assumptions, graph
classes, conclusions, and proof dependencies. They remain source-family candidates only.

## Proposition-changing decisions

An admitted source and independent review must freeze all of the following before statement work:

1. The exact numbered result and edition: ICALP 1996 or the later same-title 2003 journal publication, including
   how changes between them affect definitions and theorem numbering.
2. Directed labelled graphs versus simple graphs, vertex and label carriers, roots, finite degree,
   completeness/determinism, and equality up to graph isomorphism.
3. The graph class: `REC_Rat`, a prefix-recognizable presentation, recognizable right closure,
   pushdown transition graphs, regular/equational graphs, or another source-defined family.
4. The exact monadic second-order signature, including first-order vertex variables, vertex-set
   variables, labelled-edge relations, sentences, satisfaction, and the theory `MTh(G)`.
5. What "decidable" quantifies over and consumes: an effective presentation of `G`, a sentence
   encoding, a uniform decider for a class, or a per-graph decidability predicate.
6. Whether the conclusion is a linear reduction to `S2S`, preservation under transformations,
   decidability itself, an effective construction, or a combination of these.
7. Encodings of rational languages/substitutions/restrictions, accessibility, prefix rewriting,
   inverse edges, transitive closure, and all required effectiveness hypotheses.
8. Ordered binders, universes, finiteness/decidability instances, classical or computability
   assumptions, and the exact dependency on Rabin's theorem.

## Boundary and degenerate cases

No case is excluded at intake. Source review must resolve empty vertex or label sets, alphabets with
fewer than two labels, empty rational languages, the empty graph, graphs without a unique root,
unreachable vertices, identity or empty substitutions, finite graphs, isomorphic presentations,
sentences with no free variables, invalid encodings, and uniformity across different presentations.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the checked APIs provide
adjacent pieces only:

- `FirstOrder.Language.graph`, `SimpleGraph.structure`, and
  `FirstOrder.Language.Theory.simpleGraph` encode ordinary first-order simple graphs;
- `FirstOrder.Language.Sentence`, `FirstOrder.Language.Formula.Realize`, and
  `FirstOrder.Language.completeTheory` provide first-order syntax and semantics;
- `Language`, `DFA`, `DFA.accepts`, and `Language.IsRegular` provide finite-automata and regular-
  language interfaces; and
- `ComputablePred` expresses computability of an encoded predicate.

These declarations do not encode monadic second-order set quantification, directed labelled
transition graphs, the source's graph classes, rational graph transformations, `S2S`, or Caucal's
reduction. A bounded exact-topic search found no repo-local or pinned mathlib Caucal theorem. This
is discovery evidence only, not an exhaustive anchor audit or proof of absence.

## Explicit exclusions

- All finite graphs are not a substitute: finite adjacency and model checking do not establish the
  intended infinite-graph family result.
- First-order `completeTheory` is not the paper's monadic second-order theory.
- `THM-M-0871` Courcelle theorem, which the catalog separately describes as MSO decidability on
  bounded-treewidth graphs, owns a different target.
- Pushdown-only, regular/equational-only, tree-only, or one concrete graph instances may be source
  consequences, but none may silently replace the selected root.
- A structure field, typeclass, or hypothesis storing a decider, reduction, or desired theorem is
  circular and receives no proof credit.
- The catalog label, a DOI, a source download, a `#check`, a bounded search, or an experimental
  model checker is not kernel evidence.
