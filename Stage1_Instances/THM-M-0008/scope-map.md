# Scope map

## Metadata boundary

The source record identifies the subject (Tor functors) but not a proposition. "Properties" may
refer to mutually non-equivalent roots, including:

1. computation of `Tor` as derived tensor product and its functoriality;
2. vanishing of positive-degree Tor when one argument is projective or flat;
3. balancedness, comparing resolutions in the two variables;
4. connecting morphisms and the long exact Tor sequence associated to a short exact sequence;
5. module-level results such as `Tor₁` detecting flatness.

The statement phase must select exactly one source theorem, or a source-defined theorem family with
an explicit finite root conjunction. It must not bundle unrelated properties merely because the
metadata uses a plural noun.

## Domains to decide

- Rings and left/right modules versus a monoidal abelian category.
- Projective, flat, or enough-projectives assumptions and which tensor variable is derived.
- Natural isomorphism versus objectwise isomorphism, and variance in both arguments.
- Degree indexing, the degree-zero case, short exact sequence orientation, and boundary maps.
- Universe levels, linearity, classical choice, and the exact mathlib object model.

## Exclusions

- `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_101.lean` as accepted rev-5.6 evidence.
- Its `StatementShape := Nonempty (TorPropertyPackage C)` as a source-faithful target: several
  package fields are abstract `Prop`s paired with proof fields and have no source statement.
- Projective-vanishing wrappers as proof of balancedness or a long exact sequence.
- The neighboring Ext long-exact-sequence target, or a generic homology sequence, as a substitute.

After source selection, statement work must freeze ordered binders, hypotheses, conclusion,
degenerate cases, imports, elaborated expression, environment fingerprint, and mutation tests.
