# Scope map

## Received scope

The repository fixes only the title `零和序列`, the collective attribution `众多数学家`, the period
`20世纪`, and the gloss `零和问题的理论`. It gives no bibliography, definition, ordered binders,
hypotheses, conclusion, proof, correction history, or formal artifact. Stage0 repeats the gloss and
explicitly leaves the formal system, exact definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine state, and artifact links open. The `已验证` label is untrusted
metadata.

The natural English subject translation is "zero-sum sequences." That translation identifies a
field, not a theorem. It does not determine which group, sequence representation, invariant,
threshold, length restriction, structure conclusion, or inverse result is intended.

## Candidate mathematical families

An eventual source-approved target could concern one of the following, but none is asserted or
credited at intake:

- existence of a nonempty zero-sum subsequence under a length hypothesis;
- the Davenport constant, its finiteness, value, bounds, or extremal sequences;
- the Erdos-Ginzburg-Ziv constant or another prescribed-length zero-sum threshold;
- Olson constants or subset-sum variants;
- zero-sum-free or minimal zero-sum sequence structure and inverse theorems; or
- block monoids and factorization invariants derived from zero-sum sequences.

These have different domains, binders, hypotheses, conclusions, boundary cases, and proof
architectures. A definition of zero-sum sequence cannot be substituted for a theorem about the
subject.

## Proposition-changing decisions

Before the statement phase can freeze a canonical claim, an accepted source and independent
reviewer must fix:

1. The algebraic carrier: finite abelian group, cyclic group, general additive commutative group,
   monoid, or another precisely sourced class, including finiteness and decidable-equality needs.
2. The sequence encoding: `List`, `Multiset`, finitely supported multiplicity function, free
   abelian monoid element, or an indexed family, with checked transports for any credited alternate.
3. The subsequence relation and multiplicity policy: order-preserving list subsequence,
   submultiset, selected indices, or support subset; repetitions must not be silently discarded.
4. Whether zero-sum means the whole sequence sums to the additive identity, and whether the empty
   sequence counts; an existence conclusion must state nonemptiness or prescribed cardinality.
5. The exact theorem family: unconstrained or prescribed-length existence, zero-sum-free or minimal
   structure, Davenport/EGZ/Olson invariant, optimal bound, inverse theorem, or factorization result.
6. The definition and codomain of every invariant, including whether infinity is possible and
   whether a least threshold, supremum, or maximum is asserted.
7. The ordered quantifiers, dependencies, inequalities, strictness, optimality witnesses, universe
   levels, foundation profile, computation policy, and exact conclusion.
8. The relationship to the separately cataloged EGZ and Olson targets, so no theorem or proof body
   receives duplicate ownership or credit.

## Boundary and degenerate cases

No case is excluded before a proposition is selected. Source review must decide the trivial group;
an empty sequence; a sequence containing the zero element; singleton and repeated-term sequences;
the empty, full, and proper subsequence distinctions; prescribed length zero or one; cyclic modulus
zero or one if `ZMod n` is used; sequences shorter than a threshold; equality at the threshold;
and whether invariant definitions over groups outside the finite class take an infinite value.

These choices are material. Because the empty multiset has sum zero, an encoding that omits a
nonempty or positive-cardinality condition can trivialize an intended existence theorem.

## Neighboring target boundaries

- `THM-M-0931` owns the Erdos-Ginzburg-Ziv theorem: among sufficiently many integers or residues,
  a prescribed-size subsequence has sum divisible by the size/modulus. Its pinned mathlib proof
  supplies no statement identity or proof credit here.
- `THM-M-0933` owns the catalog's Olson/Davenport-constant result family. An Olson theorem or a
  Davenport-constant formula cannot silently become this generic root.
- `THM-M-0930` owns combinatorial Nullstellensatz and `THM-M-0936` owns Cauchy-Davenport. They may
  become proof dependencies for a future exact proposition but cannot select it by proximity.

Also excluded are one finite example, a cyclic-group special case, an unchecked exhaustive search,
or a structure/hypothesis that stores the requested zero-sum subsequence or optimal bound.

## Lean boundary

Pinned mathlib provides additive group APIs, multiset cardinality and sum, finite indexed sums, and
the four public EGZ declarations. A bounded exact-topic search found no declaration named for the
broad zero-sum-sequence subject, Davenport constant, or Olson constant. `IntakeProbe.lean`
authenticates only this substrate and excluded neighbor. It defines no zero-sum predicate,
canonical theorem, source transport, or proof body. Exhaustive candidate and terminal-provenance
auditing belongs to the later anchor-audit phase.

## Retry condition

Select a lawful immutable primary or approved authoritative edition and one pinpoint proposition;
record all incorporated definitions, complete binders, hypotheses, conclusion, proof boundary,
corrections, and boundary conventions; reconcile neighboring target ownership; and obtain
independent source review. A later statement phase may then encode exactly that proposition,
minimize pinned imports, serialize its expression and environment, check every credited transport,
and run all four required statement-mutation classes.
