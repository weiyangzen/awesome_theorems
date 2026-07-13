# THM-M-0941 scope map

## Preserved theorem family

The repository fixes target `THM-M-0941`, the name Freiman's theorem, Gregory Freiman, 1964, and
the slogan "structure of sets with small doubling." This identifies the classical inverse-additive
theorem family: a finite set with small sumset has bounded-complexity progression structure. It
does not select one binder-complete claim.

The familiar integer statement is only a locator: for a finite set `A` of integers with
`|A + A| <= K |A|`, one expects containment in a proper multidimensional arithmetic progression
whose dimension and size are bounded in terms of `K`. It is not frozen or credited here.

## Proposition-changing decisions

The statement phase must independently source and freeze all of the following:

1. The ambient domain: integers, a torsion-free abelian group, a bounded-torsion group, or an
   arbitrary abelian group. The inspected Green-Ruzsa arbitrary-group extension specifically uses
   coset progressions and is not the same proposition as the classical integer theorem.
2. A finite set versus finset representation, nonemptiness, decidable equality, and whether the
   hypotheses use `|A + A| <= K |A|`, a rational doubling constant, or another normalization.
3. The type and range of `K`, its quantifier order, and whether bounds are qualitative existential
   functions `d(K), f(K)` or explicit quantitative formulas and constants.
4. The container: arithmetic progression, generalized/multidimensional arithmetic progression,
   convex progression, or coset progression, together with its exact carrier representation.
5. Properness, symmetry, translation, subgroup/torsion component, dimension or rank, and the
   cardinality bound relative to `|A|`.
6. Whether the conclusion contains all of `A`, a large subset, or only a Freiman-isomorphic model.
   These are different inverse theorems and cannot be interchanged.
7. Exact ordered binders, hypotheses, conclusion, minimal imports, logical profiles, alternate
   transports, and the removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

## Boundary cases

- The empty set, singleton sets, and the nonempty hypothesis needed by ratio-style doubling.
- `K < 1`, `K = 1`, integral versus rational/real `K`, and vacuous or impossible hypotheses.
- Arithmetic progressions of rank zero, zero side length, repeated generators, and nonproper
  parameterizations.
- Subgroups and cosets in torsion groups, where a progression-only conclusion can fail.
- Sets already equal to progressions, intervals, single cosets, or a union of cosets.
- Translations, embeddings between integers and general groups, and cardinal coercions.

No case is excluded at intake because no canonical proposition is selected.

## Excluded substitutions

- Green-Ruzsa's arbitrary-abelian-group theorem selected silently in place of the classical integer
  theorem, or conversely the integer theorem used to claim the general result.
- Freiman's dimension lemma, the `3k-4` theorem, very-small-doubling classifications, inverse
  theorems in finite fields, or polynomial Freiman-Ruzsa conjectures.
- Ruzsa covering, Plunnecke-Ruzsa growth inequalities, Balog-Szemeredi-Gowers, or an approximate-
  subgroup theorem used as the root rather than as possible dependencies.
- A Freiman homomorphism/isomorphism definition, finite model, or large structured subset used as
  though it were the required containment conclusion.
- A structure or premise storing the desired progression and its bounds.
- The catalog's untrusted `verified` label, a citation, or the API probe used as proof evidence.

## Neighbor boundaries

`THM-M-0942` owns Ruzsa's covering lemma, `THM-M-0943` the Plunnecke-Ruzsa inequality, and
`THM-M-0944` Balog-Szemeredi-Gowers. `THM-M-0940` is the catalog's separate "fundamental theorem of
additive combinatorics" entry. These may eventually be dependencies or source-disambiguation
signals, but none grants proof credit to this target.

## Formal boundary

Pinned mathlib defines finite-set addition, `Finset.addConst`, Plunnecke-Ruzsa bounds,
`IsAddFreimanHom`/`IsAddFreimanIso`, and special classifications for doubling below `3/2`, the
golden ratio, and `2`. A bounded exact-topic search found no generalized arithmetic or coset
progression interface and no declaration of the full structural Freiman theorem. These APIs are
adjacent or partial substrate only. The canonical Lean target, expression and environment fingerprints,
checked transports, discovery protocol, obligation registry, and proof state remain downstream.
