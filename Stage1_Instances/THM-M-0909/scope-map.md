# Scope map

## Preserved catalog scope

The intake preserves the existential counterexample family denoted by the catalog gloss
`非4-可选的平面图`: Voigt's result that a planar graph is not 4-choosable. The catalog attribution
and year agree with the 1993 paper, and a zbMATH review reports a 238-vertex witness. The exact
primary-source proposition is not yet admitted, so this family description is not a canonical
statement or a Lean target.

## Candidate root, not credited

A standard candidate is: there exists a finite planar simple graph `G` that is not 4-choosable,
meaning that some assignment of allowed-color collections, each of cardinality at least four,
admits no proper vertex coloring that selects an allowed color at every vertex. A stronger
source-specific candidate additionally requires `G` to have 238 vertices.

Those formulations guide scope analysis only. Neither is selected or elaborated at intake.

## Proposition-changing decisions

Before statement elaboration, an admitted source and accountable review must freeze:

- the 1993 primary edition, exact theorem or construction locator, incorporated definitions,
  complete proof boundary, corrections and errata, and the relationship to the 2006 reprint;
- finite simple undirected graphs versus a plane graph, multigraph, or other carrier, including
  finiteness, decidable equality, loops, parallel edges, and isolated vertices;
- abstract planarity versus a supplied plane or sphere embedding, and the exact combinatorial or
  topological embedding representation;
- the color carrier and whether allowed colors range over integers, a finite global palette, or an
  arbitrary type;
- `Finset`, finite set, multiset, or duplicate-bearing list representation and whether duplicates
  affect cardinality;
- lists of exactly four colors versus at least four colors and the checked monotonic relationship
  between those definitions;
- the ordered binders for graph existence, planarity, list assignments, cardinality hypotheses,
  coloring functions, membership, and properness;
- `not 4-choosable` as a negated universal property versus an explicit bad-list witness, with a
  checked transport between the two forms; and
- whether the 238-vertex cardinality is part of the canonical conclusion or only construction
  provenance.

## Boundary and degenerate cases

No case is excluded at intake. Source review must decide empty and singleton graphs, edgeless and
disconnected graphs, isolated vertices, empty color carriers, finite versus infinite palettes,
duplicate list entries, lists with more or fewer than four distinct colors, vacuous colorings, and
whether planarity is proof-relevant. It must also ensure that a source construction really gives
one bad list assignment rather than merely failing ordinary four-colorability.

## Neighbor target boundaries

- `THM-M-0906` is the general list-coloring topic. Future definitions or proofs there do not
  establish Voigt's planar counterexample.
- `THM-M-0908` is Thomassen's planar-list-coloring upper-bound family. Every planar graph being
  5-choosable does not construct a graph that is not 4-choosable.
- `THM-M-0833` is the four-color theorem. Ordinary 4-colorability and 4-choosability are different;
  a graph may be ordinarily 4-colorable while failing a particular four-list assignment.

## Explicit exclusions

- Ordinary graph colorability, chromatic number at most four, or the four-color theorem presented
  as list choosability.
- Thomassen's five-choosability theorem, a six-choosability bound, or a result for a special planar
  graph subclass presented as Voigt's counterexample.
- An arbitrary small graph, drawing, or list assignment not checked against the selected source
  construction and planarity definition.
- A structure or hypothesis that stores the desired bad assignment, planarity witness, or
  non-choosability conclusion without constructing it from the theorem's premises.
- SAT, exhaustive search, native computation, an image, or an unchecked certificate presented as a
  general kernel proof.
- The catalog's `已验证` label, bibliographic metadata, the secondary review, or the API probe
  used as H0 or machine-proof credit.

## Downstream boundary

The statement phase must admit and independently review an immutable primary source, then freeze
one exact proposition and minimal Lean encoding. Complete formal-candidate discovery, obligation
architecture, proof work, trust and provenance checks, validation, and release remain separate
open tasks.
