# Statement receipt

Item: `S56-M-0533-STATEMENT`  
Theorem: `THM-M-0533`  
Base revision: `9c62e277cad936290d63af79d788d97dd17bf4cf`

## Frozen target

The canonical declaration is
`AwesomeTheorems.THM_M_0533.MayerVietorisSequence` in `Statement.lean`.  It states the ordinary
integral singular-homology Mayer-Vietoris long exact sequence for two open subsets `U` and `V` of
a topological space `X` whose union is all of `X`.  Homology is the pinned mathlib
`AlgebraicTopology.singularHomologyFunctor` with coefficients `ULift Z`; the lift is the
universe-polymorphic encoding of integral coefficients.

For every natural degree it binds a connecting morphism and concludes exactness at the
intersection, biproduct, and ambient-space terms.  It also concludes surjectivity of the final
degree-zero map by exactness of `H_0(U) direct-sum H_0(V) -> H_0(X) -> 0`.  The inclusion map from
the intersection is `(i_*, -j_*)`; the map to `X` is the sum of the two inclusion-induced maps.
Connecting morphisms are existential data, not hypotheses, and exactness is never assumed.

Minimal declared imports are the singular-homology API, the abelian/additive-group instances and
biproduct/colimit instances required to instantiate it, short-complex exactness, and open-subspace
inclusions.  The canonical expression is universe-polymorphic and has type `Prop`.

`MayerVietorisSequenceAlternate` is a separately written implication-form encoding;
`canonical_iff_alternate` is its kernel-checked `Iff`.  The four mutation declarations remove the
cover hypothesis, change opens to sets, move the space binder outside, and omit the complete
degree-zero endpoint.  `fail_if_success ... rfl` checks that none is definitionally identical to
the canonical target.  This is a statement-identity mutation test only, not proof evidence.

## Scope and source boundary

The statement fixes the open-cover form, unreduced integral singular homology, natural indexing,
sign convention, and degree-zero endpoint.  These match the standard statement in Allen Hatcher,
*Algebraic Topology* (Cambridge University Press, 2002), Mayer-Vietoris Sequences, p. 149: for
`X = A union B` with the interiors of `A` and `B` covering `X`, the sequence with maps
`phi = (i_*,-j_*)` and `psi = k_* + ell_*` is exact.  Taking `U,V` open makes their interiors equal
to themselves.  This statement phase does not claim an H0 source review or theorem proof.

## Environment fingerprint

- Lean toolchain: `leanprover/lean4:v4.29.0`
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- project base: `9c62e277cad936290d63af79d788d97dd17bf4cf`
- TCB: Lean kernel, Lake environment, pinned mathlib object/source tree
- foundation: mathlib's noncomputable categorical homology construction; no new axiom or axiom
  declaration is introduced by this statement module
- computation: declarative/noncomputable; no oracle or experimental result

## Validation

Run from `Formalizations/Lean`:

| Command | Result |
|---|---|
| `lake env lean ../../Stage1_Instances/THM-M-0533/Statement.lean` | exit 0; canonical declaration printed with type `Prop`; only mutation-fixture unused-variable warnings |
| `rg -n 'sorry' Stage1_Instances/THM-M-0533 --glob '*.lean'` | exit 1; no matches |
| `git diff --check -- Stage1_Instances/THM-M-0533` | exit 0; no output |

This receipt supports only provisional statement-node acceptance.  Anchor audit, obligation tree,
proof, theorem validation, release, H0, M0, R0, audit completion, and theorem completion remain
open.
