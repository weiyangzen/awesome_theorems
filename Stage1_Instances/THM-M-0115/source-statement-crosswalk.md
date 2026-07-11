# THM-M-0115 Source-Statement Crosswalk

This is an intake crosswalk, not an `H0` source audit. Pinpoint page verification, editions, errata,
and independent review remain open under `S56-M-0115-ANCHOR_AUDIT`.

| Canonical component | Primary-source anchor | Intake mapping | Open verification |
|---|---|---|---|
| General GRR transformation and proper covariance | A. Grothendieck, *Classes de faisceaux et theoreme de Riemann-Roch*, in SGA 6, Lecture Notes in Mathematics 225, Springer (1971), Expose 0 | Historical general source for the Riemann-Roch transformation | exact theorem/page, edition scan, assumptions, errata |
| Proper morphism of nonsingular quasi-projective varieties | W. Fulton, *Intersection Theory*, 2nd ed., Springer (1998), Chapter 15, Section 15.2, Grothendieck-Riemann-Roch theorem | Chosen classical scope for this instance | exact theorem number/page and base-field conventions |
| `ch(f_* alpha) td(T_Y) = f_*(ch(alpha) td(T_X))` | Fulton, Chapter 15, Section 15.2 | Direct source shape for the frozen equality | notation-level check against print edition |
| Rational Chow target and Todd factors | Fulton, Chapters 3 and 15 | Fixes codomain and characteristic-class interpretation | grading/completion conventions and any denominators |

The repository's legacy description, "Riemann-Roch formula for schemes", is broader and too vague
to be the executable root. This intake does not treat that metadata or its untrusted `verified`
label as proof evidence. The selected classical formulation must be checked against the cited
edition before statement acceptance; any correction requires an explicit scope delta rather than a
quietly broadened theorem.
