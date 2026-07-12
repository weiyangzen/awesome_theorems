# Scope map

## Frozen repository scope

- Label: Woodward theorem (`伍德沃德定理`).
- Period: twentieth century.
- Attribution: only the non-identifying phrase "many mathematicians".
- Literal claim: a result in cobordism theory.
- Inventory category: topology / algebraic topology.

These fields are the entire theorem-specific source content found in the repository. They establish
a discovery topic, not a mathematical proposition. In particular, the label supplies no domain,
quantifiers, assumptions, invariant, equivalence relation, or conclusion.

## Identity gate

Before statement freeze, a stable primary source must establish all of the following: the author's
full identity; publication title, edition or journal data, year, theorem and page; the precise use
of the name "Woodward theorem" or a documented attribution crosswalk; and the theorem's connection
to the repository phrase "cobordism theory." A secondary index may help locate that source but
cannot by itself satisfy this gate.

If the Chinese or English name is a mistranslation, the correction must be evidenced and reviewed;
it must not be silently replaced by a better-known cobordism theorem. If no unique source can be
recovered, the target remains blocked at statement rather than being assigned an invented claim.

## Decisions required after identification

The selected source must fix the geometric category (smooth, topological, PL, or another setting),
compactness and boundary conventions, dimension, orientation or tangential structure, the exact
cobordism relation, coefficient rings and characteristic data, and whether the conclusion is an
existence statement, classification criterion, group/ring computation, or correspondence. It must
also settle connectedness, empty objects, degenerate dimensions, and equality versus equivalence.
Lean universes, binder order, quotient/setoid encoding, classical assumptions, and computation
profile must follow those choices.

## Explicit exclusions

- Thom's cobordism classification, Pontryagin-Thom, h-cobordism, s-cobordism, or the cobordism
  hypothesis merely because each is a known result involving cobordism.
- A weaker invariant direction when the recovered source states a complete classification.
- An abstract structure that contains the desired conclusion as assumed data.
- A theorem selected only because a search result contains the surname Woodward.
- The repository label `已验证` as evidence of a human proof or kernel-checked formalization.

A later Lean target must expose the concrete notions used by the recovered source. Missing mathlib
infrastructure must be recorded as a blocker, never hidden in theorem hypotheses.
