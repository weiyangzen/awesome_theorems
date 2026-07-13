# Scope map

## Preserved repository scope

The complete catalog record fixes only the title `介值定理`, Bernard Bolzano, the year 1817, the
gloss `连通空间上连续函数的值域`, high importance, and an untrusted `已验证` label. The
point-set-topology category, execution rank, intake score, and lane are scheduling metadata. They
add no mathematical assumptions.

The title and attribution make the ordered intermediate-value family the leading interpretation:
a continuous function on a connected or preconnected domain takes every value between suitable
endpoint values. The literal gloss is not itself truth-valued and also describes continuous-image
connectedness. This intake records the leading interpretation without promoting it to a canonical
statement.

## Proposition-changing decisions

An approved source review must freeze:

- whether the theorem says that a continuous image is connected, or that an ordered codomain image
  contains every value between two attained values;
- whether the domain is a connected space, a preconnected space, a connected set, a preconnected
  set, or a real closed interval;
- whether the codomain is `Real` or a more general linearly ordered topological space, including
  the exact order/topology compatibility assumptions;
- whether continuity is global, on a selected set, or only on a closed interval;
- the ordered binders for the domain, codomain, set, function, endpoints, and intermediate value;
- endpoint membership, endpoint order, value orientation, and whether both orientations or an
  unordered interval are included;
- the exact conclusion: connected image, interval inclusion in the image/range, an existential
  preimage for one intermediate value, or existence of a zero under sign assumptions;
- equality cases, empty and singleton domains, equal endpoints, constant functions, and other
  boundary cases; and
- the historical/modern source relationship, incorporated definitions, translation, proof
  boundary, corrections or errata, and independent review.

These choices are not harmless Lean notation. They produce propositions of different generality
and sometimes different mathematical content.

## Candidate families not credited

1. For arbitrary topological spaces, the continuous image of a connected set is connected.
2. For a preconnected set and ordered codomain, all values between two attained endpoint values
   occur in the image.
3. For a preconnected whole space and ordered codomain, the interval between `f a` and `f b` lies
   in the range of a continuous function.
4. For a continuous function on a closed or unordered interval, every value between its endpoint
   values occurs on that interval.
5. For a real continuous function with opposite-sign endpoint values, some point is a zero.

No item in this list is the canonical statement until source and scope review selects it and maps
all assumptions.

## Degenerate and mutation scope

The statement phase must decide empty versus nonempty domains, connected versus merely
preconnected carriers, equal endpoints, reversed endpoint order, equal or reversed endpoint
values, constant functions, endpoints already realizing the queried value, singleton images, and
zero exactly at an endpoint. It must also mutation-test removal of connectedness/preconnectedness
and continuity, a changed domain or codomain, changed binder scope, and the selected boundary
cases. Intake silently excludes none of them.

## Neighbor and substitution exclusions

- `THM-M-0626` separately catalogs `连通集的连续像连通`. Its statement, evidence, and status
  cannot be inherited. The overlap is evidence that the literal THM-M-0634 gloss needs a reviewed
  order-theoretic identity decision, not permission to merge the targets.
- `THM-M-1442` separately owns the bisection-method family. Intermediate-value root existence
  supplies no bisection recurrence, invariant, convergence, rate, or solver-correctness credit.
- A theorem restricted to `Real`, one interval, polynomial functions, or a sign-changing zero
  cannot replace a more general connected-space claim without source-approved implication or
  equivalence evidence.
- The connected-image theorem, an order-convex image theorem, endpoint existence, and a root
  corollary cannot be interchanged merely because textbooks group them under "intermediate value."
- A hypothesis or structure field containing the desired witness, the catalog's verified label,
  or a successful API probe supplies no theorem proof.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, direct candidate
interfaces include `IsConnected.image`, `IsPreconnected.intermediate_value`,
`intermediate_value_univ`, `intermediate_value_Icc`, `intermediate_value_Icc'`, and
`intermediate_value_uIcc`. They span more than one candidate scope. Their availability confirms
formal feasibility and sharpens the ambiguity, but it does not establish source identity.

No canonical Lean proposition, minimal import set, elaborated expression, environment fingerprint,
checked alternate encoding, discovery protocol, obligation registry, or proof-body credit is
frozen at intake. Those are downstream gates.
