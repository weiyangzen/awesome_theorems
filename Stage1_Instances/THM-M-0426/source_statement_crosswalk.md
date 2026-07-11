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

