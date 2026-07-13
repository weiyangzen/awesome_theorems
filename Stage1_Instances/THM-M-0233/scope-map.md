# Scope map

## Preserved theorem family

The intake preserves target `THM-M-0233`, the argument principle, and the catalog gloss that
relates zeros and poles of a complex function. The inspected DLMF equation identifies the
recognizable full family: a signed multiplicity count, a normalized contour integral of the
logarithmic derivative, and a normalized phase change along a positively oriented contour. These
are candidate clauses to crosswalk, not an accepted canonical proposition.

## Proposition-changing decisions

Before the statement phase can freeze a root, an immutable source and independent review must fix:

- whether `f` is meromorphic on a neighborhood of the contour and its interior, analytic except
  for finitely many poles, or described through another equivalent source definition;
- the ambient complex domain and whether the theorem is planar or includes the point at infinity;
- whether `C` is a positively oriented simple closed piecewise-smooth contour, a circle, a Jordan
  curve, or a general cycle, and the precise definition of its interior;
- whether finiteness of enclosed zeros and poles is assumed or derived, and how orders and
  multiplicities are encoded;
- the boundary requirements, including absence of zeros and poles on `C` and any continuity or
  differentiability requirement inherited from the contour integral;
- whether the canonical conclusion includes the integral equality, the phase-change or winding
  equality, or the conjunction, and the exact sign and normalization conventions;
- all ordered binders, typeclass context, hypotheses, and conclusion dependencies; and
- treatment of the zero function, nonzero constants, no enclosed zeros or poles, repeated or
  reversed traversal, self-intersection, radius zero, boundary singularities, and poles at
  infinity.

The catalog word `全纯` (holomorphic) is not silently corrected to `亚纯` (meromorphic). The exact
source phase must explain whether it is loose terminology, a holomorphic zero-count specialization,
or a punctured-domain formulation that still admits poles.

## Candidate encodings not credited

1. A general contour theorem equating the signed divisor sum in the bounded component of a Jordan
   contour with the normalized integral of `logDeriv f`.
2. The same theorem with a winding number or continuous phase-change clause for `f` composed with
   the contour.
3. A circle-only theorem using `circleIntegral`, closed balls, and mathlib's meromorphic divisor.
4. A holomorphic specialization counting zeros only, with pole count zero.

These formulations have different domains and conclusions. No one of them is selected at intake.

## Explicit exclusions

- A circle-only, polynomial-only, rational-function-only, or holomorphic-zero-only special case
  presented as the full contour theorem.
- Jensen's formula, the residue theorem, Rouché's theorem, or the fundamental theorem of algebra
  substituted for the argument principle.
- A formula that counts zeros but omits poles, multiplicities, or required boundary hypotheses.
- A reversed sign or orientation convention without a checked source-faithful transport.
- A phase/winding statement substituted for the integral formula, or conversely, when the selected
  source root contains both.
- A structure or hypothesis storing the desired count identity and then projecting it.
- A numerical contour integral, plotted image curve, sampled phase unwrap, or unchecked winding
  certificate.
- The untrusted `已验证` label, an API typecheck, or a bounded no-match search as H0 or M0 evidence.

## Neighbor boundaries

`THM-M-0223` (residue theorem) is a likely proof ingredient but is a distinct root relating a
contour integral to residues. `THM-M-0232` and `THM-M-0234` are separate Rouché-related catalog
targets about stability or comparison of zero counts. None supplies source identity or proof credit
for this target.

## Formal boundary

Pinned mathlib has real adjacent substrate: `meromorphicOrderAt`, `MeromorphicOn.divisor`,
`logDeriv`, `MeromorphicOn.logDeriv`, `circleIntegral`, and
`MeromorphicOn.circleAverage_log_norm`. The bounded exact-topic search found no named terminal
argument-principle theorem or winding-number interface. This is discovery-only evidence, not the
later exhaustive anchor audit. No minimal import set, canonical expression, expression fingerprint,
checked transport, mutation result, discovery freeze, obligation freeze, graph, or proof state is
claimed.
