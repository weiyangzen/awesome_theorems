# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Gravitational field equation | A. Einstein, *Die Grundlage der allgemeinen Relativitatstheorie*, Annalen der Physik 49 (1916), 769-822, especially the field-equation development around equations (52)-(53) | Future canonical spacetime predicate | Primary historical source located, but its notation, sign and trace-reversed form have not been transcribed and independently checked: `H2` |
| Modern tensor form with cosmological term | A. Einstein, *Kosmologische Betrachtungen zur allgemeinen Relativitatstheorie*, Sitzungsberichte der Koniglich Preussischen Akademie der Wissenschaften (1917), 142-152 | `Ric - (R/2)g + Lambda g = kappa T` | Primary cosmological-term source located; exact page/equation transcription, edition hash, and convention bridge remain open |
| Einstein tensor definition | Modern normalization of the Ricci and scalar-curvature terms | legacy `S1_M_196.EinsteinTensorAt` | Candidate algebraic encoding only; it accepts preconstructed tensors and is not a checked geometric definition |
| Pointwise field equation | Same equation after evaluation at a point | legacy `S1_M_196.EinsteinFieldEquationAt` | Useful discovery candidate, but not an exact manifold-level target and no rev-5.6 credit is inherited |
| Vacuum, zero cosmological constant | Special case `T = 0`, `Lambda = 0` | legacy `EinsteinFieldEquationAt_vacuum_zeroLambda_iff` | A specialization only; it cannot broaden into or replace the sourced general equation |
| Conservation compatibility | Contracted Bianchi identity together with the field equation implies the convention-appropriate divergence condition on `T` | Future typed bridge obligations | Consequence/compatibility condition, not silently part of the root until the source and matter assumptions are frozen |

The generated phrase does not determine a single proposition. An equation can be a defining law,
a predicate on supplied fields, the Euler-Lagrange equation of an action, or the conclusion of an
existence theorem. Those claims have different binders and proof obligations. This dossier therefore
does not manufacture a canonical theorem from the label.

The statement phase must acquire stable source files and hashes, transcribe the exact equations and
assumptions, audit errata/translation differences, freeze dimension and sign/curvature/unit
conventions, and decide the logical force. It must then inspect and elaborate the actual Lean type,
serialize its normalized expression, check any historical-to-modern and trace-reversal transports,
and mutation-test every binder, hypothesis, matter boundary, and vacuum/cosmological special case.

Discovery identifiers (not immutable evidence receipts): Einstein 1916 DOI
`10.1002/andp.19163540702`; Einstein 1917 bibliographic pages 142-152. No `H0` or machine-closure
claim is made.

