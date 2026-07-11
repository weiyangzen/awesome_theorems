# Source-statement crosswalk

| Claim component | Source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Screened entry | `Docs/researches/math_theorems.md`, "Euler方程": Euler, 1757, "理想流体的运动方程" | none | Repository source supplies a subject, not a proposition |
| Modern momentum equation | `Docs/researches/physics_theorems.md`, fluid mechanics item 4: `rho(Dv/Dt) = -grad P + rho g` | none | An equation schema; variables, domain, regularity, and asserted conclusion are absent |
| Historical source | L. Euler, *Principes généraux du mouvement des fluides*, Mémoires de l'Académie Royale des Sciences et Belles-Lettres de Berlin 11 (published 1757), pp. 274-315 | none | Primary work identified for discovery; edition/hash, pinpoint equation mapping, assumptions, and errata review are not accepted |
| Distinct PDE theorems | Adjacent repository entries for Beale-Kato-Majda, Yudovich, and Wolibner | separate future targets | Explicitly excluded from this target; using one would substitute the theorem |

## Missing statement decisions

An exact claim requires, at minimum: compressible or incompressible regime; spatial dimension and
domain; time interval; scalar field; density and pressure laws; body force; initial/boundary data;
solution concept and regularity; and a proposition-level conclusion. For example, merely encoding
the displayed momentum equality as a hypothesis and concluding the same equality would be a
tautological wrapper, not a formalization of a mathematical theorem.

The historical formulation may support a derivation claim from balance principles, while modern
analysis supports existence, uniqueness, conservation, or regularity claims. Those are not
interchangeable. Until an authoritative source selects one, there is no canonical statement and no
source-to-binder crosswalk to credit.

No `H0` or machine-closure claim is made. Required follow-up is a scan of a stable primary-source
edition, a page/equation-level crosswalk into modern notation, an explicit proposition choice, and
independent review of that choice before the Lean statement gate.
