# Source-statement crosswalk

## Repository source

`Docs/Stage0_Blueprint.md` and `Docs/researches/math_theorems.md` identify the 1972
Zakharov-Shabat system with the short claim `NLS\u65b9\u7a0b\u7684Lax\u5bf9` ("a Lax pair for the NLS
equation"). The manifest's `\u5df2\u9a8c\u8bc1` label is explicitly untrusted under rev-5.6 and supplies no
human-source or kernel credit.

## Candidate primary source

The primary candidate is V. E. Zakharov and A. B. Shabat, "Exact theory of two-dimensional
self-focusing and one-dimensional self-modulation of waves in nonlinear media," *Soviet Physics
JETP* 34 (1972), no. 1, 62-69 (English translation of the Russian publication). It introduces an
auxiliary spectral system for the nonlinear Schrodinger model and derives compatibility/evolution
relations used by the inverse-scattering method.

This bibliography is a discovery anchor, not `H0` evidence. The original and English editions,
exact equation numbers, translation fidelity, hypotheses, and errata have not been independently
inspected in this intake. The statement phase must not fill those gaps from memory.

## Crosswalk

| Repository phrase | Source component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| Zakharov-Shabat system | source's two-component auxiliary spatial system | typed vector or pair, coefficient matrix/operator, and spatial derivative equation | included; exact equations and types open |
| Lax pair | paired spatial and temporal auxiliary evolutions | two operators or matrix-valued coefficients plus an explicit compatibility predicate | included; convention open |
| NLS equation | source-normalized nonlinear Schrodinger evolution | complex-valued potential, derivatives, nonlinear term, domains, and equality | included; sign and normalization open |
| compatibility | equality of mixed evolutions or zero curvature | differentiability hypotheses and sign-correct coefficient identity | included; direction/equivalence open |
| reduction of potentials | source relation producing the physical NLS field | conjugation/sign relation and any real-valued parameter | included if present in selected passage; exact form open |
| spectral parameter | parameter in the auxiliary problem | explicit type, binder order, and quantifier | included; domain and scope open |
| inverse scattering | method surrounding the compatibility calculation | separate analytic definitions and theorems | excluded from the root unless source selection requires a named sub-obligation |

## Lean boundary

Repository search finds legacy abstract Lax-pair and zero-curvature material, including
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_210.lean`. That material does not select the 1972
equations, encode the NLS potential reduction, or establish a source-to-expression bridge. It is
therefore only a later anchor-audit candidate and supplies no `M0` credit here.

Before `H0`, an independent reviewer must verify an immutable primary-source copy, exact page and
equation anchors, assumptions, translation differences and errata, and every source-to-Lean row.
Before any machine credit, the statement phase must elaborate the exact expression and check any
normalization, scaling, gauge, or focusing/defocusing transport used.
