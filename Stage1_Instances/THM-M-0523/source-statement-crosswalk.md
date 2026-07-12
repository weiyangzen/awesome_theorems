# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` contains two records named `马宁-德林费尔德定理`. The record
corresponding to `THM-M-0523` attributes it to Yuri Manin and Vladimir Drinfeld, dates it to 1973,
and gives only `椭圆曲线上Heegner点的性质` ("properties of Heegner points on elliptic curves").
`Docs/Stage0_Blueprint.md` repeats that wording and explicitly leaves definitions, assumptions,
proof path, axioms, and machine artifacts open. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted`.

The repository also has duplicate ID `THM-M-0124` with the same name and essentially the same
gloss. Its historical `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_043.lean` instead describes
the standard cusp-difference torsion statement. The file labels itself a statement-shape boundary,
uses abstract compactified-curve and divisor-class interfaces, and explicitly says that it does not
prove Manin-Drinfeld. Under rev-5.6 it is a discovery lead only.

## Primary-source identification still required

The named theorem is conventionally associated with independent work of Manin and Drinfeld on
cuspidal divisor classes of modular curves. Intake did not accept a particular edition, theorem
number, page, translation, assumptions, or errata record. The source phase must obtain and
independently review those pinpoint details before assigning `H0` or freezing the exact range of
modular curves. General mathematical familiarity and the legacy Lean commentary are not primary
source evidence.

## Crosswalk

| Repository/source phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Manin-Drinfeld theorem" | conventionally, torsion of degree-zero cusp divisor classes | concrete modular curve, cusps, divisor class, Jacobian/`Pic^0`, torsion | candidate named-theorem reading |
| "Heegner points on elliptic curves" | a different arithmetic topic | CM/Heegner point construction and a specified property | conflicts with theorem name; no proposition supplied |
| "modular curve" | curve attached to a congruence subgroup | source-fixed compactified modular-curve object | absent from pinned mathlib probe |
| "cusps" | boundary points/cusp orbits | `IsCusp`, `CuspOrbits` | pinned APIs probed |
| "difference of cusps" | degree-zero divisor `[c]-[d]` | divisor and divisor-class map | concrete API not identified |
| "torsion" | some nonzero integer/natural multiple is zero in `J` or `Pic^0` | additive finite-order predicate on concrete target | target object not identified |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.NumberTheory.ModularForms.Cusps`. It checks arithmetic-subgroup, cusp,
cusp-orbit, and finiteness APIs. A scoped source search found no `Manin-Drinfeld` or cuspidal-divisor
declaration in pinned mathlib. This is encoding reconnaissance only, not the later immutable anchor
audit and not a proof. The legacy file's abstract structures must not be mistaken for concrete
algebro-geometric constructions.
