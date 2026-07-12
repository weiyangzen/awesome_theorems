# Scope map

## Included topic boundary

- Algebraic computation over a source-specified coefficient semiring, ring, or field.
- A source-specified computation model, such as arithmetic circuits or straight-line programs.
- Exact resource measures, including size, depth, degree, uniformity, and constants policy where
  relevant.
- One concrete theorem about a specified polynomial family, complexity class, completeness result,
  reduction, upper bound, or lower bound.

## Ambiguities to resolve at statement freeze

The repository record does not select a proposition. At minimum, the source phase must decide:

1. whether the objects are individual polynomials, polynomial families, circuits, or algorithms;
2. the coefficient domain and whether constants are free, bounded, or uniform;
3. the circuit gates, fan-in, size/depth measure, and family uniformity convention;
4. whether the conclusion is membership, completeness, simulation, an upper bound, or a restricted
   lower bound;
5. all asymptotic quantifiers and encodings of input length, number of variables, and degree.

Boundary cases that remain open include zero-variable and zero polynomials, constant circuits,
empty families, degree zero, circuits of size/depth zero, and characteristic-dependent claims.

## Explicit exclusions

- The unresolved VP versus VNP equality/separation problem, separately recorded as `THM-M-0735`.
- Boolean circuit complexity, proof complexity, or numerical algorithm complexity as substitutes.
- A definition of arithmetic-circuit complexity presented as though it were a theorem.
- An easy identity about multivariate polynomials substituted for a complexity theorem.
- Any unrestricted general circuit lower bound not actually proved by the selected source.
- The repository label `已验证` as human-proof or machine-proof evidence.

No canonical Lean target is frozen at intake because no proposition is present in the source record.
