# Scope map

## Preserved theorem family

The intake preserves the catalog's Euclidean triangle-concurrency family. In its familiar form,
three cevians from the vertices of a nondegenerate triangle are concurrent exactly when a cyclic
product of ratios cut on the opposite sides is one. The catalog itself says only `共点线的比例关系`;
it supplies no variables, formula, direction, or boundary convention. Intake therefore preserves
the family without silently choosing a proposition.

For an ordered mathlib triangle `t`, a prospective side-point family `p : Fin 3 -> P` maps index
`i` to the line through vertices `i + 1` and `i + 2`. A common point `p'` on the line through
vertex `i` and `p i` expresses concurrency. Under the usual `A, B, C` ordering, the pinned metric
quotient expands cyclically to `BD / DC * CE / EA * AF / FB = 1`. This is a discovery crosswalk,
not a frozen binder list or statement.

## Decisions required at statement freeze

1. Preserve and independently review an authoritative source edition, exact proposition,
   incorporated definitions, proof boundary, translation, correction, and errata status.
2. Decide whether the root is concurrency implies the ratio identity, the converse, or an iff.
   The inspected human lead states an iff; the located pinned Lean declarations prove only the
   concurrency-to-ratio direction.
3. Fix the ratio convention: directed affine ratios, unsigned metric distances, or a cross-product
   equality. Specify the cyclic order, reciprocal convention, and sign when a point is exterior.
4. Fix whether `D`, `E`, and `F` lie on closed side segments, open sides, or full supporting lines.
   The pinned declarations use complete affine lines and do not impose betweenness.
5. Fix the ambient domain: the real Euclidean plane, a two-dimensional real affine inner-product
   space, a more general normed affine torsor, or an algebraic affine space over a field.
6. Fix nondegeneracy and every denominator condition. Mathlib's `Affine.Triangle` bundles affine
   independence; the quotient forms add nonzero restrictions but the cross-product forms do not.
7. Decide whether concurrency means existence of a supplied finite point, pairwise line
   intersection, or projective concurrency including a point at infinity.
8. Fix ordered binders, universes, namespaces, options, foundation/TCB profiles, and every credited
   transport before expression hashing and mutation tests.

## Boundary cases to resolve

- repeated or collinear triangle vertices and a zero-area triangle;
- a side point equal to either adjacent vertex, causing a zero numerator or denominator;
- two side points or a concurrency point equal to a triangle vertex;
- external side points, sign changes, and whether unsigned distances still express the intended
  theorem;
- cevians that coincide with triangle sides, are pairwise parallel, or meet only projectively;
- existence and uniqueness of a concurrency witness versus merely accepting one as a binder;
- general affine dimension versus an actual two-dimensional Euclidean plane;
- reversing the triangle orientation, cyclic relabeling, or using reciprocal ratios.

No case is excluded at intake. A later source-approved statement must include each admitted case or
state and justify its exclusion.

## Candidate encodings, not credited statements

| Candidate | Relationship to the catalog | Intake boundary |
|---|---|---|
| `Affine.Triangle.prod_dist_div_dist_eq_one_of_mem_line_of_mem_line` | direct unsigned-distance quotient from concurrency | forward only; full sidelines; denominator endpoint exclusions; generic normed affine domain |
| `Affine.Triangle.prod_dist_eq_prod_dist_of_mem_line_of_mem_line` | division-free distance cross-product | forward only; sign is erased; no converse or segment condition |
| `Affine.Triangle.prod_div_one_sub_eq_one_of_mem_line_point_lineMap` | directed affine-coordinate quotient | forward only; coordinate weights need a checked geometric ratio transport |
| `Affine.Triangle.prod_eq_prod_one_sub_of_mem_line_point_lineMap` | division-free algebraic product | close to a directed-ratio cross multiplication; exact source mapping open |
| Thomas Prince, Theorem 1 | explicit Euclidean iff with a signed-length extension to produced sidelines | inspected source lead only; catalog identity, preservation, errata mapping, and independent review open |

The generalized `AffineIndependent.exists_affineCombination_eq_smul_eq` declarations are useful
proof architecture and provenance leads. They broaden beyond a triangle and cannot replace the
canonical root.

## Excluded substitutions

- the forward pinned theorem used as if it also proved the converse or an iff;
- the converse or an iff silently selected merely because it is a common textbook formulation;
- unsigned metric distances used for external side points without resolving the signed-ratio
  convention;
- a theorem only about interior medians, angle bisectors, or one numerical triangle;
- Menelaus's theorem (`THM-M-0199`), trigonometric Ceva, mass points, Routh's theorem, or a
  higher-dimensional simplex generalization used as the root;
- an affine coordinate determinant without checked point, line, ratio, and concurrency transports;
- a premise, structure field, axiom, oracle, diagram, or certificate containing the desired product
  identity or converse;
- a catalog label, citation, theorem name, API probe, or successful import treated as proof credit.

## First downstream gate

The statement phase must admit one independently reviewed source proposition, resolve every choice
above, elaborate exactly that proposition with minimal pinned imports, preserve its normalized
expression and environment fingerprint, compile all credited transports, and run the required
removed-hypothesis, changed-domain, binder-scope, and boundary mutations. Until then the canonical
expression, obligation registry, and proof credit remain empty.
