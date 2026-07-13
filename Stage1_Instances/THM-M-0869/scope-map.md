# THM-M-0869 scope map

## Received scope

The repository record names `禁用子图问题` and says only `禁用子图类的刻画`. It attributes the
topic collectively to many mathematicians in the twentieth century and marks it `已验证`. Under
rev-5.6 that status is untrusted inventory metadata. The Stage0 projection classifies the record as
a problem or decision proposition while explicitly leaving its definitions, premises, proof route,
dependencies, equivalent forms, axiom policy, machine status, and artifacts open.

## Candidate roots not credited

The received words are compatible with distinct statements:

1. A class of finite simple graphs is closed under ordinary subgraphs if and only if it is the
   class avoiding some, generally infinite, family under ordinary subgraph containment.
2. A hereditary class is exactly a class avoiding some family of induced subgraphs.
3. A minor-closed class is described by excluded minors, with a finite obstruction family only
   after invoking the Graph Minor Theorem.
4. A concrete graph class has a specified finite forbidden-subgraph, induced-subgraph, topological-
   minor, or minor characterization.
5. Given a fixed finite obstruction family, class membership is decidable or has a stated
   complexity bound under a fixed graph encoding.

The first two can become definitional representation facts when the obstruction family is chosen
as all minimal or all excluded graphs. The third has far stronger mathematical content. The fourth
and fifth require a named class and exact obstruction/algorithm data. None can be substituted for
another without changing the theorem.

## Proposition-changing decisions

Before statement elaboration, an approved source decision must freeze:

- one immutable primary or authoritative source edition, exact theorem/problem locator,
  incorporated definitions, proof boundary, correction history, and independent review;
- finite versus infinite, simple versus directed/multi/hypergraph objects, labeled versus
  isomorphism classes, vertex universes, and finiteness/typeclass assumptions;
- ordinary subgraph, induced subgraph, topological minor, minor, immersion, or another containment
  preorder, including orientation of the relation and equality up to isomorphism;
- the graph property or class, its isomorphism closure, and whether closure under the chosen
  containment relation is a hypothesis, conclusion, or definition;
- the obstruction family, whether it is arbitrary, canonical, minimal, an antichain, finite,
  computable, or explicitly enumerated, and whether existence or uniqueness is claimed;
- whether the target is a representation equivalence, a finite-basis theorem, a concrete
  characterization, a recognition theorem, or a branch ledger;
- ordered binders, universes, all hypotheses and side conditions, and the exact conclusion; and
- empty graphs, empty classes, empty obstruction families, duplicate/isomorphic obstructions,
  infinite vertex types, loops, isolated vertices, and other boundary cases.

## Neighbor target boundaries

- `THM-M-0840` separately owns the Strong Perfect Graph Theorem, a concrete forbidden induced-
  subgraph characterization.
- `THM-M-0865` separately owns Kuratowski's planar characterization by subdivisions of `K5` and
  `K3,3`; it cannot silently supply this generic root.
- `THM-M-0866` separately owns Wagner's forbidden-minor characterization of planar graphs.
- `THM-M-0867` separately owns the Robertson-Seymour graph-minor well-quasi-order theorem.
- `THM-M-0868` separately owns the Graph Minor Theorem/Wagner-conjecture proof family.

No statement, status, or proof credit transfers from a neighboring target.

## Explicit exclusions

- Defining an obstruction family from the complement of an arbitrary class and presenting the
  resulting tautology as a source-selected deep classification theorem.
- Replacing ordinary subgraphs with induced subgraphs, topological minors, or minors because that
  relation has a more convenient API or famous theorem.
- Adding finiteness, minimality, computability, decidability, or complexity conclusions absent from
  the selected source.
- Restricting to planar, perfect, chordal, line, interval, or another concrete graph class without
  source authorization.
- Encoding the desired characterization in a structure field, hypothesis, axiom, oracle, or
  unchecked certificate.
- Treating the catalog's `已验证` label, a theorem name, an API check, or bounded no-match search as
  source or proof evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks ordinary copy containment
`G ⊑ H`, freeness, induced containment `G ⊴ H`, transitivity, and existence-of-subgraph witness
interfaces from `Mathlib.Combinatorics.SimpleGraph.Copy`. These APIs can support some future
encodings, but they do not select the graph-class universe or theorem. A bounded search found no
exact generic forbidden-class characterization and no simple-graph minor API in the inspected
directory. This is not a global absence result or a complete anchor audit.
