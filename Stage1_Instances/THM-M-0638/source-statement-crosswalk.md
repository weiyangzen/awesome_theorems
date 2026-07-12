# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` records the Chinese title `吉洪诺夫不动点定理`, attributes it
to Andrey Tychonoff, dates it to 1935, and gives only `局部凸空间上的不动点` ("a fixed point on
a locally convex space"). `Docs/Stage0_Blueprint.md` repeats that metadata while leaving exact
definitions, premises, proof path, axioms, and formal artifacts open. Under rev-5.6, the inherited
`已验证` value is `source_status_untrusted`; it is neither source-fidelity nor machine evidence.

The repository contains a second record, `THM-M-0317`, with the same title, author, year, and an
equivalent gloss, but categorized under functional analysis rather than point-set topology. The
catalog does not explain whether these IDs are intentional aliases or an accidental duplicate.
Their evidence and state therefore remain separate until the integration lane makes an explicit
scope decision.

## Inspected primary-source lead

A. Tychonoff, "Ein Fixpunktsatz," *Mathematische Annalen* **111** (1935), 767-776,
DOI `10.1007/BF01472256`. Crossref confirms the author, title, journal, volume, issue, date, and
page range. A stable Goettingen digitization has work ID `PPN235181684_0111`; canvas `00000774`
is printed page 770 and contains section 2's theorem:

> Bei jeder stetigen Abbildung einer konvexen, bikompakten Menge eines linearen topologischen
> lokal-konvexen Raumes in sich gibt es wenigstens einen Fixpunkt.

This says that every continuous self-map of a convex compact subset of a locally convex
topological linear space has at least one fixed point. The repository-local `THM-M-0317` statement
receipt records an inspection of pages 767-770 and a Lean-facing interpretation with real scalars,
Hausdorff separation, continuous vector operations, explicit nonemptiness, and an in-domain fixed
point. That receipt and source scan are discovery inputs here, not an accepted source review or
state transfer for `THM-M-0638`.

## Crosswalk

| Source component | Candidate mathematical meaning | Candidate Lean component | Intake status |
|---|---|---|---|
| linear topological space | real vector space with continuous addition and scalar multiplication | `AddCommGroup E`, `Module ℝ E`, `TopologicalSpace E`, `IsTopologicalAddGroup E`, `ContinuousSMul ℝ E` | source family located; exact adopted binder context open |
| locally convex | convex-neighborhood basis at zero | `LocallyConvexSpace ℝ E` | pinned API probed; definition transport awaits review |
| source separation convention | Hausdorff/regular ambient topology in the paper's setup | at least `T2Space E` if confirmed | candidate only; independent definition review open |
| convex compact set | invariant domain of the self-map | `Convex ℝ K`, `IsCompact K`, and explicit `K.Nonempty` | family located; nonempty translation must be approved |
| continuous self-map | continuous map whose image remains in the domain | `Continuous f` plus `Set.MapsTo f K K`, or a continuous subtype map | encoding and continuity scope open |
| at least one fixed point | a domain member mapped to itself | `∃ x ∈ K, Function.IsFixedPt f x` | intended family conclusion; no canonical expression yet |
| `THM-M-0317` duplicate | same named/source theorem in a different category | no automatic Lean transport or receipt transfer | identity review required before statement acceptance |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

## Source-fidelity boundary

Before `H0` or exact-statement credit, a reviewer independent of this intake must preserve or pin a
lawful stable source copy, verify the theorem and all incorporated definitions, confirm the scalar
and separation conventions, decide how source nonemptiness maps to mathlib, record the proof
boundary and an errata search, review the translation, and approve every source-to-Lean row. The
integration lane must also decide whether `THM-M-0638` and `THM-M-0317` are one duplicated target
or genuinely distinct instances; until then, neither may inherit the other's accepted state.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks the candidate vocabulary from `Mathlib.Topology.Algebra.Module.LocallyConvex` and
`Mathlib.Dynamics.FixedPoints.Basic`. A bounded name and vocabulary search found component APIs,
one-dimensional and contraction special cases, and compact-product Tychonoff results, but no exact
compact-convex locally-convex fixed-point theorem. This is intake discovery only, not the immutable
candidate audit required by `S56-M-0638-ANCHOR_AUDIT` and not proof credit.
