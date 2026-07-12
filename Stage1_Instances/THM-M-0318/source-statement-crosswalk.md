# Source-statement crosswalk

## Primary source candidate

Juliusz Schauder, "Der Fixpunktsatz in Funktionalraumen," *Studia Mathematica* **2** (1930),
171-180, is the historical primary-paper candidate. This dossier records only the bibliographic
identification. A stable scan, the exact theorem/page, original hypotheses and terminology, and any
errata have not been inspected, so the citation is `H2` discovery evidence rather than `H0` source
fidelity evidence.

A modern reference must also be selected during source audit to disambiguate the commonly named
compact-convex form from the closed-convex/relatively-compact-image and locally convex variants.
No modern book theorem is treated as inspected evidence in this intake.

## Crosswalk

| Repository/source phrase | Frozen mathematical meaning | Planned Lean component | Intake status |
|---|---|---|---|
| "Schauder fixed-point theorem" | compact-convex fixed-point existence | one canonical proposition | included; exact source form open |
| "Banach space" | ambient real normed space in Stage0 wording | normed-space typeclasses | completeness intentionally not frozen |
| nonempty compact convex set | domain on which topological approximation acts | `K.Nonempty`, `IsCompact K`, `Convex Real K` | vocabulary checked |
| continuous self-map | continuity on `K` and preservation of `K` | `ContinuousOn f K`, `Set.MapsTo f K K` or subtype map | encoding choice open |
| fixed point | an element of `K` fixed by `f` | `Exists fun x => x in K and f x = x` | human conclusion frozen |

## Source and theorem boundaries

The Stage0 line "a fixed-point theorem on Banach spaces" is too weak to determine the theorem:
compactness, convexity, nonemptiness, continuity, and the self-map condition are essential scope
information. Conversely, completeness of the ambient space is unnecessary in the standard
compact-subset formulation and must be retained only if the inspected source requires it.

Before `H0`, an independent reviewer must inspect the stable primary-source copy and record the
edition/scan identity, theorem and page, definitions, every hypothesis, conclusion, errata search,
and a row-by-row source-to-Lean mapping. Before machine credit, anchor audit must search the pinned
mathlib environment for an exact terminal theorem and distinguish the unrelated Schauder-basis API.
