# Scope map

## Included root

Let `K` be a number field of degree `n`, with `r2` pairs of complex embeddings, ring of integers
`O_K`, and discriminant `d_K`. For every class `C` in the ideal class group of `O_K`, the intended
claim produces a nonzero integral ideal `I` representing `C` with

`N(I) <= (4 / pi)^r2 * (n! / n^n) * sqrt(abs(d_K))`.

The statement phase must freeze the meanings of ideal-class orientation, integral/nonzero ideal,
absolute ideal norm, discriminant sign convention, coercions from naturals to reals, and equality at
the boundary. It must also check degree-one fields, totally real fields (`r2 = 0`), and the fact that
number fields have nonzero discriminant.

## Object and binder map

| Mathematical object | Anticipated Lean representation | Status |
|---|---|---|
| number field `K` | `K : Type u`, `[Field K]`, `[NumberField K]` | discovery only |
| ring of integers | `𝓞 K` | discovery only |
| ideal class | `ClassGroup (𝓞 K)` | discovery only |
| nonzero integral ideal | `(Ideal (𝓞 K))⁰` | discovery only |
| class represented by `I` | `ClassGroup.mk0 I` | orientation must be checked |
| absolute norm | `absNorm (I : Ideal (𝓞 K))` | codomain/coercion must be checked |
| degree and complex places | `finrank ℚ K`, `NumberField.InfinitePlace.nrComplexPlaces K` | discovery only |
| discriminant | `NumberField.discr K` | convention must be crosswalked |

## Exclusions

- Minkowski's convex-body theorem by itself.
- Minkowski's lattice first or second theorem, or the Minkowski sum of convex sets.
- Merely proving finiteness of the ideal class group or existence of some representative.
- A bound only for principal ideals, or a claim that the class group has abstract generators below
  a bound without a representative for every class.
- PID/class-number-one corollaries, which may be downstream applications but are not the root.
- The legacy wrapper as accepted rev-5.6 evidence before exact-statement and provenance gates.

The later statement phase owns universes, ordered binders, minimal imports, normalized expression,
checked transports, environment fingerprint, and mutation tests. These are deliberately not claimed
by intake.
