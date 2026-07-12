# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` identify Andrey Tychonoff, 1935,
and only the phrase "a fixed-point theorem on a locally convex space." The manifest repeats the
Chinese theorem name and marks the inherited source status as untrusted. These metadata identify a
theorem family, not an exact proposition and not machine evidence.

## Historical primary source candidate

A. Tychonoff, "Ein Fixpunktsatz," *Mathematische Annalen* **111** (1935), 767-776,
DOI `10.1007/BF01472256`. The bibliographic identity, journal volume, year, and page range were
checked against the Crossref record on 2026-07-12. The article's theorem text, definitions,
separation hypotheses, proof nodes, and errata have not yet been inspected, so this is not `H0`.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Expected Lean component | Intake status |
|---|---|---|---|
| locally convex space | ambient topological vector space | `LocallyConvexSpace R E` plus required topology/module classes | included; separation profile open |
| compact convex domain | invariant domain of the map | `IsCompact K`, `Convex R K`, `K.Nonempty` | included; exact source conventions open |
| continuous self-map | map preserves the domain and is continuous | `Continuous f` and `Set.MapsTo f K K`, or a continuous subtype map | included; encoding open |
| fixed point | a point of the domain fixed by the map | `exists x, x in K and Function.IsFixedPt f x` | included |

## Fidelity and review boundary

The statement phase must inspect a stable copy of the article and record the exact theorem/page,
notation, all assumptions, definitions imported by reference, and any errata. It must then reconcile
the classical modern formulation above with Tychonoff's wording rather than silently upgrading or
weakening it. An independent reviewer must approve that row-by-row map before `H0` is possible.

Pinned-mathlib name searches during intake found the component APIs but no declaration named for
Tychonoff/Tikhonov or a compact-convex locally-convex fixed-point theorem. This bounded search is
not the immutable, exhaustive candidate audit required by `S56-M-0317-ANCHOR_AUDIT`.
