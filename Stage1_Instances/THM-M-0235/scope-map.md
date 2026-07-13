# Scope map

## Received claim

`Docs/researches/math_theorems.md:1696-1701` fixes only the title `开映射定理`, the attribution
"many mathematicians," the nineteenth century, and the gloss `非常值全纯函数是开映射`
("nonconstant holomorphic functions are open maps"). It supplies no bibliographic source,
definitions, exact hypotheses, theorem locator, proof boundary, or formal artifact.

The complex-analysis category and the literal holomorphic-function wording identify the classical
complex open mapping family. They exclude the separately cataloged Banach-space open mapping
theorem `THM-M-0276`, whose source claim concerns surjective bounded linear operators.

## Candidate classical boundary

A familiar domain form says that a nonconstant holomorphic function on a connected open subset of
the complex plane maps each open subset of its domain to an open subset of the complex plane. This
is a scope description only. The statement phase must source and fix:

1. Whether the domain is an explicit set `U : Set ℂ`, a subtype, a source-defined "domain," or the
   whole complex plane.
2. Whether nonemptiness, openness, and connectedness are explicit premises or carried by a domain
   definition, and whether connectedness is represented by `IsConnected U` or by separate
   nonemptiness and `IsPreconnected U` data.
3. Whether holomorphicity is encoded as `DifferentiableOn ℂ f U`, `AnalyticOnNhd ℂ f U`, or
   another source-faithful predicate, together with checked equivalence on an open set.
4. Whether nonconstancy means `¬ ∃ w, ∀ z ∈ U, f z = w`, existence of two points in `U` with
   unequal images, or a total-function predicate. These differ on the empty domain and outside U.
5. Whether "open map" is the relative-domain result
   `∀ s ⊆ U, IsOpen s → IsOpen (f '' s)`, an `IsOpenMap` on the subtype restriction, or the total
   predicate `IsOpenMap f`. The last speaks about every open subset of all `ℂ` and is justified
   directly only for the whole-domain form.
6. The ordered binders, exact codomain, universe and topology instances, conclusion, foundation
   profile, and every alternate encoding with a checked transport.

## Boundary cases

The exact source crosswalk must resolve the empty set, singleton and disconnected sets, the whole
plane, constant functions, functions constant on one connected component but not globally,
functions holomorphic only on a neighborhood of `U`, the empty open subset, `s = U`, and behavior
outside `U`. In particular, preconnectedness alone permits the empty domain, where the constant
disjunct in mathlib is vacuously true; an ordinary source convention for "domain" may already
exclude this case.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the direct candidate
`AnalyticOnNhd.is_constant_or_isOpen` has the shape

```text
AnalyticOnNhd ℂ g U -> IsPreconnected U ->
  (exists w, forall z in U, g z = w) or
  forall s subset U, IsOpen s -> IsOpen (g '' s).
```

The corollary `AnalyticOnNhd.is_constant_or_isOpenMap` specializes to `U = Set.univ` and concludes
the total predicate `IsOpenMap g`. The local declaration
`AnalyticAt.eventually_constant_or_nhds_le_map_nhds` supplies a neighborhood-level alternative.
On open complex sets, pinned Cauchy-integral APIs connect complex differentiability with
`AnalyticOnNhd`; that bridge is a downstream statement obligation, not an intake inference.

These are strong exact-topic interfaces, hence provisional `M3`. Their names and successful
elaboration do not establish source identity, choose the canonical target, audit terminal bodies,
or supply root proof credit.

## Explicit exclusions

- `THM-M-0276`, the Banach open mapping theorem for surjective bounded linear operators.
- The whole-domain theorem for entire functions unless a checked specialization is explicitly
  selected from a source-faithful domain statement.
- Only the local neighborhood alternative, inverse or implicit function theorem, maximum modulus
  principle, identity theorem, isolated-zero theorem, or a polynomial special case.
- A theorem for one connected component when the accepted root quantifies over the entire domain.
- A structure or premise that stores openness or the desired conclusion.
- A theorem name, source URL, `#check`, untrusted `已验证` label, or API probe as H0 or M0 evidence.
