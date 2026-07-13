# Scope map

## Preserved catalog scope

The intake preserves the catalog's functional-analysis theorem family: a pointwise bounded family
of continuous linear operators is uniformly bounded in operator norm. The literal Chinese gloss
only says "uniform boundedness of an operator family"; the conventional premise, completeness
assumption, and quantifier scopes come from identification of the named theorem and source/formal
leads, not from a binder-complete catalog proposition.

A likely modern root, not yet credited as canonical, says: let `E` be a Banach space, `F` a normed
space over a common scalar field, and `(T_i)_(i in I)` an arbitrary family of continuous linear
maps `E -> F`. If for every `x : E` there exists a real `C_x` such that
`norm (T_i x) <= C_x` for every `i`, then there exists a real `C` such that
`norm (T_i) <= C` for every `i`.

This candidate includes empty `I` and zero spaces. The pointwise bound may depend on `x`; the
conclusion's bound may not depend on `i`. Completeness belongs to the domain, not the codomain.

## Proposition-changing decisions

The statement phase must freeze the following from an admitted source and independent review:

1. A common real or complex scalar field versus mathlib's more general pair of nontrivially normed
   fields connected by an isometric ring homomorphism.
2. Normed additive groups versus seminormed additive groups, and continuous linear maps versus
   continuous semilinear maps.
3. An arbitrary index type versus the sequence form actually printed in the 1927 source.
4. Pointwise boundedness encoded by real existential bounds, bounded ranges, or an `ENNReal`
   supremum, together with checked relationships for every credited alternate form.
5. Exact universes, binder order, implicit typeclasses, inequality orientation, and the location
   and dependencies of the two existential bounds.
6. Whether empty families, trivial spaces, and negative candidate bounds stay within the universal
   proposition, and how they are mutation-tested.
7. The source edition, incorporated definitions, exact proof boundary, translation, corrections or
   errata, arbitrary-family bridge, and independent review.

## Historical source boundary

Banach and Steinhaus's 1927 paper defines a complete metric real vector domain `D`, a normed vector
codomain `C`, continuous additive (called linear) functionals `u : D -> C`, and the operator norm.
Section 2, Lemma 3 proves that if a sequence `(u_n)` is pointwise bounded in limsup on a set of
second category, then the limsup of the operator norms is finite. Taking the whole complete domain
gives sequential uniform boundedness. The article's headline Theorems I and II are stronger
double-sequence condensation results, not literally the arbitrary-family candidate above.

An unbounded arbitrary family yields a sequence with norms tending to infinity, so the modern
family form is mathematically related. That selection/reduction uses an additional choice and
contradiction argument not stated as Lemma 3 and must be checked rather than silently imported.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Normed.Operator.BanachSteinhaus` declares:

```text
banach_steinhaus
  [CompleteSpace E]
  {g : iota -> E ->SL[sigma12] F}
  (h : forall x, exists C, forall i, norm (g i x) <= C) :
  exists C', forall i, norm (g i) <= C'
```

It also declares `banach_steinhaus_iSup_nnnorm`. The former is a direct exact-topic interface and
supports provisional `M3`, but it is more general than the historical real-linear setting. The
barrelled-space theorem `WithSeminorms.banach_steinhaus` is a proof-route lead and must not replace
the normed-space root.

## Explicit exclusions

- Discontinuous or merely algebraic linear maps, nonlinear maps, or arbitrary numerical/functions
  families.
- A premise at one fixed vector, or only on a dense subset without an additional bridge.
- One premise bound uniform over both `x` and `i`, which materially strengthens pointwise
  boundedness.
- A codomain-completeness premise silently added to the theorem.
- The general barrelled-space/equicontinuity theorem substituted for the conventional root.
- `THM-M-0312` status, statement work, proof credit, or receipts inherited across target IDs.
- The catalog label, theorem name, primary-source URL, or successful API probe used as kernel or
  source-completion evidence.

No canonical Lean expression, ordered binder list, checked alternate encoding, expression hash,
or environment fingerprint is frozen by this intake.
