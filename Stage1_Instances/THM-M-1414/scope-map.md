# Scope map

## Received scope

The repository fixes the title `谱分解定理`, Stephen Smale, 1967, and only the gloss "decomposition
of Axiom A systems." It supplies no bibliography, dynamical category, definitions, ordered
binders, hypotheses, conclusion, exception policy, or formal artifact. The metadata status
`已验证` is untrusted under rev-5.6.

## Leading candidate family

Smale's 1967 theorem (6.2) is the leading candidate. A source-faithful statement would need to
freeze all of the following:

- a compact differentiable manifold `M` and a diffeomorphism `f : M -> M` with the exact source
  regularity and boundary conventions;
- the nonwandering set `Omega(f)` with Smale's definition;
- Axiom A: `Omega(f)` is hyperbolic and the periodic points of `f` are dense in `Omega(f)`;
- the source's invariant stable/unstable tangent-bundle splitting and contraction/expansion data;
- a finite indexed family of subsets whose union is exactly `Omega(f)`;
- pairwise disjointness, closedness, invariance, and indecomposability of every piece;
- topological transitivity of the restriction of `f` to every piece; and
- uniqueness of the decomposition in the exact sense intended by the source.

These bullets delimit a candidate theorem family; they do not select or assert the canonical root.

## Decisions required at statement freeze

1. Select theorem (6.2) for diffeomorphisms or Part II theorem (5.2) for flows through an
   accountable source review. They are not interchangeable encodings.
2. Pin the exact manifold category, compactness, smoothness, boundary, metric, diffeomorphism, and
   derivative conventions used by the selected theorem.
3. Formalize the nonwandering set, periodic points, invariant hyperbolic splitting, uniform
   contraction/expansion, and density clauses without weakening Axiom A.
4. Resolve Smale's `indecomposable` terminology and its relationship to the separately asserted
   topological transitivity clause; neither clause may be silently discarded as redundant.
5. Decide how a finite decomposition is represented: a natural `k`, a nonempty finite index type,
   a finite set of subsets, or another encoding, with checked transports for any credited forms.
6. Specify whether uniqueness means equality after reindexing, equality as a finite set of pieces,
   or a source-defined canonical equivalence.
7. Resolve empty and singleton boundary cases, including an empty nonwandering set, `k = 0`, empty
   pieces, and whether indecomposable pieces are necessarily nonempty.
8. Reconcile Smale's dense-orbit definition of topological transitivity with the open-set action
   class available in pinned mathlib; no equivalence may be assumed without its hypotheses and a
   checked witness.
9. Audit the proof boundary: theorem (6.2) is followed by a proof sketch in section 1.7 and cites
   source [117], which has not been inspected in this intake.

## Explicit exclusions

- The linear-algebra or functional-analysis spectral theorem, spectral measures, eigenvalue
  decompositions, or operator spectra.
- The flow theorem Part II (5.2) silently substituted for the diffeomorphism theorem (6.2), or the
  converse substitution.
- A decomposition of the whole manifold in place of the nonwandering set. Smale's stable-set
  decomposition of the manifold is the separate corollary (6.3).
- Arbitrary homeomorphisms, continuous self-maps, endomorphisms, semigroup actions, or systems that
  do not satisfy the selected Axiom A hypotheses.
- Merely partitioning a finite set, or returning pieces already assumed in a structure, as a proof
  of existence and uniqueness.
- A cyclic decomposition into mixing components, a Markov partition, symbolic coding, structural
  stability, or zeta-function rationality as a replacement root.
- Generic pinned APIs for invariant sets, periodic points, or topological transitivity as evidence
  for Axiom A, hyperbolicity, the decomposition, or its proof.

No canonical Lean target is frozen at intake. The primary candidate is precise enough to guide the
dependent statement phase, but selecting it before independent review would overstate what the
repository's broad gloss establishes.
