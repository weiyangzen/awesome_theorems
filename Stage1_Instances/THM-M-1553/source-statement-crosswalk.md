# Source-statement crosswalk

## Candidate primary sources

- Ryogo Hirota, "Exact Solution of the Korteweg-de Vries Equation for Multiple Collisions of
  Solitons", *Physical Review Letters* 27 (1971), 1192-1194. This is the historical source candidate
  associated with the repository's 1971 date; the exact displayed equations, hypotheses, and any
  corrections have not yet been checked against a stable copy.
- Ryogo Hirota, *The Direct Method in Soliton Theory*, Cambridge Tracts in Mathematics 155,
  Cambridge University Press (2004), KdV/bilinear-method chapters. This is a candidate authoritative
  exposition, not yet an exact theorem/page anchor.

These citations are discovery anchors only and do not establish `H0`. Source inspection must also
decide whether the published presentation states a theorem with analytic hypotheses or performs a
formal differential calculation; the Lean theorem may need to make implicit regularity explicit.

## Crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "integrable systems" | first instance is KdV only | concrete KdV residual | included; universal reading excluded |
| "bilinear method" | KdV tau substitution and forward bridge | derivatives, `log`, Hirota polynomial | included; exact encoding open |
| bilinear equation | `(D_x^4 + D_x D_t) tau . tau = 0` | concrete diagonal operator identity | convention provisional pending source |
| nonlinear equation | `u_t + 6 u u_x + u_xxx = 0` | pointwise equality on fixed domain | convention provisional pending source |
| soliton solutions | explicit tau family plus dispersion | parameter type and proved identities | separate corollary, not assumed |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_212.lean` is discovery evidence. It contains the
same provisional KdV conventions and useful bilinear-map lemmas. However,
`KdVHirotaDifferentialData` bundles abstract linear maps, while `HirotaBilinearData.Certificate`
requires the decisive admissibility, bilinear identity, and bilinear-to-nonlinear facts as fields.
Thus `Certificate.conclusion` is certificate plumbing, not closure of the source result. The file
must be re-audited at the pinned revision and cannot supply statement or proof credit at intake.

Before `H0`, an independent reviewer must check edition, equation numbers/pages, all implicit
analytic assumptions, normalization, errata, and the complete row-by-row source-to-Lean mapping.
