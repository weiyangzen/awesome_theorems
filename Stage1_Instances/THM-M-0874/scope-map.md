# Scope map

## Preserved theorem boundary

The intake preserves the catalog's Babai graph-isomorphism quasipolynomial-algorithm family. The
post-fix source lead states the stable high-level result: there is a deterministic algorithm for
deciding whether two finite graphs are isomorphic, with worst-case running time
`exp((log n)^(O(1)))`, where `n` is the number of vertices. This human-level statement does not yet
determine one exact Lean expression.

The source proof runs primarily through String Isomorphism. Babai v2 states String Isomorphism as
Theorem 1.1.1 and derives Graph Isomorphism and Coset Intersection as Corollary 1.1.2. The post-fix
Bourbaki exposition states the corresponding results as Theorem 1.1 and Corollary 1.2. A later
formalization must model the string algorithm and the graph-to-string reduction explicitly; it may
not replace the catalog target by String Isomorphism or Coset Intersection alone.

## Decisions required at statement freeze

1. Fix the graph domain: finite simple undirected loopless graphs, a colored or directed extension,
   vertex types, labels, equal versus unequal orders, and the exact isomorphism witness relation.
2. Fix a canonical finite serialization of a graph pair, valid and malformed inputs, padding and
   canonicalization, and whether complexity is measured by vertex count or encoding length.
3. Decide whether the output is a Boolean decision, an optional isomorphism witness, a coset of all
   isomorphisms, a generating set for automorphisms, or an explicitly related bundle.
4. Freeze the deterministic computation model, totality and halting contract, primitive step and
   cost measure, uniformity, and worst-case quantification.
5. Define quasipolynomial time exactly: a bound such as `exp(C * (log n)^c)` for constants `c, C`
   and sufficiently large `n`, including logarithm base, real/natural rounding, threshold, and
   treatment of small inputs.
6. Freeze the ordered binders and conclusion: existence of a machine, correctness on every valid
   encoded graph pair, totality, and the time bound, with every constant and threshold quantified in
   the intended order.
7. State and check the Graph Isomorphism to String Isomorphism encoding, induced symmetric-group
   action on unordered vertex pairs, correctness in both directions, and polynomial overhead.
8. Select and preserve the complete repaired source bundle, reconcile v2, the UPCC fix, the Design
   Lemma correction and the post-fix reconstruction, and assign every proof branch to a source.

## Candidate roots and branches

- Existence and correctness of a fully specified deterministic Graph Isomorphism decision
  procedure.
- Worst-case quasipolynomial running time for that procedure.
- A conjunction of totality, decision correctness, and the bound, with separate obligations.
- String Isomorphism Theorem 1.1.1 plus the graph-to-string reduction yielding Graph Isomorphism.
- The stronger witness/coset output described by the post-fix exposition.
- Coset Intersection, colored graphs, or orbit-sensitive refinements as separately typed branches.

Only the complete source-approved Graph Isomorphism root may instantiate this target. A branch,
definition, reduction, or stronger output contract cannot silently replace it.

## Boundary and degenerate cases

Statement work must decide empty and singleton graphs; unequal vertex counts; isolated vertices;
empty and complete graphs; loops, parallel edges, directions, colors, and labels; duplicate and
noncanonical encodings; malformed or truncated inputs; zero-length inputs; graph pairs on different
vertex types; zero and one in logarithms; rounding of real bounds to natural step counts; constants
and the sufficiently-large threshold; and whether an invalid input returns false, an error, or lies
outside the quantified domain. No case is excluded at intake.

## Explicit exclusions

- Plain decidability, brute-force enumeration, or membership of Graph Isomorphism in NP is not the
  quasipolynomial result.
- An oracle, assumed solver, stored correctness witness, benchmark, timing experiment, or generated
  certificate cannot serve as the algorithm or proof.
- A polynomial-time algorithm for a special graph class, the Weisfeiler-Leman heuristic, canonical
  labeling alone, or an average-case bound cannot replace the general worst-case target.
- Generic `SimpleGraph.Iso`, `Language`, computability, or unbounded computable-reduction APIs are
  substrate, not Babai's algorithm or its resource bound.
- The pre-fix v2/STOC text cannot be treated as the complete corrected proof without the repair
  bundle and post-fix reconciliation.
- The catalog's `已验证` label, a source URL, or an API probe gives no H0 or machine-proof credit.

## Neighbor and formal boundaries

`THM-M-0873` owns the generic graph-isomorphism/quasipolynomial complexity record,
`THM-M-0875` owns the Weisfeiler-Leman algorithm family, `THM-M-0876` owns the position of Graph
Isomorphism relative to P and NP, and `THM-M-1567` is another generic Graph Isomorphism catalog
record. Their statements and proof credit do not transfer by topical proximity.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`SimpleGraph.Iso` expresses adjacency-preserving bijections, `Language` expresses predicates on
strings, and `Turing.TM2ComputableInTime` packages a machine, a time function, and an output bound.
Mathlib's `ManyOneReducible` is computability-based rather than a polynomial-resource reduction.
A bounded intake search found no Babai, String Isomorphism, Graph Isomorphism complexity, or
quasipolynomial implementation. These observations are discovery only, not the downstream immutable
anchor audit or a proof of global absence.
