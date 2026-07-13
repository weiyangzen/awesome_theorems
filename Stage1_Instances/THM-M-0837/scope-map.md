# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0837`, the label `Robertson-Sanders-Seymour-Thomas证明`, the
attribution `Robertson等`, the year 1997, and the gloss `四色定理的新证明`. These literals identify
the RSST Four-Colour Theorem proof family and provenance, but they are not one binder-complete
proposition. Importance `高` and status `已验证` are inventory metadata, not source or Lean evidence.

The strongest bibliographic lead is Neil Robertson, Daniel P. Sanders, Paul Seymour, and Robin
Thomas, "The Four-Colour Theorem," *Journal of Combinatorial Theory, Series B* 70(1), 1997,
pp. 2-44, DOI `10.1006/jctb.1997.1750`. Crossref and the authors' bibliography agree on that
metadata. The full JCTB proof text was not successfully retrieved in this intake and is not claimed
as inspected proof evidence.

An author-maintained summary and the authors' 1996 announcement, "A New Proof of the Four-Colour
Theorem," were inspected as discovery evidence. The announcement's visible abstract states the
ordinary graph conclusion: every finite loopless planar graph admits a vertex-colouring with at
most four colours. It also exposes the proof-specific architecture described below. Neither source
lead selects this repository target's exact root or supplies H0.

## Candidate roots not selected

- Ordinary Four-Colour Theorem: every finite loopless planar graph is vertex-four-colourable.
- The same conclusion with a required, source-faithful RSST proof and computation provenance.
- Clause (2.2): no good configuration appears in a minimal counterexample.
- Clause (2.3): every internally 6-connected triangulation contains a good configuration.
- The conjunction of the two clauses with the minimal-counterexample reduction and composition to
  the Four-Colour Theorem.
- Correctness and completeness of the reducibility and unavoidability programs, configuration
  corpus, rules, data, compiler/runtime assumptions, and their composition to the mathematical root.
- A quadratic algorithm that returns a four-colouring of an input planar graph, with a frozen
  representation, correctness theorem, and complexity model.

These are inequivalent proposition or provenance packages. None receives statement or proof credit
at intake.

## Proposition-changing decisions

Before statement work, accountable and independent review must decide:

- whether the root is the generic theorem, a proof-provenance package, a clause suite, the algorithm,
  or an exact conjunction;
- map colouring versus graph colouring, and the checked transport between them;
- finite graph representation, loop and parallel-edge conventions, planar versus plane embedding,
  faces, connectedness, triangulation, and the reduction from an arbitrary planar graph;
- colour type, "at most four" convention, properness, empty/small/disconnected graphs, and all
  ordered binders and universes;
- minimal-counterexample ordering and existence, internal 6-connectivity, near-triangulations,
  configurations, rings, appearance, good configurations, and the exact 633-object corpus;
- D-reducibility, C-reducibility, safe reducers, consistency sets, and the precise role of the
  reducibility program;
- the 32 discharging rules, charge convention, cartwheels, degree cases, finite case corpus, and the
  precise role of the unavoidability program; and
- source edition, incorporated clauses, proof and computation boundaries, corrections or errata,
  compiler/runtime/hardware trust, replay policy, and independent review.

## Boundary and degenerate cases

The statement phase must resolve empty vertex and edge sets, disconnected graphs, bridges,
isolated vertices, loops and parallel edges, finite versus infinite graphs, graph embeddings with
crossings, outer-face conventions, non-triangulated graphs, small triangulations, separating rings
of sizes three through five, multiple embeddings, configuration isomorphism and induced-subgraph
conditions, vertices outside the source degree ranges, malformed or incomplete configuration/rule
data, and algorithm inputs outside its declared representation.

## Explicit exclusions

`THM-M-0833` owns the generic Four-Colour Theorem label. `THM-M-0836` owns the Appel-Haken computer
proof, and `THM-M-0838` owns Gonthier's Coq formal proof. Their future statements, state, evidence,
and proof bodies do not transfer to this target without an accepted shared-obligation and
proof-provenance decision.

A theorem assuming a four-colouring, reducibility, unavoidability, the 633 configuration result,
the discharging conclusion, algorithm correctness, or certificate validity is not a proof of that
assumption. A fixed finite graph, finite sample, picture, search result, historical executable run,
floating status label, or citation is not a substitute. General colouring lemmas do not establish
planarity or four-colourability.

## Computation and Lean boundary

The author sources report integer-arithmetic programs and explicitly discuss unproved compiler and
hardware trust. Later author-hosted arXiv records `1401.6481` and `1401.6485` describe the two
computer-verified lemmas and ancillary program/data packages. These are discovery leads only: no
archive, program, corpus, certificate, parser, checker, run, or trust closure is pinned or credited
here.

Pinned mathlib supplies `SimpleGraph.Coloring`, `SimpleGraph.Colorable`, and chromatic-number
interfaces. Its colouring module explicitly lists planar graphs as TODO, and the bounded local
search found no Four-Colour or RSST declaration or simple-graph planarity predicate. The API probe
is substrate discovery only, not a statement, anchor audit, transport, computation, or proof.
