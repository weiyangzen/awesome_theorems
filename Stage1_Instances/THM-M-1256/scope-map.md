# Scope map

## Preserved source scope

- Operator: a linear partial differential operator with constant coefficients.
- Claim family: solvability of the corresponding PDE.
- Attribution/date: Lars Hörmander, 1955, as unverified repository metadata.
- Intended distinction: this is not the separately indexed 1967 subelliptic Hörmander theorem.

This is the full mathematical scope justified by the repository record. It does not yet determine
a proposition.

## Decisions required before statement freeze

The statement phase must identify a primary source and freeze: the coefficient field and number of
variables; the polynomial symbol and exclusion of the zero operator, if required; the domain and
local/global quantifiers; the datum and solution spaces (smooth functions, distributions, or other
spaces); the equation convention `P(D)u = f`; support or growth conditions; and whether the result
asserts a fundamental solution or direct solvability. Boundary cases such as zero-dimensional
space, the zero polynomial, zero datum, and disconnected/open domains must be explicitly mapped.

It must also record the exact relation, if any, between the chosen theorem and the
Malgrange-Ehrenpreis assertion that every nonzero constant-coefficient linear differential operator
has a distributional fundamental solution.

## Explicit exclusions

- `THM-M-1255` (Malgrange-Ehrenpreis) adopted merely as a convenient substitute.
- The 1967 bracket-generating/subelliptic theorem (`THM-M-1258` or `THM-M-1259`).
- The Hörmander Fourier multiplier theorem or propagation-of-singularities results.
- Variable-coefficient PDE solvability, hypoellipticity, or regularity without source support.
- Treating the metadata label `已验证` as either human-proof or Lean-kernel evidence.
