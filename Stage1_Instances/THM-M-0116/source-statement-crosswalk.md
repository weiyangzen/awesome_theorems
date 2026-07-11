# Source-statement crosswalk

| Claim component | Source anchor | Frozen target component | Intake finding |
|---|---|---|---|
| Historical finite-basis theorem | F. Severi, *La base minima pour la totalite des courbes tracees sur une surface algebrique*, Ann. Sci. Ecole Norm. Sup. (3) 25 (1908), 449-468 | finite generation for divisor classes on an algebraic surface | Primary historical candidate located; terminology and hypotheses require edition-level audit before H0 |
| Modern Neron-Severi group | S. Kleiman, "The Picard scheme", in *Fundamental Algebraic Geometry: Grothendieck's FGA Explained*, AMS, 2005, chapter 9 | `NS(X) = Pic(X) / Pic^0(X)` and finite generation | Modern source candidate; exact proposition/page and equivalence with the divisor quotient remain to be pinned |
| Base and geometry | algebraically closed `k`; smooth projective surface `X/k` | ordered domain/hypothesis block | Matches the narrow Stage0 wording; historical source may use different ground-field assumptions |
| Equivalence relation | algebraic equivalence of divisors | quotient defining `NS(X)` | Must not be weakened to numerical equivalence or strengthened to equality in `Pic(X)` |
| Conclusion | finite generation | `Module.Finite Z NS(X)` or an equivalent group predicate | Lean representation is intentionally deferred until the statement phase |

The repository's Chinese label translates literally as the "Severi group finite-generation
theorem" and Stage0 expands it as finite generation of the Neron-Severi group of an algebraic
surface. That expansion is the controlling repository claim. The two cited works are discovery
anchors, not accepted evidence receipts: exact scans/editions, page-level premise mapping,
corrections or errata, and independent review are outstanding. Consequently the human-source state
is `H2`, not `H0`.

No Lean/mathlib theorem is asserted here. Searching, pinning, type inspection, and terminal-body
provenance belong to the later statement and anchor-audit nodes.
