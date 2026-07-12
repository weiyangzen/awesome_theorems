# Scope map

## Included topic boundary

- A source-selected uncertainty theorem for a function and its Fourier transform.
- The exact ambient space, measure, scalar field, Fourier convention, function class, concentration
  functional, hypotheses, bound or rigidity conclusion, and equality cases in that source.
- Boundary handling for zero functions, infinite quantities, and almost-everywhere equality.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different propositions:

1. **Variance/second-moment inequality:** a product of spatial and frequency dispersions has a
   normalization-dependent positive lower bound, possibly after centering.
2. **Support-size theorem:** finite-measure or compact-support assumptions on both a function and
   its Fourier transform force vanishing, or satisfy a quantitative support bound.
3. **Concentration inequality:** most `L2` mass cannot lie simultaneously in prescribed spatial
   and frequency sets, with a quantitative error term.
4. **Entropic uncertainty:** an entropy sum has a lower bound.

The statement phase must select an immutable source passage and freeze ordered binders, whether the
domain is `ℝ` or `ℝ^n`, the Fourier kernel (`2π` convention included), integrability/Sobolev or
Schwartz hypotheses, centering, normalization, the meaning of concentration, constants, and
equality cases.

## Explicit exclusions

- Hardy's uncertainty principle (`THM-M-0345`) as a substitute.
- The operator/quantum-mechanical Robertson or canonical-commutator inequality as a substitute for
  this harmonic-analysis entry.
- Plancherel, Fourier inversion, or norm preservation alone; these are infrastructure, not the
  claimed uncertainty result.
- A tautology obtained by assuming the desired lower bound or defining "concentrated" to make the
  conclusion immediate.
- The repository label `已验证` as source or proof evidence.

No canonical Lean target is frozen at intake because the qualitative gloss does not determine one.
