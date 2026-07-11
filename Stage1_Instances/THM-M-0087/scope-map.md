# Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | Classical Gabriel-Popescu representation of a Grothendieck abelian category as a Serre quotient of modules | Exact choice of ring/opposite conventions and equivalence API is open |
| Category hypotheses | abelian, cocomplete/AB5 Grothendieck structure, generator or separator, local smallness and universes | Equivalence of repository typeclasses with source hypotheses is unverified |
| Embedding branch | `Hom(G,-)` / preadditive coyoneda is full and faithful | Existing wrapper is discovery input; exact elaboration is deferred |
| Adjoint branch | a left adjoint to the embedding and its exactness/finite-limit behavior | Finite-limit preservation alone must not be silently substituted for the full quotient theorem |
| Quotient branch | kernel as a localizing Serre subcategory and induced equivalence from the quotient | Historical file describes only a conditional localization bridge; root composition remains open |
| Foundations | Lean kernel, pinned mathlib, classical categorical constructions | toolchain, dependency closure, axioms, and TCB are not fingerprinted |

Minimum future branches are: hypothesis normalization; module-category convention;
fullness and faithfulness; adjunction; exactness; kernel/Serre/localizing properties;
quotient universal property; essential surjectivity/equivalence; and checked
composition to the classical root. No branch is closed or excluded at intake.
