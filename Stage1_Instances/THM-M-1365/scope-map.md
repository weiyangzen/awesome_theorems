# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-1365`, the label "Smale horseshoe," the gloss "a geometric
model of chaos," attribution to Stephen Smale, and the year 1967. Intake preserves that dynamical-
systems topic and its geometric/symbolic boundary. It does not turn the gloss into a theorem or
the untrusted status label into source-fidelity or kernel evidence.

## Proposition-changing decisions

An approved source selection must freeze all of the following before statement elaboration:

- whether the root concerns the explicit horseshoe construction, a class of horseshoe maps, a
  perturbation theorem, a global diffeomorphism, or a theorem derived from a transverse homoclinic
  point;
- the ambient plane, square, compact surface, or manifold; all topology, smoothness, metric, and
  dimension data; and whether the map is local, an embedding, a diffeomorphism onto its image, or a
  global self-diffeomorphism;
- the exact horizontal/vertical strips, crossing order, affine or cone estimates, contraction and
  expansion constants, boundary behavior, and any orientation assumptions;
- the maximal invariant set, including forward and backward iterate conventions and whether it is
  defined inside a non-invariant neighborhood, a global nonwandering set, or another object;
- the symbol alphabet and one- versus two-sided shift, product topology, shift orientation, coding
  map, and whether the conclusion is equality, bijection, homeomorphism, semiconjugacy, or
  topological conjugacy;
- whether compactness, invariance, Cantor-set structure, density or count of periodic points,
  indecomposability, hyperbolicity, entropy, chaos, or structural persistence is assumed or
  concluded; and
- every ordered binder, local/global quantifier, iterate exponent, exceptional case, and proof and
  source boundary.

These choices yield materially different propositions. This list is a resolution ledger, not a
canonical statement.

## Candidate source results not credited

Smale's 1967 Section 1.5 separates at least these candidate roots:

1. Proposition (5.1): periodic points of the full shift on a finite alphabet are dense, with
   exactly `N^k` points fixed by the `k`th iterate.
2. Proposition (5.3): for the described two-strip planar construction, the compact invariant
   indecomposable set is topologically conjugate to the full two-symbol shift.
3. Proposition (5.4): a similarly defined invariant set for a perturbation remains conjugate to
   that shift.
4. The global extension to a diffeomorphism of the sphere whose nonwandering set contains the
   horseshoe invariant set and two isolated fixed points.
5. Theorem (5.5): a transverse homoclinic point yields a Cantor invariant set on which a positive
   iterate is topologically a shift automorphism.

The catalog does not identify any one of these as its theorem. None is selected, conjoined,
asserted, or credited at intake.

## Explicit exclusions

- Replacing this target by generic symbolic dynamics (`THM-M-1401`), the shift map
  (`THM-M-1402`), topological entropy (`THM-M-1403`), or a Markov-partition theorem
  (`THM-M-1415`).
- Importing the distinct Stage0 physics records `THM-P-0778` (horseshoe dynamics) or
  `THM-P-0786` (horseshoe/shift conjugacy) as this target's canonical statement or evidence.
- Replacing the geometric horseshoe by the more general homoclinic theorem without a reviewed
  target decision, or conversely using one explicit affine example as a theorem about every
  transverse homoclinic point.
- Defining a structure that assumes the desired conjugacy, invariant-set properties, hyperbolicity,
  or chaos conclusion and then projecting that field.
- Treating a plotted folded square, finite orbit sample, numerical Lyapunov exponent, animation,
  or simulation as proof.
- Treating a generic semiconjugacy or stream API, a bounded no-match search, or the catalog label
  `已验证` as statement identity or proof evidence.

## Boundary cases

The statement phase must resolve tangencies versus transverse crossings, touching strip
boundaries, zero or one crossing component, more than two strips, degenerate contraction or
expansion constants, noninjective maps, one-sided versus two-sided iteration, empty invariant set,
points escaping the chosen neighborhood, coding nonuniqueness at boundaries, orientation reversal,
the iterate `m = 0` versus `m > 0`, and local conclusions misread as global chaos claims.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, streams, function semiconjugacy and iteration,
periodic-point predicates, and generic homeomorphisms are available. A bounded repository and
pinned-mathlib search found no exact named Smale-horseshoe or horseshoe-conjugacy declaration under
the recorded terms. The API probe and negative search are intake discovery inputs only, not an
exhaustive anchor audit, source-identical target, or proof.
