# Scope map

## Preserved theorem family

The intake preserves the Wecken minimum-fixed-point realization family suggested by the catalog's
title, attribution, date, and Nielsen-number gloss. A later statement phase may select a root only
after an immutable source passage and its incorporated definitions have been mapped and
independently reviewed.

Candidate mathematical components, none credited here as the canonical claim, include:

- a source-specified compact polyhedron, manifold, or related topological space `X`;
- a continuous self-map `f : X -> X` and its free or otherwise specified homotopy class;
- Nielsen fixed-point classes, their fixed-point indices, essential classes, and the count `N(f)`;
- a minimum fixed-point number obtained from the cardinalities of fixed-point sets of maps
  homotopic to `f`; and
- a realization map `g` homotopic to `f` with exactly `N(f)` fixed points, or the resulting equality
  between the minimum fixed-point number and `N(f)`.

## Decisions required at statement freeze

The statement phase must freeze all of the following from an approved source rather than from a
modern textbook convention:

1. The exact paper, theorem or page locator, original terminology, translation, incorporated
   definitions, proof boundary, correction history, and independent review.
2. The class of spaces, including compactness, connectedness, triangulability or ANR hypotheses,
   manifold dimension, boundary, and any exceptional low-dimensional cases.
3. The carrier and regularity of maps, and whether homotopy is free, based, relative to a boundary,
   or subject to another constraint.
4. The path or lift/Reidemeister definition of fixed-point classes, the index convention, the
   meaning of essential, and the finite count represented by the Nielsen number.
5. The definition of the minimum fixed-point number: a minimum versus an infimum, the admitted
   class of representatives, and the treatment of infinite fixed-point sets.
6. Whether the root is an existence statement for a realizing representative, an equality
   `MF[f] = N(f)`, a conjunction, or another source proposition.
7. The ordered binders, quantifier dependencies, hypotheses, conclusion, universes, foundation
   policy, and exact equality/cardinality encoding.

## Boundary and degenerate cases

Source review must explicitly resolve empty, singleton, disconnected, noncompact, or
nontriangulable spaces; dimensions zero, one, two, and the source threshold; manifolds with
boundary; maps with no or infinitely many fixed points; identity and constant maps; inessential
zero-index classes; maps homotopic to fixed-point-free representatives; and whether a minimum is
attained. No case is silently excluded at intake.

## Neighbor and substitution exclusions

- `THM-M-0642` separately owns the catalog's Nielsen fixed-point-theory item. Definitions,
  invariance, and the Nielsen lower bound from that family do not themselves establish Wecken
  realization, and no status or evidence transfers between targets.
- `THM-M-0641`, `THM-M-0640`, and `THM-M-0636` own Lefschetz and Brouwer fixed-point families;
  existence of some fixed point is not a minimum-realization theorem.
- A surface-only result cannot silently replace a source theorem in dimension at least three, or
  conversely; low-dimensional exceptions cannot be erased.
- A definition of `N(f)`, homotopy invariance, or the lower bound `N(f) <= #Fix(g)` is not the
  realization/equality direction.
- Generic fixed-point, homotopy, fundamental-group, quotient, or covering APIs provide substrate
  only. A structure or premise that assumes a realizing representative is not a proof.
- The catalog's `已验证` label and the discovery-only probe supply no human or machine proof credit.

No canonical Lean target, expression fingerprint, alternate encoding, mutation result, obligation
registry, discovery protocol, or proof state is frozen at intake.
