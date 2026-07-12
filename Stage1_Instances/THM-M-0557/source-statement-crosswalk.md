# Source-statement crosswalk

## Repository record and source candidates

The repository inventory supplies only the label "homotopy groups", the attribution Witold
Hurewicz, the year 1935, and the phrase "higher homotopy groups of topological spaces". Its
`已验证` field is untrusted under rev-5.6. It supplies no theorem locator, dimension convention,
map model, group law, or conclusion, so it does not identify an exact proposition.

A historical primary-source candidate is Witold Hurewicz's 1935 paper series *Beitraege zur
Topologie der Deformationen*, beginning in **Proceedings of the Koninklijke Nederlandse Akademie
van Wetenschappen** 38. This intake has not inspected a pinned scan or identified the exact part,
page, terminology, and proposition corresponding to the repository phrase. The series is therefore
a discovery candidate, not `H0` evidence.

A modern theorem-source candidate is Allen Hatcher, *Algebraic Topology* (2002), Section 4.1,
"Homotopy Groups". It provides stable modern definitions and theorem locators to inspect, but it is
secondary to the historical attribution and has not yet received edition/page/errata or independent
source review here. Neither candidate currently grants human-source acceptance.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "topological spaces" | pointed space and any separation/connectedness assumptions | type, topology, basepoint, explicit typeclasses | domain family identified; hypotheses open |
| "higher" | exact dimension range and treatment of `pi_0`/`pi_1` | ordered natural-number binders and inequalities | proposition-critical range open |
| homotopy classes | based maps modulo based homotopy | sphere/loop maps, based homotopy, quotient/setoid | model open |
| "groups" | well-defined multiplication, unit, inverse, and laws | concrete operation and `Group` instance/theorem | intended construction identified; exact root open |
| higher commutativity | abelianness in the selected range | `CommGroup` result or checked equivalent | candidate conclusion; source locator open |
| naturality/invariance | maps induced by pointed maps and equivalences | homomorphism, identity/composition, equivalence transport | inclusion in root unresolved |
| Hurewicz / 1935 | historical attribution | no kernel-proof credit | exact paper part and locator open |

## Human and machine boundary

Repo-local discovery found adjacent use of `Mathlib.Topology.Homotopy.HomotopyGroup` in the legacy
Adams spectral-sequence file, including the type alias `HomotopyGroup.Pi`. That file belongs to a
different theorem and provides neither source identity nor proof credit for this target. Intake is
not the prescribed exhaustive anchor audit, so no claim is made here about exact mathlib closure or
external Lean projects.

Before `H0`, an independent reviewer must inspect an immutable source edition, identify an exact
theorem/definition and pages, map every premise and conclusion, check terminology and corrections,
and approve the row-by-row mapping. Before statement credit, the selected claim must map to an
elaborated Lean expression without replacing group construction by a pre-existing instance or
silently changing based maps, dimension range, or commutativity.
