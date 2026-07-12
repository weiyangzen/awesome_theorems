# Scope map

## Preserved repository boundary

- Catalog title: `Rokhlin塔` (`Rokhlin tower`).
- Attribution and date: Vladimir Rokhlin, 1948.
- Literal gloss: `遍历理论的工具` (`an ergodic-theory tool`).
- Intended subject boundary: a source-selected theorem about a Rokhlin tower, not an arbitrary
  result that merely uses or resembles a tower.
- Assurance boundary: the catalog's `verified` field is discovery metadata and provides no source
  or machine-proof credit.

The classical Rokhlin lemma is the leading candidate family because inspected literature connects
the named tower, Rokhlin's 1948 note, and a tower whose finitely many disjoint levels cover almost
all of a probability space. This observation does not select one exact formulation.

## Decisions required at statement freeze

The dependent statement phase must approve an immutable source passage and freeze all of the
following before it writes a canonical proposition:

1. Whether the root is the tower-existence lemma itself, the periodic-approximation corollary used
   in the 1948 paper, or another source-named result.
2. A concrete unit interval with Lebesgue measure, an abstract standard/Lebesgue probability
   space, an arbitrary finite measure space, or another exact domain.
3. Whether atomlessness is explicit, derived from the chosen space, or replaced by a stronger
   standard-space hypothesis.
4. Whether the transformation is an invertible measurable equivalence, an almost-everywhere
   automorphism, or a noninvertible endomorphism, and whether it preserves or merely nonsingularly
   transports the measure.
5. The exact aperiodicity predicate: no periodic points, a null union of positive-period points, or
   a source-specific modulo-null/free-action condition. Ergodicity must not silently replace
   aperiodicity.
6. Tower height and indexing: `n`, `n + 1`, levels `0` through `n - 1`, and the lower bound on `n`.
7. Whether levels are forward images or preimages of the base, whether the base is measurable or
   only null-measurable, and whether disjointness is literal or almost everywhere.
8. The coverage conclusion and codomain: union measure `> 1 - epsilon`, complement measure
   `< epsilon`, strict versus weak inequalities, and normalization when total mass is not one.
9. Boundary behavior for heights zero/one, `epsilon <= 0`, `epsilon >= 1`, atomic spaces,
   periodic null sets, and representatives changed on null sets.
10. Lean universes, measurable equivalence representation, `Set.image` versus iterate preimages,
    finite union encoding, exact imports, classical-choice use, and any alternate encoding with a
    checked transport.

The source review must also reconcile the catalog's year 1948 with later sources that cite either
the 1948 short note or Rokhlin's 1949 survey, including the 1966 English translation.

## Explicit exclusions

- Kakutani skyscrapers or induced transformations as the root; the neighboring catalog target
  `THM-M-1409` is separately owned.
- The special ergodic proof route as a substitute for the general aperiodic theorem unless the
  approved source selects that special case.
- Cantor-set/clopen, topological marker, amenable-group, multidimensional, nonsingular, infinite
  measure, and C*-algebra Rokhlin lemmas without an approved source relationship.
- Only the definitions of a measure-preserving map, periodic point, standard Borel space, or
  almost-everywhere disjoint sets.
- The periodic-approximation corollary, generic nonmixing theorem, or rank-one definition merely
  because each uses Rokhlin towers.
- A structure containing the desired base, disjointness, and coverage as fields followed by a
  theorem that projects those assumptions.
- Literal disjointness silently weakened to almost-everywhere disjointness, or an image tower
  silently replaced by a preimage tower, without a checked equivalence under the selected map.
- The repository label `已验证` (`verified`) as evidence of a human proof, Lean statement, or
  kernel closure.

No canonical claim, Lean expression, discovery protocol, or obligation registry is frozen during
this intake. Those remain blocked on exact source and statement selection.
