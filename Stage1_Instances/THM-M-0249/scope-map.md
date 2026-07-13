# Scope map

## Preserved theorem family

The intake preserves exactly the catalog's Mergelyan polynomial-approximation family. The standard
reading concerns a compact set `K` in the complex plane whose complement is connected and a
complex-valued function continuous on `K` and holomorphic on `interior K`; the conclusion is
uniform approximation on `K` by complex polynomials. This is a source lead and scope description,
not the frozen canonical proposition.

## Decisions required at statement freeze

An approved source and independent review must settle all of the following before a Lean target is
credited:

1. Whether `K` is a `Set Complex`, a bundled compact subset, or an equivalent subtype, and whether
   compactness is a hypothesis, a typeclass, or built into the carrier.
2. Whether connected complement means `IsConnected Kᶜ`, nonempty plus `IsPreconnected Kᶜ`,
   connectedness in the complex plane, or connectedness in the Riemann sphere, with a checked
   equivalence for any alternate encoding.
3. Whether `f` is a function `Complex -> Complex` with `ContinuousOn f K`, a bundled continuous map
   on the subtype `K`, or another exactly transported representation.
4. Whether "holomorphic on the interior" is encoded by `DifferentiableOn Complex f (interior K)`,
   `AnalyticOnNhd Complex f (interior K)`, or a source-faithful equivalent predicate.
5. Whether approximation is expressed pointwise with `forall z in K`, by a supremum norm on
   continuous maps, by closure/density of polynomial restrictions, or by a sequence converging
   uniformly; all credited forms require checked transports.
6. The quantifier order for `f`, positive `epsilon`, and `p : Polynomial Complex`, the use of
   strict versus non-strict error, and the exact polynomial evaluation function.
7. All ordered binders, universes, coercions, typeclass assumptions, foundation profile, and the
   relation between the human claim and every formal encoding.

These are proposition-changing choices. Intake records them rather than deciding them from memory.

## Degenerate and boundary cases

Source review must explicitly resolve the empty compact set; singletons and finite sets; empty
interior; the whole complement; disconnected `K` with connected complement; compact sets with
holes; constant and zero functions; constant polynomials; positive, zero, and negative error;
whether an empty interior makes the holomorphic condition vacuous; and whether the complement's
nonemptiness is included in the connectedness predicate. No case is excluded at intake.

## Candidate formulations not credited

- The epsilon formulation for compact `K : Set Complex`, connected `Kᶜ`, continuous `f` on `K`,
  holomorphic `f` on `interior K`, and a complex polynomial uniformly within each positive error.
- Density of restrictions of holomorphic polynomials in the algebra `A(K)` of continuous functions
  on `K` holomorphic on its interior.
- A sequence of complex polynomials converging uniformly on `K` to `f`.
- The equivalent no-hole formulation through holomorphic extension over bounded components of the
  complement.

These readings guide later source review. None is selected, asserted, or machine-credited here.

## Excluded substitutions

- Real Weierstrass approximation on an interval does not prove complex polynomial approximation on
  arbitrary compact planar sets.
- Complex Stone-Weierstrass with the star closure includes complex conjugation; it approximates all
  continuous functions and is not Mergelyan's holomorphic-polynomial theorem.
- Runge approximation by rational functions, approximation by holomorphic functions on a
  neighborhood, Bishop's rational-approximation criterion, Lavrentiev's empty-interior special
  case, and zero-free polynomial approximation are distinct results.
- A theorem for disks, intervals, Jordan domains, finite sets, or empty-interior compacta alone is
  only a special case.
- Omitting connected complement or interior holomorphicity makes the usual universal polynomial
  approximation claim false; the catalog's shorter gloss cannot be formalized literally.
- A structure storing an approximating polynomial, a numerical fit, a theorem name, or the
  `已验证` label supplies no proof credit.

## Neighbor and formal boundaries

`THM-M-0248` separately owns Bishop's rational-approximation theorem and `THM-M-0265` separately
owns real Weierstrass approximation. They may later contribute typed dependencies but grant no
status by proximity. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks only adjacent topology, complex
analysis, polynomial, and continuous-map APIs. The bounded search is intake discovery, not an
exhaustive anchor audit or a proof of global absence.
