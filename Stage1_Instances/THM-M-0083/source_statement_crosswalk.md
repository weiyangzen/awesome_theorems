# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Meaning of representability | S. Mac Lane, *Categories for the Working Mathematician*, 2nd ed., Springer GTM 5 (1998), Chapter III, section 2, “Representable Set-Valued Functors” | `CategoryTheory.Functor.IsRepresentable` in `Mathlib.CategoryTheory.RepresentedBy` | Standard primary textbook anchor located; immutable scan/page and definition-level premise audit remain open |
| Universal element characterizes a representation | Mac Lane, same edition, Chapter III, section 2, discussion of universal elements and representations | provisional `UniversalElementCriterion F ↔ F.IsRepresentable` | Selected exact-root interpretation; source wording must be pinpointed and independently reviewed before H0 |
| Induced map sends `f : Y ⟶ X` to `F(f)(x)` | Same universal-element construction for a contravariant set-valued functor | `fun f : Y ⟶ X => F.map f.op x` | Variance and `op` placement are explicit; Lean elaboration and mutation checks remain statement-phase work |
| Representing object uniqueness | Mac Lane, Chapter III, representability consequences via Yoneda | `RepresentableBy.uniqueUpToIso` | Consequence only; deliberately excluded from the exact root |
| Adjoint-functor or Brown-style existence theorem | Not identified by the repository's terse source text | legacy partial-adjoint/AFT and homological branches | Excluded. Substituting one of these stronger theorems would broaden or change the assigned theorem |

The metadata supplies only the Chinese title `可表函子定理` and description
`函子可表的条件`. Those words do not uniquely identify Freyd's adjoint functor
theorem, Brown representability, or another specialized existence theorem. The
legacy Lean artifact explicitly chooses the universal-element characterization;
this intake preserves that choice provisionally while recording the ambiguity
rather than manufacturing a stronger source statement.

Discovery anchors, not immutable evidence receipts:

- Mac Lane bibliographic record: ISBN 978-0-387-98403-2, DOI
  `10.1007/978-1-4757-4721-8`.
- Repo-local candidate:
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_139.lean`.
- Mathlib candidate module: `Mathlib.CategoryTheory.RepresentedBy`.

No `H0` or machine-closure claim is made. The source audit must obtain a fixed
edition artifact, exact pages/definitions, assumption and variance crosswalk,
errata search, and independent review. The statement phase must then elaborate
the selected target, fingerprint its environment and normalized expression,
check bundled/unbundled transports, and mutation-test universes, variance,
binders, bijectivity, and empty-category boundaries.
