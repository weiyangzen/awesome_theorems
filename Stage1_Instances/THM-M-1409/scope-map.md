# Scope map

## Frozen catalog boundary

- Target: `THM-M-1409`, execution rank 908, `L0 / rework_required`.
- Title: `Kakutani塔` (Kakutani tower).
- Catalog attribution and date: Shizuo Kakutani, 1943.
- Literal gloss: `诱导变换的构造` ("construction of an induced transformation").
- Intended field: measure-theoretic dynamical systems and ergodic theory.
- The manifest value `已验证` is untrusted metadata and supplies no source or proof credit.

These facts delimit a topic and construction family. They do not yet determine one theorem.

## Candidate mathematical components

A source-selected target may involve some or all of the following, but intake credits none as the
canonical claim:

1. A measure-preserving endomorphism or invertible transformation `T` of a probability, finite, or
   sigma-finite measure space.
2. A measurable base `A`, commonly of positive measure, and a first positive return time
   `r_A(x) = min {n >= 1 | T^n x belongs to A}` on a source-specified recurrent domain.
3. The induced transformation `T_A(x) = T^(r_A(x)) x` on `A`, with a precise convention for points
   whose return time is infinite.
4. The unnormalized restricted measure used in the located 1943 source and a conclusion about the
   induced map's strong-sense measure preservation and ergodicity. A normalized probability
   version would require a checked alternate encoding rather than silent replacement.

The located paper calls this an induced measure-preserving transformation and does not use the
later "tower" or "skyscraper" terminology. Tower levels, converse skyscraper representation, and
Kac's formula remain interpretation risks to exclude or map explicitly, not equally supported
components of the source-aligned root.

## Decisions required at statement freeze

The next phase must freeze from a pinpoint primary passage:

1. Whether the root is a definition/construction, an existence theorem, a decomposition theorem,
   a preservation theorem, an ergodicity equivalence, an integral formula, or a representation.
2. The measurable-space and measure hypotheses, including completeness, probability/finite status,
   and whether statements are pointwise or almost everywhere.
3. Whether `T` is merely measurable, nonsingular, conservative, measure preserving, invertible,
   or ergodic, and which of these are assumptions versus conclusions.
4. The base-set hypotheses and whether zero/full measure bases or atoms are allowed.
5. Positive first return versus first hitting time, the codomain (`Nat`, positive naturals, or an
   extended value), and behavior on nonreturning points.
6. The exact induced-map carrier, measurable structure, measure normalization, tower-level formula,
   ordering/indexing, disjointness, and coverage boundary.
7. Every degenerate case, alternate encoding, and direction of any claimed equivalence.

## Explicit exclusions

- Rokhlin's tower lemma or a finite approximately exhaustive Rokhlin tower as a substitute; it is
  the separate target `THM-M-1410`.
- Poincare recurrence alone. It can establish return behavior but is not itself the requested
  induced-transformation/tower construction.
- Kac's return-time formula alone, an arbitrary suspension, or a Young tower.
- A finite-height tower, constant return-time special case, invertible-only or probability-only
  specialization unless the inspected source selects it.
- A structure that accepts the return time, induced map, preservation laws, or coverage as fields,
  followed by a tautological constructor or projection.
- Mathlib's generic partial-function `PFun.fix`, which its documentation calls a first-return map
  but which is not an ergodic Kakutani construction.
- Any recurrence theorem checked by `IntakeProbe.lean` merely because the pinned library provides
  it, or the catalog's `verified` label as evidence.

No canonical Lean proposition or boundary policy is frozen at intake. The statement phase must
resolve the source identity before proof-tree construction or formal-candidate credit.
