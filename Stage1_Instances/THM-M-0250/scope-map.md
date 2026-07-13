# Scope map

## Received topic boundary

The repository wording supports only a classical analytic Hardy-space subject on the complex unit
disk. A later statement phase may select a theorem inside that family only after an accountable
source review. At minimum it must fix:

- the disk model (`{z : C | |z| < 1}` or an equivalent subtype) and scalar/value space;
- an exponent regime such as `0 < p < infinity`, `1 <= p < infinity`, `p = 2`, or `p = infinity`;
- holomorphicity or complex analyticity on the disk;
- the radial functional, including normalized angular measure and whether powers, roots, extended
  values, or essential suprema are used;
- the `H^p` carrier, equality, norm or quasinorm, and completeness convention; and
- one exact conclusion, all quantitative constants, ordered binders, hypotheses, and boundary
  cases.

This is a topic boundary, not a candidate statement and not proof credit.

## Proposition-changing choices

The phrase "Hardy spaces on the unit disk" leaves materially different targets open:

1. Definition or nontriviality of `H^p`, versus vector-space, normed-space, Banach, or quasi-Banach
   structure.
2. Radial integral-mean membership versus an almost-everywhere boundary `L^p` characterization,
   including the existence and mode of radial or nontangential limits.
3. The coefficient `l^2` characterization and isometry for `H^2`, versus general `H^p` theory.
4. Point-evaluation or growth bounds, density of polynomials, maximal-function estimates, or
   factorization results.
5. A single fixed exponent, a quantified range of finite positive exponents, or the `H^infinity`
   endpoint; scalar-valued versus vector-valued functions.
6. Normalized Haar/Lebesgue measure on the circle versus an unnormalized angular integral, and
   supremum versus limit as the radius tends to one.

These variants are related mathematically but are not interchangeable Lean propositions. No
variant is canonical at intake.

## Boundary cases to freeze later

- `p = 0`, `p = 1`, `p = 2`, finite `0 < p < 1`, and `p = infinity`.
- Radius `r = 0`, the open endpoint `r < 1`, and limiting behavior as `r` tends to one.
- The zero function and conventions for zero powers, logarithms, and extended-real values.
- Functions defined on all of `C` versus only on the unit-disc subtype; equality pointwise versus
  equality of boundary functions almost everywhere.
- Real versus complex scalars, vector-valued codomains, and any completeness assumptions.
- Empty or degenerate encodings accidentally obtained through inconsistent exponent or radius
  hypotheses.

No case is excluded yet because there is no exact proposition to which an exclusion can attach.

## Neighbor-target boundary

- `THM-M-0251` separately owns inner-outer factorization in Hardy spaces.
- `THM-M-0252` separately owns the Corona / `H^infinity` maximal-ideal-space result.
- `THM-M-0253` separately owns Hardy-space interpolation sequences.
- `THM-M-0254` separately owns the catalog's BMO characterization topic.
- `THM-M-0300` owns real-variable `H^1` atomic decomposition, while `THM-M-0360` through
  `THM-M-0363` own real-variable Hardy multiplier, characterization, atomic-decomposition, and BMO
  duality families.

Those records may guide discovery but cannot donate a statement, proof body, receipt, or accepted
state to this target.

## Explicit exclusions

- Defining an arbitrary predicate named `HardySpace` and proving a tautology about it.
- Assuming the desired boundary value, norm bound, factorization, or completeness property as data
  and returning it by projection.
- Substituting harmonic Hardy spaces, real-variable Hardy spaces on Euclidean space, a half-plane
  theory, or one special polynomial/function case without a source decision.
- Treating complex mean value, the maximum-modulus principle, or circle-integral infrastructure as
  the missing Hardy-space root.
- Treating the untrusted `已验证` label, a nearby declaration name, or a successful API probe as
  human-source or machine-proof evidence.

## Retry condition

Before statement execution, an accountable reviewer must preserve and hash an immutable primary or
authoritative source, identify an exact theorem and all incorporated definitions, map its complete
assumptions and conclusion, check corrections or errata, and obtain independent review. Only then
may the statement phase choose minimal imports, elaborate the exact Lean expression, serialize its
environment fingerprint, check alternate transports, and run all required mutation classes.
