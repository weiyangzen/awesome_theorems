# Source-statement crosswalk

## Candidate primary sources

- Nobuo Yoneda, "On the homology theory of modules," *Journal of the Faculty of Science,
  University of Tokyo, Section I* 7 (1954), 193-227. This is the historical source candidate;
  the exact formulation and page must be inspected before H0.
- Saunders Mac Lane, *Categories for the Working Mathematician*, second edition, Springer (1998),
  the Yoneda lemma section. This is a modern authoritative source candidate; theorem number,
  page, assumptions, and errata remain to be checked.

These are discovery anchors, not verified source evidence.

## Crosswalk

| Repository phrase | Mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "Yoneda lemma" | `Nat(Hom(-, X), F) ≅ F(X)` naturally in `X,F` | `yonedaEquiv` / `yonedaLemma` | required bridge; audit open |
| "object is uniquely determined" | representables reflect object isomorphism | `Yoneda.fullyFaithful.preimageIso` | canonical consequence |
| "representable functor" | contravariant hom functor | `yoneda.obj X` | variance frozen; universes open |
| "uniquely" | uniqueness up to categorical isomorphism, not equality | `Nonempty (X ≅ Y)` | included |
| converse | object isomorphism induces representable isomorphism | `yoneda.mapIso` | included |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_138.lean` declares `StatementShape` and wrappers
using `Yoneda.fullyFaithful`, `preimageIso`, and `yoneda.mapIso`. It imports much broader homological
material than the core claim needs. The statement node must determine minimal pinned imports and
check the exact type; the anchor-audit node must record mathlib revision, declaration types, axioms,
and terminal proof provenance. No legacy declaration is accepted here.

