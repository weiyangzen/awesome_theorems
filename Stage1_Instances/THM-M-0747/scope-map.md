# Scope map

## Preserved theorem family

The target is computability-theoretic simple-set existence. A later statement phase may freeze the
root only after an immutable source passage and independent review settle the exact formulation.
The intended family has these material components:

- a predicate or set `A` on the natural numbers;
- computable enumerability of `A`;
- infinitude of the complement of `A`;
- immunity of that complement, meaning it has no infinite computably enumerable subset; and
- an existential conclusion producing at least one such `A`.

The last two conditions can prospectively be expressed as: for every predicate `W`, if `W` is
computably enumerable and its extension is infinite, then some natural number satisfies both `W`
and `A`. That intersection form requires a checked equivalence before it can be credited as an
alternate encoding.

## Decisions required at statement freeze

1. Pinpoint the primary definition and existence result in an immutable edition, including page,
   surrounding notation, assumptions, proof boundary, correction history, and independent review.
2. Decide whether the canonical object is `A : Nat -> Prop` or `A : Set Nat`, and record the checked
   transport between them.
3. Select the exact computable-enumerability model: mathlib `REPred`, an enumeration/range model,
   a partial-function domain, or another source-mapped representation.
4. Fix whether "immune" includes infinitude as part of its definition or whether infinitude is a
   separate conjunct, and ensure it applies to the complement rather than to `A` itself.
5. Freeze the ordered quantifiers in the no-infinite-c.e.-subset form or the every-infinite-c.e.-set-
   meets-`A` form, including any decidability or encoding instances introduced by Lean.
6. State all boundary conventions: empty and finite candidate sets, finite complements, empty or
   finite test predicates, equality/extensionality of predicates, and positive-integer versus
   natural-number indexing.
7. Determine the accepted foundation policy for classical logic, choice, predicate extensionality,
   and the computability library's coding infrastructure.

## Explicit exclusions

- The algebraic-topology notion of a simplicial set; the repository category and provenance rule it
  out despite a possible Chinese-language ambiguity.
- Merely proving that a noncomputable computably enumerable set exists. That is a consequence or
  weaker neighboring gloss, not simple-set existence.
- Existence or properties of creative, productive, maximal, hypersimple, hyperhypersimple, or
  effectively immune sets without an approved equivalence or specialization.
- Post's problem about an intermediate Turing degree, Friedberg-Muchnik incomparability, or a claim
  about many-one completeness. These are neighboring but distinct roots.
- Defining `Simple A` as a structure field that already assumes the desired witness and then
  projecting the field as the proof.
- Treating `REPred`, the halting problem, or generic set infinitude as a formal anchor for the root.
- Treating `已验证`, a DOI, or bibliographic metadata as human-proof or Lean kernel evidence.

No canonical Lean target, statement fingerprint, checked alternate encoding, obligation registry,
discovery protocol, proof state, or completion claim is frozen at intake.
