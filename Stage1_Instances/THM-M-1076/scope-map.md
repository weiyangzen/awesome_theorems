# Scope map

## Repository-supported scope

The repository fixes only the name "Smith's key renewal theorem", the attribution to Walter Smith,
and the description "limit behavior of renewal processes". That supports classifying the target as
renewal theory, but it does not determine one proposition.

## Candidate classical scope

The most common nonarithmetic formulation uses an interarrival law `F` on the nonnegative
half-line, its renewal measure `U = sum_(n >= 0) F^{*n}`, finite positive mean `mu`, and a directly
Riemann integrable function `z`. Its characteristic conclusion is

```text
integral over [0,t] of z(t - x) U(dx)  ->  (1 / mu) integral over [0,infinity) of z(x) dx.
```

This formula is a candidate scope description only. The source audit must decide whether the
selected edition uses `U` including the mass at zero, a renewal function instead of a measure,
integration over `[0,t]` or the real line, and real-valued or signed test functions. It must also
transcribe the exact definition of direct Riemann integrability and every regularity assumption.

## Variant decisions required

| Surface | Material alternatives | Why it changes the target |
|---|---|---|
| Renewal model | ordinary, delayed, or random-walk renewal | initial delay and negative increments change the measure and hypotheses |
| Arithmetic type | nonarithmetic or lattice with maximal span `d` | the limiting integral is replaced by a residue-class lattice sum |
| Mean | finite positive, zero, or infinite | the standard normalization needs `0 < mu < infinity` |
| Test function | directly Riemann integrable, nonnegative, signed, compactly supported, or another class | convergence and integrability obligations differ |
| Renewal convention | include `F^{*0}` or begin at the first renewal | boundary mass and formulas differ, even if some limits agree |
| Limit mode | scalar analytic limit, almost sure process limit, or distributional convergence | these are different propositions |
| Time boundary | `t -> infinity` on reals or integers | topology and lattice formulation differ |

## Explicit exclusions

- THM-M-1077 Blackwell's renewal theorem, even if it is later used as a proof ingredient.
- Only the elementary renewal theorem `E[N(t)] / t -> 1 / mu`.
- A renewal reward theorem or regenerative-process limit without a checked equivalence.
- A theorem whose hypotheses already contain the desired convolution limit.
- Any lattice/nonlattice transport that has not been stated and checked explicitly.

The statement phase must obtain an authoritative formulation before fixing ordered binders,
domains, boundary cases, universes, imports, or a Lean expression.
