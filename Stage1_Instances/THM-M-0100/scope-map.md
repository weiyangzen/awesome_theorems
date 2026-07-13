# Scope map

## Preserved theorem family

The intake preserves Kazhdan's Property (T) family for topological groups. It does not turn the
property name into the tautology `PropertyT G -> PropertyT G`, nor select one of these materially
different common theorem surfaces:

- existence of a compact Kazhdan set as the definition of Property (T);
- every continuous unitary representation with almost invariant vectors has a nonzero invariant
  vector;
- for locally compact groups, isolation of the trivial representation in the unitary dual;
- compact generation or finite generation consequences;
- Property (T) for a specified higher-rank group, or inheritance by lattices; and
- for sigma-compact locally compact groups, equivalence with Property (FH).

A later statement phase may select one root only from a complete, immutable, independently reviewed
source passage. Any claimed alternate formulation requires a source-faithful, kernel-checked
transport.

## Decisions required at statement freeze

1. Decide whether the root is the predicate definition, a characterization theorem, a consequence,
   an example family, or an equivalence theorem, and identify its exact source result and proof
   boundary.
2. Fix the group carrier and universe, topology, separation and local compactness assumptions,
   sigma-compactness or compact generation, and any countability conditions.
3. Fix complex Hilbert-space conventions and the continuous unitary representation model, including
   strong continuity, inner-product orientation, zero-dimensional spaces, and universes.
4. Define invariant and nonzero invariant vectors, `(Q, epsilon)`-invariance, almost invariant
   vectors, compact Kazhdan sets, and the strict versus non-strict inequality convention.
5. Fix ordered binders over representations, Hilbert spaces, compact subsets, positive constants,
   and vectors, including normalization versus scale-invariant formulations.
6. For alternate forms, define weak containment, the unitary dual and Fell topology, affine
   isometric actions, fixed points, or first cohomology as needed, and prove both transport
   directions under the precise domain assumptions.
7. Freeze all boundary cases, foundation/TCB/computation profiles, minimal imports, and statement
   mutation tests before inspecting proof closure.

## Degenerate and boundary cases

Source review must explicitly dispose of the trivial and compact group cases; empty or
subsingleton carriers allowed by the selected typeclass contract; zero Hilbert space; zero versus
unit vectors; the empty compact subset; `epsilon = 0` versus `epsilon > 0`; representations already
containing invariant vectors; discrete versus nondiscrete topology; non-locally-compact groups;
non-sigma-compact groups in the Property (FH) equivalence; and real versus complex Hilbert spaces.

No case is excluded at intake. Packaging a Kazhdan set or the desired implication as an input field
and projecting it is circular rather than a proof of a source theorem.

## Neighbor and substitution exclusions

- Kazhdan-Lusztig polynomials, conjectures, and bases are unrelated despite sharing a name.
- Spectral-gap, expander, ergodicity, fixed-point, cohomology-vanishing, finite-generation, and
  lattice results may be consequences or characterizations, but none silently replaces the root.
- A proof for only a finite group, compact group, a named matrix group, or a finite-dimensional
  representation is not a proof of an unrestricted source-selected formulation.
- Generic algebraic `Representation.invariants` infrastructure does not encode continuity,
  unitarity, almost invariance, compact Kazhdan sets, or Property (T).
- The catalog's `verified` label and the intake API probe receive no source or machine-proof credit.
