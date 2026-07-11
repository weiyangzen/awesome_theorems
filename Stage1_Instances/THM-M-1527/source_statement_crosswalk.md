# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository claim: "fundamental equations of electromagnetism" | `Docs/Stage1_Blueprint.md`, `S1-M-195` | none | Metadata description only; it supplies no quantifiers, conventions, hypotheses, or conclusion |
| Four macroscopic equations in SI notation | J. D. Jackson, *Classical Electrodynamics*, 3rd ed. (Wiley, 1998), section 6.1, equations (6.1)-(6.4) | vector fields with divergence, curl, and time derivative | Concrete published reference candidate, but edition pages, assumptions, constitutive choices, and errata are not yet accepted |
| Covariant exterior-calculus formulation | C. W. Misner, K. S. Thorne, J. A. Wheeler, *Gravitation* (Freeman, 1973), chapters 3-4 | differential forms `F`, `J`, exterior derivative, metric Hodge star | Candidate mathematical model; exact normalization/sign crosswalk remains open |
| Historical source | J. C. Maxwell, *A Treatise on Electricity and Magnetism*, 1st ed. (Clarendon Press, 1873), volume II, Part IV | no direct Lean candidate | Historical formulations are not textually identical to the modern four-equation package; useful for genealogy, not an exact root without audit |
| Covariant-to-3+1 equivalence | Must be reconstructed from a convention-compatible source presentation | prospective theorem over a Lorentzian 4-manifold plus splitting data | Selected provisional theorem family; no checked bridge or exact Lean API identified |
| Charge conservation | Exterior derivative of the sourced Maxwell equation and `d^2 = 0` | `d J = 0` | Consequence only; cannot substitute for the root equivalence |
| Vacuum electromagnetic wave equation | Maxwell system with zero sources plus flat-spacetime identities | wave equations for electric/magnetic fields | Consequence under stronger hypotheses; explicitly outside the root |

The repository title names an equation system, not a truth-valued theorem. A formal target must
therefore state either satisfaction inside an axiomatized model or a genuine derived relationship.
This intake chooses the covariant-to-3+1 equivalence only provisionally because it preserves all
four named equations while yielding a mathematical proposition. The statement phase must reject
or finalize it using a pinpoint source and must freeze signature, units, Hodge-star orientation,
source normalization, regularity, and splitting data before elaboration.

No `H0` claim is made. Jackson, Misner-Thorne-Wheeler, and Maxwell are discovery anchors rather than
immutable evidence receipts. Required follow-up includes exact edition/page or equation images,
file hashes, assumption-to-binder mapping, correction/errata search, and independent review.
