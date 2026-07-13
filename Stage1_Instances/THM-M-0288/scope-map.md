# Scope map

## Received claim

`Docs/researches/math_theorems.md` supplies only the title "Vitali covering theorem" and the gloss
"covering lemma and differentiation theorem." This is a compound theorem-family description, not a
truth-valued proposition. This intake freezes the ambiguity and the choices that the statement
phase must make; it does not invent a canonical theorem.

## Candidate covering boundaries

Several materially different claims are commonly associated with the name:

- a finite or countable interval-cover selection theorem in Euclidean space;
- a metric-ball selection lemma extracting a disjoint subfamily whose fixed dilations cover the
  original family or its centers;
- a measurable theorem extracting a countable pairwise-disjoint fine subfamily covering a set
  almost everywhere;
- a Vitali relation/family axiom packaging fine coverings and almost-everywhere disjoint extraction;
- a covering theorem specialized to a doubling measure.

The source review must fix the ambient set, dimension or metric space, centers and radii, boundedness
or fineness condition, open/closed/measurable set convention, dilation constant, countability,
coverage target, and whether the conclusion is literal coverage or coverage modulo a null set.

## Candidate differentiation boundaries

The catalogue also names a "differentiation theorem," which may mean:

- differentiation of one locally finite measure with respect to another;
- the Lebesgue density theorem for measurable or arbitrary sets;
- differentiation of an integral or convergence of local averages for a scalar function;
- the vector-valued Lebesgue differentiation theorem;
- a special Euclidean balls/cubes result or an abstract Vitali-family result.

These conclusions have different binders, regularity assumptions, codomains, filters, null-set
statements, and dependencies. The statement phase must also decide whether differentiation is the
root, a required consequence of the covering theorem, or merely contextual prose.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Vitali.exists_disjoint_subfamily_covering_enlargement_closedBall` is a topological closed-ball
  selection theorem on a pseudo-metric space. It assumes uniformly bounded radii and `3 < tau` and
  covers every input closed ball by a `tau`-dilation of a selected disjoint ball.
- `Vitali.exists_disjoint_covering_ae` is a measurable result. Under second-countability,
  local-finiteness, closedness, nonempty interiors, a proportional measure bound, and fineness, it
  returns a countable pairwise-disjoint subfamily covering the target set almost everywhere.
- `Vitali.vitaliFamily` packages suitable closed sets under a small-scale doubling condition as a
  `VitaliFamily`.
- `VitaliFamily.ae_tendsto_rnDeriv` differentiates locally finite measures along an arbitrary Vitali
  family, almost everywhere.
- `VitaliFamily.ae_tendsto_average_norm_sub` and `VitaliFamily.ae_tendsto_average` are Lebesgue
  differentiation statements for locally integrable functions.

These are strong exact-topic formal candidates, hence provisional `M3` rather than `M4`. None is
`M0`: source-root selection, normalized expression identity, a checked transport or composition,
terminal proof-body provenance, trust policy, and node-specific accepted receipts remain downstream.

## Required statement decisions

1. Admit an immutable authoritative source and pinpoint the exact theorem, incorporated definitions,
   proof boundary, translation, corrections, and errata.
2. Decide whether the catalogue intends one covering proposition, one differentiation proposition,
   or a two-node bundle with an explicit implication/composition edge.
3. Freeze all ambient spaces, universes, topological and measurable structures, measures, families,
   centers, radii, constants, fineness conditions, ordered binders, and hypotheses.
4. Freeze whether coverage is finite/countable, disjoint/pairwise-disjoint, literal/almost-everywhere,
   and of the original family, centers, or target set.
5. If differentiation is included, freeze the differentiated measure/function, local integrability,
   scalar field/codomain, limiting filter, exceptional-set measure, and exact limit.
6. Classify each pinned declaration as the canonical target, a checked alternate encoding, a child
   obligation, or only a discovery anchor; compile every credited relationship witness.
7. Resolve empty families and sets, zero or infinite measures, nonpositive radii, zero-measure
   averaging sets, non-doubling spaces, and failures of second countability or local finiteness.

## Explicit exclusions

- Vitali convergence/uniform-integrability and Vitali-Caratheodory approximation theorems.
- Besicovitch covering silently substituted for Vitali covering.
- A finite-family or one-dimensional interval special case used as an unrestricted root.
- A metric-ball `5r`-style selection lemma silently substituted for measurable a.e. extraction, or
  conversely.
- A density-point, Radon-Nikodym, or function-average result silently substituted for the covering
  theorem, or included without a checked root relationship.
- A `VitaliFamily` value whose defining covering property is assumed as data used as proof of the
  source covering theorem.
- The untrusted `已验证` label, theorem-name match, source URL, or intake probe used as proof credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion, checked alternate encoding,
or degenerate-case exclusion is frozen by this intake.
