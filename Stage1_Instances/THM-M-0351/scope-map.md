# Scope map

## Included topic boundary

- A source-specified Littlewood-Paley decomposition on a specified group or Euclidean space.
- Exact low-frequency and dyadic projection operators, including cutoff regularity and support.
- The stated function or distribution space, exponent range, measure, and scalar field.
- The source's precise inequality, norm equivalence, unconditional convergence, or reconstruction
  conclusion, with its constants and mode of convergence.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these materially different targets:

1. **Periodic theorem:** a Littlewood-Paley inequality for Fourier series on the circle or torus.
2. **Euclidean square-function theorem:** for `1 < p < infinity`, equivalence between an `L^p`
   norm and a dyadic square-function norm on `R^n`.
3. **Hilbert-space decomposition:** an `L^2` orthogonal or almost-orthogonal frequency-band
   identity, which is substantially weaker than the general `L^p` theorem.
4. **Reconstruction:** convergence of the sum of dyadic blocks to the input, either in a norm or
   distributionally.
5. **Function-space characterization:** a homogeneous or inhomogeneous Besov or
   Triebel-Lizorkin norm characterization.

The statement phase must inspect an immutable source and freeze the ambient space, Fourier
normalization, dyadic partition, low-frequency block, exponent range, input class, equality or
two-sided constants, and convergence sense. It must also decide whether the theorem is scalar or
vector valued and whether endpoints or weak-type variants are included.

## Explicit exclusions

- Plain Plancherel or Fourier-series convergence as a substitute for a general Littlewood-Paley
  theorem.
- An arbitrary sequence decomposition with no Fourier support or partition-of-unity conditions.
- A tautological square function defined to equal the original norm.
- Wavelet, Besov, Triebel-Lizorkin, multiplier, or Calderon-Zygmund theorems as substitutes unless
  the selected source states an exact checked equivalence.
- The separate manifest target `THM-M-1298`, which has the same title in a PDE category but is a
  distinct repository ID and cannot share scope or proof credit.
- The inventory label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify one.

