# Scope map

## Included topic boundary

- A source-specified Fourier multiplier operator on a specified group or Euclidean space.
- The exact symbol regularity, differentiability, integral, Sobolev, or scale-uniform condition.
- The source's function space, scalar field, measure, Fourier normalization, and exponent range.
- The precise strong- or weak-type boundedness conclusion, including dependence of its constant.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these materially different targets:

1. **Hormander integral criterion:** a scale-uniform integral/Sobolev condition on localized
   derivatives of the symbol implies strong `L^p` boundedness in a source-defined exponent range.
2. **Hormander-Mihlin criterion:** pointwise derivative estimates through a dimension-dependent
   order imply `L^p` boundedness for `1 < p < infinity`.
3. **Hilbert-space result:** an essentially bounded symbol yields an `L^2` multiplier, which is
   substantially weaker than a general `L^p` multiplier theorem.
4. **Periodic or group variant:** a theorem for Fourier series or another locally compact abelian
   group, with discrete symbols and different hypotheses.
5. **Endpoint variant:** weak `(1,1)`, Hardy-space, BMO, or other endpoint conclusions rather than
   ordinary strong `L^p` boundedness.

The statement phase must inspect an immutable source and freeze the ambient space and dimension,
Fourier normalization, symbol measurability and equivalence convention, smoothness/order or
localized norm, treatment of the origin, exponent range, initial dense domain, extension to `L^p`,
and the exact operator-norm conclusion. Binder scope and all constants must follow that source.

## Explicit exclusions

- Plancherel or the bounded-symbol `L^2` result as a substitute for a general `L^p` theorem.
- The neighboring manifest target `THM-M-0359` (Mihlin multiplier theorem) without a checked source
  showing that the present target intentionally uses exactly that statement.
- A Fourier multiplier defined on Schwartz functions or tempered distributions without the claimed
  `L^p` extension and bound.
- An arbitrary assumed bounded linear map packaged as the desired multiplier.
- Calderon-Zygmund, Littlewood-Paley, or singular-integral boundedness as a substitute absent a
  checked equivalence and source crosswalk.
- The inventory label `已验证` as human-source or kernel-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify a unique
symbol criterion or proposition.

