# Source-statement crosswalk

The full repository claim is `上积与斯廷罗德运算的关系` ("the relationship
between the cup product and Steenrod operations"). The crosswalk below keeps
that wording distinct from conventional refinements that still require direct
primary-source audit.

| Claim component | Human source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Repository root: cup product/Steenrod-operation relation | `Docs/researches/math_theorems.md`, entry `卡当公式`; reproduced in `Docs/Stage0_Blueprint.md` as `THM-M-0550` | None selected | Authoritative local wording, but too terse to determine one proposition |
| Mod-2 component product formula | N. E. Steenrod, *Products of cocycles and extensions of mappings*, Annals of Mathematics 48 (1947), 290-320 | Candidate `Sq^n(x cup y) = sum_{i+j=n} Sq^i(x) cup Sq^j(y)` | Primary historical paper identified for audit; exact formula/page, notation, premises, and corrections are not yet pinned |
| Cartan's systematic treatment of cohomology operations | H. Cartan, *Seminaire Henri Cartan 1954/55: Algebres d'Eilenberg-Mac Lane et homotopie* | No formal target | Primary seminar source family identified; exposé/formula pinpoint and edition hash remain open |
| Total-square multiplicativity | Obtained conventionally by collecting all component identities in a completed or degreewise finite graded object | Candidate total-operation encoding | Not credited as equivalent until the formal carrier, finiteness, and component extraction maps are fixed and checked |
| Odd-prime reduced-power product formula | Classical Steenrod reduced-power theory | Unselected analogue | The local phrase says operations in the plural but does not choose a prime; this cannot be merged with the mod-2 root without a source decision |
| Cup-product and operation substrates in Lean | Repository-local and pinned-mathlib search deferred to the anchor-audit phase | None | No theorem name, wrapper, external project, or historical label receives proof credit at intake |

The source wording rules out Cartan's homotopy formula
`L_X = d i_X + i_X d`, despite the shared name. It does not resolve the
remaining distinctions between squares, reduced powers, component formulas,
and total operations. Those distinctions change coefficients, degrees, signs,
and often the formal type, so choosing among them belongs to the exact
statement gate.

Bibliographic locators above are discovery anchors, not immutable evidence
receipts. No `H0` claim is made. `H1` records a classical proved theorem family
with primary sources identified, while exact edition hashes, formula/page
pinpoints, assumptions, translation, errata/corrections, source-to-node mapping,
and independent review remain outstanding.
