# Scope map

## Preserved theorem family

The intake preserves only the catalog's recognizable boundary: a comparison theorem for the
numbers of zeros of complex holomorphic functions associated with Rouché and 1862. A common source
family uses two functions regular within and on a closed contour, a strict domination inequality
on that contour, and equality of the interior zero counts. This description is a candidate family,
not an accepted canonical proposition.

## Decisions required at statement freeze

1. Select a lawful immutable primary or authoritative source and pinpoint the exact theorem,
   incorporated definitions, proof passage, corrections, errata, and independent review.
2. Fix the geometric object: a circle and disk, a Jordan curve and its interior, the boundary of a
   bounded domain, or another source-defined contour-region pair, including orientation and which
   components count as "inside."
3. Fix contour regularity and domain hypotheses: simple versus possibly self-intersecting, closed,
   piecewise smooth or rectifiable; compactness and boundedness; and openness or connectedness of
   the surrounding complex domain.
4. Fix analytic regularity: holomorphic on a neighborhood of the closure, holomorphic in the
   interior plus continuous on the boundary, or another exact condition. Decide whether both
   functions share the same regularity and ambient domain.
5. Freeze the compared functions and inequality. Candidate conventions include `|g| < |f|` with
   zero counts of `f` and `f + g`, or `|f - g| < |f|` with zero counts of `f` and `g`. These require
   a checked renaming/subtraction transport, not a name match.
6. Define the zero count: finite set cardinality versus a sum of analytic orders, treatment of
   multiplicity, the exact interior set, finiteness hypotheses or derived finiteness, and the
   identically-zero case.
7. Resolve whether nonvanishing of the dominant function on the boundary is explicit or derived
   from the strict inequality, and prohibit zeros of either compared function on the contour as
   required by the selected statement.
8. Resolve zero-radius or empty contours, empty interiors, constant and identically-zero functions,
   zero perturbation, equality rather than strict inequality, disconnected domains, and other
   boundary cases.
9. Reconcile the ownership boundary with `THM-M-0234` before either ID receives statement or proof
   credit for the same mathematical root.

## Candidate branches not credited

- The general closed-contour or Jordan-domain theorem comparing `f` with `f + g`.
- The difference form comparing `f` and `g` under `|f - g| < |f|`.
- A disk/circle specialization using `Metric.ball`, `Metric.closedBall`, and `Metric.sphere`.
- A homotopy or winding-number formulation whose equivalence to a zero-count theorem is checked.
- A divisor-sum formulation using local vanishing orders and a finite-support proof.

No branch is selected, asserted, or credited at intake.

## Explicit exclusions

- `THM-M-0233` (the argument principle) as a substituted root; it may later be a bridge obligation.
- `THM-M-0234` (`儒歇定理`) or any of its future artifacts until duplicate-scope ownership is
  independently resolved; no evidence transfers between IDs.
- A polynomial-only, disk-only, or one-zero corollary presented as the general theorem without a
  checked reduction from the accepted root.
- Equality of winding numbers or contour integrals without a checked argument-principle and
  multiplicity bridge to the selected zero count.
- A finite sample of boundary points, numerical root count, floating-point contour integral,
  plot, oracle, or unchecked certificate.
- A hypothesis or structure field that directly assumes the desired equality of zero counts.
- The catalog's `已验证` label, the theorem name, a source lead, or adjacent API elaboration as H0
  or M0 evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides `analyticOrderAt`,
`analyticOrderNatAt`, `meromorphicOrderAt`, `MeromorphicOn.divisor`, nonnegativity of divisors for
analytic functions, and circle-integral Cauchy interfaces. A bounded case-insensitive search of
repo-local Lean and pinned mathlib found no declaration named for Rouché's theorem and no literal
`argument principle` occurrence. This is intake discovery only, not the required downstream
inventory, provenance audit, or global absence claim.
