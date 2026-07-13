# Scope map

## Preserved theorem family

The intake preserves two related but non-identical surfaces instead of forcing them into one
unreviewed proposition:

- the standard Bannai-Ito conjecture: for every fixed integer valency `k >= 3`, there are only
  finitely many distance-regular graphs of valency `k`; and
- the repository's literal gloss: a bound on the diameter of distance-regular graphs.

In the proof paper, a distance-regular graph is finite and connected. For vertices at distance
`i`, the numbers of neighbors one layer nearer and one layer farther depend only on `i`; regularity
and valency `k = b_0` follow. Section 2.3.2 observes that a bound on diameter as a function of fixed
`k` implies finiteness because bounded degree and diameter bound the number of vertices. It also
quotes the different Ivanov bound `D_Gamma <= F(k) h_Gamma`. These facts explain the catalog gloss
but do not make every diameter inequality identical to Theorem 1.1.

## Decisions required at statement freeze

1. Preserve and independently review the original 1984 page and an immutable proof edition,
   including definitions, assumptions, theorem locator, proof boundary, corrections, and errata.
2. Decide whether the repository root is the standard finiteness theorem, a source-numbered
   diameter theorem, or a checked conjunction. Record an exact implication or equivalence for the
   catalog's diameter gloss rather than treating prose similarity as identity.
3. Fix the graph model: finite loopless undirected graphs, connectedness, natural path distance,
   diameter, and the complete intersection-number definition of distance-regularity.
4. Fix the ordered quantifiers. The standard reading is `for every k >= 3`, followed by finiteness
   of the class for that fixed `k`; this is not one bound for a single chosen graph and not a claim
   that only finitely many distance-regular graphs exist in total.
5. Choose a small/universe-stable representation of finite graphs up to graph isomorphism. Raw
   existential carriers across arbitrary universes do not by themselves form the finite set of
   isomorphism classes asserted by the source.
6. Define how graph isomorphisms preserve distance-regularity and valency, and whether finiteness is
   encoded by a finite set of representatives, a bounded `Fin n` normal form, `Set.Finite`, or an
   equivalent quotient. Check every credited transport.
7. Freeze the foundation, classical choice, quotient, computation, and finite-enumeration policy,
   then mutation-test domain, binder order, hypotheses, conclusion, and boundary cases.

## Degenerate and boundary cases

The source threshold excludes valencies `0`, `1`, and `2`; the statement gate must test that
changing `k >= 3` to `k >= 2` changes the claim, since cycles give an infinite valency-two family.
It must also preserve the source convention that distance-regular graphs are finite and connected,
rather than relying on mathlib's natural-valued diameter, which is `0` for disconnected finite
nontrivial graphs. Empty and singleton carriers, complete graphs of diameter one, diameter zero,
and any convention for one-vertex valency must be disposed of explicitly.

Finiteness must mean finitely many graphs up to the selected isomorphism relation. Finitely many
intersection arrays, bounded vertex order, a bound on diameter, and finitely many labeled graphs on
each fixed carrier are useful bridges but are not definitionally the same conclusion. Each required
direction needs a checked witness.

## Explicit exclusions

- A generic diameter inequality, Ivanov's `D <= F(k) h`, or a bound that still depends on the graph
  through `h` cannot replace the fixed-valency finiteness root without a complete checked bridge.
- Distance-transitive graphs, Moore graphs, strongly regular graphs, bipartite graphs, and any fixed
  valency such as `3`, `4`, `5`, `6`, or `7` are proper subclasses or special cases.
- The valency-two case cannot be included: cycles are a counterfamily to the finiteness claim.
- The broader `THM-M-0894` distance-regular-graph topic supplies definitions, not this finiteness
  theorem or its proof.
- A structure carrying an assumed diameter bound, a finite list of all graphs, intersection data,
  or an isomorphism certificate is an interface, not a proof of existence of that bound or list.
- Bounded degree plus bounded diameter without the finite connected simple-graph hypotheses and the
  reconstruction to finitely many isomorphism classes is only part of the route.
- The catalog status, paper title, API probe, metadata response, or bounded name search supplies no
  accepted proof credit.

## Formal discovery boundary

Pinned mathlib supplies `SimpleGraph`, `SimpleGraph.Connected`, `SimpleGraph.IsRegularOfDegree`,
`SimpleGraph.dist`, `SimpleGraph.edist`, `SimpleGraph.diam`, and `SimpleGraph.Iso`. It does not expose
an identified `DistanceRegular` predicate or Bannai-Ito declaration in the bounded graph-source
search. The probe authenticates adjacent APIs only; the exhaustive immutable anchor audit and the
exact formal target remain downstream.
