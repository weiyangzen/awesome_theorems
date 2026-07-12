# Scope map

## Included root claim

- An arbitrary family indexed by a type `iota`.
- Continuous semilinear maps `g i : E ->SL[sigma12] F` between normed spaces over compatible
  nontrivially normed fields.
- Completeness of the domain `E`; completeness of the codomain is not required.
- Pointwise boundedness: for each `x : E`, some real `C` bounds every `norm (g i x)`.
- Uniform operator-norm boundedness: one real `C'` bounds every `norm (g i)`.

The empty family and zero spaces are not excluded by the intended universal statement. The pointwise
bound may depend on `x`; the conclusion's bound may not depend on `i`.

## Explicit exclusions

- Removing completeness of the domain.
- Requiring one pointwise bound uniform over both `x` and `i`, which would strengthen the premise.
- Bounding values at only one fixed vector or only a dense subset without additional bridge data.
- Families of discontinuous linear maps or nonlinear maps.
- Uniform boundedness of arbitrary functions, measures, integrals, or numerical sequences.
- Substitution of the more general barrelled-space/equicontinuity theorem for the normed root.
- Treating the repository label `已验证` or a successful `#check` as proof evidence.

## Statement gate

`Statement.lean` freezes the universes, binder order, scalar homomorphism and typeclass context with
one direct import. `statement.json` records the normalized expression and environment fingerprints.
The checked `iff` covers the real-bound and `iSup` formulations; mutations distinguish domain
completeness, domain specialization, the scope of `C`, and index nonemptiness. The empty family has
a direct kernel-checked boundary witness. Proof closure and candidate eligibility remain downstream.
