# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies the title "Killip-Visan theorem", attribution Rowan
Killip/Monica Visan, year 2010, statement "mass-critical NLS", importance high, and the untrusted
label `已验证`. `Docs/Stage0_Blueprint.md` repeats these fields while explicitly leaving definitions,
hypotheses, proof, axioms, and machine status open. No bibliography, theorem number, page, edition,
or errata record is attached. Repository search found no target-specific Lean artifact.

Consequently this intake asserts no primary-source candidate. The phrase identifies a large theorem
family rather than a proposition, and selecting a familiar member would substitute missing
mathematics. The metadata label supplies neither `H0` nor machine-proof credit.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "mass-critical" | scaling-critical regularity is the mass/L2 level | scaling action, mass functional, critical exponent | family indicated; definitions unresolved |
| "NLS" | nonlinear Schrodinger equation family | exact equation, sign, exponent, domain, solution predicate | unresolved |
| Killip / Visan | author attribution | none | insufficient to select a theorem |
| 2010 | approximate bibliographic discriminator | immutable primary-source identity | insufficient without title/theorem/page |
| no conclusion stated | nothing beyond the regime | exact ordered binders, hypotheses, conclusion | canonical target unavailable |
| `已验证` | untrusted repository label | inspectable source and kernel receipts | no credit |

The next gate is primary-source identification and independent verification of the exact theorem.
Only then can a row-by-row mapping to a canonical Lean expression, including degenerate and boundary
cases, be frozen. Anchor search and proof inspection belong to later assigned phases.
