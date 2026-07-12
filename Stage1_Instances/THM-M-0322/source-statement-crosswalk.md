# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names the Krein-Milman theorem, attributes it to Mark Krein and
David Milman, dates it to 1940, and gives only the gloss `紧凸集的端点表示` ("representation of
compact convex sets by extreme points"). `Docs/Stage0_Blueprint.md` repeats this metadata and leaves
the exact definitions, premises, axiom profile, and artifact link open. The manifest carries
`已验证` only in the explicitly untrusted source-status field.

The gloss reliably selects the standard theorem family but is not a pinpoint source. It does not
state the ambient separation convention, scalar field, precise closed-convex-hull encoding, or an
edition/page that can support `H0`.

## Candidate source anchors

- M. Krein and D. Milman, "On extreme points of regular convex sets", *Studia Mathematica* 9
  (1940), 133-138, is the historical primary-paper candidate. Its exact wording, terminology,
  hypotheses, scanned pagination, and errata have not been independently inspected in this intake.
- Barry Simon, *Convexity: An Analytic Viewpoint* (Cambridge University Press, 2011), chapter 8, is
  the modern source cited by the pinned mathlib module. An exact theorem/page and its conventions
  remain to be checked.

These are discovery anchors, not accepted human-proof evidence. The source audit must inspect an
immutable copy, record theorem/page and all assumptions, crosswalk the proof's semantic nodes, check
errata, and obtain independent review.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| compact convex set | `s` compact and real-convex | `IsCompact s`, `Convex Real s` | included; exact expression open |
| locally convex ambient space | real Hausdorff locally convex TVS | `LocallyConvexSpace Real E` plus topology/module continuity instances | candidate API probed |
| extreme points | points not lying in an open segment with endpoints in `s` | `s.extremePoints Real` | candidate API probed |
| convex hull | smallest real-convex set containing the extreme points | `convexHull Real (s.extremePoints Real)` | candidate API probed |
| closed hull / representation | equality after topological closure | `closure (...) = s` | candidate declaration probed |
| `已验证` | untrusted inventory label | no proposition or proof object | rejected as evidence |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Convex.KreinMilman` exposes `closure_convexHull_extremePoints` with the visible
compactness and convexity premises and equality conclusion above. `IntakeProbe.lean` checks the
candidate and its constituent APIs under the pinned toolchain. The later statement phase must
serialize the full elaborated expression and run mutations; the anchor audit must inspect imports,
proof-body provenance, axioms, and exact source fidelity. Nothing in this intake promotes the
candidate to M0 or H0.
