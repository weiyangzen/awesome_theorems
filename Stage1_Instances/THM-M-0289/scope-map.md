# Scope map

## Included theorem family

- The Hardy-Littlewood maximal operator formed from averages of a source-specified function over
  source-specified neighborhoods in a Euclidean or other source-specified measure space.
- A weak type `(1,1)` distribution estimate for positive thresholds.
- The exact measurability and integrability premises, dimension-dependent constant, and covering
  result required by the selected source.

The familiar display

```text
measure {x | M f x > lambda} <= C / lambda * integral |f|
```

is only a theorem-family guide. It is not a frozen canonical statement and supplies no proof
credit.

## Decisions required at statement freeze

The source inventory does not resolve:

1. Centered versus uncentered maximal operator.
2. Open balls, closed balls, or cubes, and whether all radii or only positive radii are used.
3. Scalar, real-valued, complex-valued, or extended-nonnegative input, and whether averages use
   absolute value, norm, or extended norm.
4. Domain `Real`, `EuclideanSpace Real (Fin n)`, another finite-dimensional normed space, or a
   doubling metric-measure space.
5. Lebesgue-measure normalization and the exact constant or dimension dependence.
6. A positive real or extended-nonnegative threshold, strict versus non-strict superlevel set, and
   treatment of zero and infinite values.
7. `L1` equivalence classes versus measurable representatives with a finite integral.
8. Whether the root asserts only weak `(1,1)`, includes strong `(p,p)` consequences, or packages a
   more general maximal theorem.

All ordered binders, universes, instances, hypotheses, the superlevel-set expression, and the
constant must be copied from an immutable reviewed source rather than reconstructed from the name.

## Boundary and degenerate cases

- Zero or infinite threshold and zero or infinite integral.
- Dimension zero, empty domains, and functions equal to zero almost everywhere.
- Balls of zero radius or zero measure and points where the supremum is infinite.
- Equality of functions versus almost-everywhere equality and representative independence.
- Measurability of the maximal function and superlevel set.

No case is silently excluded. The statement phase must incorporate or explicitly reject each case
and later mutation-test the selected boundary behavior.

## Prohibited substitutions

- A strong `(p,p)` bound for `p > 1` offered instead of the weak `(1,1)` estimate.
- The discrete Hardy-Littlewood maximal inequality, an ergodic maximal theorem, a fractional or
  dyadic maximal operator, or a one-dimensional toy special case.
- A differentiation theorem, Besicovitch/Vitali covering theorem, or generic measure API presented
  as the root claim.
- An assumed weak-type field, axiom, oracle, tautological definition, or unchecked certificate.
- `THM-M-0368` artifacts or future proof credit used without an accepted duplicate-identity and
  exact-statement transport decision.
- The catalog's untrusted `verified` label, the bibliographic citation, or the API probe treated as
  source fidelity or machine proof.

## Duplicate boundary

`THM-M-0368`, "maximal function theorem," is independently scheduled at rank 860 with the gloss
"Hardy-Littlewood maximal function weak-type estimate," the same attribution and year, and a
planned dossier for the same apparent family. This is compelling duplicate evidence, not a
dependency. Until the integration lane resolves identity and ownership, both IDs remain separate
L0 instances and no receipt or acceptance crosses between them.
