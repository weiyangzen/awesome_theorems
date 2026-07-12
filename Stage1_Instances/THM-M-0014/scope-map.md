# Scope map

## Preserved source scope

The repository fixes the title `克罗内克-韦伯定理` and the literal claim
`有理数域的有限阿贝尔扩张都包含于分圆域`: every finite abelian extension of the rational
field is contained in a cyclotomic field. It attributes the record to Leopold Kronecker and
Heinrich Weber and gives the year 1887. This identifies the classical Kronecker-Weber theorem
family, but the record does not define its objects or specify a source edition, theorem locator,
proof, correction history, or formal target.

## Statement decisions still open

An approved statement phase must resolve all of the following from an immutable, independently
reviewed source:

- whether an extension means a literal field tower `Q <= K`, an abstract `Q`-algebra `K`, an
  intermediate field of a fixed algebraic closure, or an isomorphism class;
- how finiteness is represented and whether `K` is assumed to be a number field;
- whether "abelian" explicitly includes the finite Galois hypotheses, or is phrased through the
  automorphism group after normality and separability have been established;
- whether "contained" is literal set inclusion in one ambient algebraic closure, a `Q`-algebra
  embedding, or equivalence with an intermediate field of a cyclotomic extension;
- the precise cyclotomic field model and primitive-root convention, including the local algebra
  structure used by mathlib's `CyclotomicField` API;
- whether the index is a positive integer or a nonzero natural, and whether it is merely an
  existence witness or the conductor of the extension;
- the ordered binders, universe levels, typeclass coherence assumptions, and exact conclusion;
- the treatment of the trivial extension, index `1`, index `2`, and alternate embeddings of the
  same abstract number field; and
- the exact equivalence or implication directions between all credited presentations.

These are proposition- or encoding-changing decisions. They are a resolution ledger, not a
canonical statement.

## Candidate presentation not credited

A nearby legacy artifact for the separate target `THM-M-0419` suggests the following useful Lean
shape: a number field `K` with an `Algebra Q K` instance and `IsAbelianGalois Q K` embeds as a
`Q`-algebra into `CyclotomicField n Q` for some nonzero natural `n`, using
`CyclotomicField.algebraBase` on the codomain. It explicitly contains no terminal
Kronecker-Weber proof.

That shape is not adopted for `THM-M-0014` at intake. A reviewed source-to-presentation mapping
must first show that it is faithful to this record's literal containment claim, and checked
transports must relate it to any literal-subfield formulation. Merely copying the sibling target
would violate target ownership and would not establish statement identity.

## Explicit exclusions

- `THM-M-0419`, its lifecycle state, its dossier, and its legacy `S1_M_074.lean` declarations are
  not merged, copied, or credited to this target.
- The easy direction that a cyclotomic extension is abelian Galois is not the converse
  Kronecker-Weber containment theorem.
- A theorem about one fixed cyclotomic field, one chosen extension, quadratic fields, or another
  special case cannot replace the universal finite-abelian-extension claim.
- A definition, structure field, hypothesis, or axiom that assumes the desired embedding is not a
  proof.
- The catalog's `已验证` label, a theorem name, a citation, a wrapper, or a search result supplies
  no human-source or kernel credit by itself.

## Human-source boundary

The human theorem is historically established, so the provisional human debt is `H1`, not a claim
that the mathematics is open. The repository has only an uncited secondary gloss. `H0` requires an
immutable primary or authoritative proof source with edition, exact theorem/page, incorporated
definitions and assumptions, errata audit, source-to-obligation mapping, and independent review.

## Formal boundary

No canonical Lean expression is frozen. The pinned probe authenticates only `NumberField`,
`IsAbelianGalois`, `CyclotomicField`, `CyclotomicField.algebraBase`,
`CyclotomicField.isCyclotomicExtension`, and algebra homomorphisms. A bounded exact-topic search
finds the explicitly nonterminal sibling legacy module and no terminal declaration in pinned
mathlib. This is intake discovery, not an exhaustive formal-anchor audit or a global absence claim.
