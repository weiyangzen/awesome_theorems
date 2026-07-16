# Source-statement crosswalk

| Claim component | Source anchor available at intake | Lean candidate | Intake assessment |
|---|---|---|---|
| Root functional equation | Generated `Docs/Stage1_Blueprint.md` entry says only “赫克L-函数的函数方程” and gives no bibliography | No exact canonical target selected | Insufficient to fix a theorem; `H2` |
| Number field and character class | Not stated | Legacy abstract `HeckeLFunctionData.Character` | Abstract carrier does not encode an idele-class character or its required properties |
| Completion and gamma factors | Not stated | Legacy abstract `completedLFunction` | User-supplied function; no L-series, continuation, or gamma-factor construction |
| Dual/reflection | Not stated | Legacy `dual`, `center`, and `center - s` | A possible normalization shape, not a source-faithful checked transport |
| Conductor and root number | Not stated | Legacy arbitrary complex-valued fields | Required norm, modulus-one, and local-product properties are absent |
| Primitive/imprimitive and pole cases | Not stated | Legacy `isPrimitive` proposition | No mathematical definition or imprimitive transport |

## Primary-source discovery leads

- Erich Hecke, *Eine neue Art von Zetafunktionen und ihre Beziehungen zur Verteilung der
  Primzahlen*, Mathematische Zeitschrift 1 (1918), 357-376, DOI
  <https://doi.org/10.1007/BF01203828>. This is a primary historical lead, not yet an accepted
  edition/page/theorem crosswalk.
- John Tate, *Fourier Analysis in Number Fields and Hecke's Zeta-Functions*, in Cassels and
  Froehlich (eds.), *Algebraic Number Theory* (1967), 305-347. This is a primary proof-framework
  lead for adelic local/global functional equations, but the exact theorem and conventions still
  require inspection.

These leads are discovery citations, not immutable receipts. Before `H0`, the source audit must
obtain stable copies and hashes, identify exact theorem/page ranges, map hypotheses and notation to
the chosen root, check errata, and receive independent review.

## Statement-phase decision record required

The next phase must explicitly select the character class and source formulation; record the
number-field hypotheses, conductor, infinity type, gamma factors, completed function, dual, center,
and root number; separate primitive, imprimitive, trivial/polar, and other boundary cases; and show
checked transports for every alternate normalization. Only then may it replace the null canonical
target in `intake.json` with an elaborated Lean expression and environment fingerprint.

No human-proof closure, machine closure, or source fidelity is claimed here.

## Current statement attempt (2026-07-17)

The current rev-5.6 statement attempt did not select either discovery lead as authority. The
repository record still provides only the title, Hecke attribution, 1917 date, and one-line gloss;
Stage0 explicitly leaves exact definitions and premises open. No immutable source bytes, exact
theorem or displayed-formula locator, complete transcription, correction/errata review, or
independent source approval is present in the repository.

The attempt also inspected the distinct target `THM-M-0022`, whose source wording is semantically
indistinguishable and whose owned blocker records the same unresolved Hecke-functional-equation
family. That file is discovery evidence only: the v2 DAG declares no hard edge, reuse hint, or
shared group between the targets, and no accepted alias, deduplication, or canonical-root ownership
decision exists. This target therefore consumes no declaration, receipt, state, or proof credit
from `THM-M-0022`.

`Statement.lean` checks only generic weak/strong functional-equation machinery, the primitive
Dirichlet-character specialization, and number-field adele/product-formula APIs. The legacy
`S1_M_080.lean` module remains an abstract caller-supplied interface. Neither surface defines the
received Hecke character, completed L-function, or source normalization, so neither can serve as
the canonical target or support meaningful mutations. The exact-statement gate remains blocked.
