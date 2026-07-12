# Source-statement crosswalk

## Repository record and source candidates

`Docs/researches/math_theorems.md` attributes the item to Ossian Bonnet, dates it to 1867, and gives
only "a surface is determined by its first and second fundamental forms." `Docs/Stage0_Blueprint.md`
repeats that gloss while leaving definitions, hypotheses, proof, axioms, and machine artifacts open.
The `已验证` field is untrusted metadata under rev-5.6.

Two modern source candidates make the intended family identifiable but are not yet accepted `H0`
evidence:

- Manfredo P. do Carmo, *Differential Geometry of Curves and Surfaces*, the chapter on intrinsic
  geometry of surfaces, section "The Fundamental Theorem of the Local Theory of Surfaces."
- Michael Spivak, *A Comprehensive Introduction to Differential Geometry*, volume III, the treatment
  of the fundamental theorem for surfaces via the Gauss and Codazzi equations.

The statement phase must inspect a pinned edition and record an exact theorem/page, definitions,
proof boundary, assumptions, and errata. The historical Bonnet attribution and 1867 date also need
bibliographic verification. The candidates above are discovery anchors, not substitutes for that
work, and no independent source review has occurred.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "first fundamental form" | positive-definite metric coefficients `E,F,G` or a Riemannian metric | concrete metric/bilinear form and positivity | family identified; encoding open |
| "second fundamental form" | symmetric coefficients `e,f,g` with a chosen normal convention | symmetric bilinear form/shape operator | included; sign and regularity open |
| compatibility | Gauss equation plus both Codazzi-Mainardi equations | covariant derivative, curvature, determinant/shape-operator identities | necessary hypotheses identified; exact formulas open |
| "surface" | regular parametrized surface or immersion into Euclidean `R^3` | smooth manifold/domain and concrete immersion | local/global domain open |
| "determined" | existence of a realization and uniqueness modulo rigid motion | existential immersion plus Euclidean-isometry relation | both halves included; exact quantifiers open |
| Bonnet / 1867 | historical attribution | no machine-proof credit | bibliography unverified |

## Lean and evidence boundary

A repository search found no theorem-specific Lean artifact for `THM-M-0160`. The pinned mathlib
tree contains general manifold immersion and Riemannian infrastructure, but the intake search did
not locate a terminal fundamental theorem of surface theory or a concrete second-fundamental-form
API. This is only a local discovery observation, not the exhaustive immutable anchor audit required
by the next phases and not proof that no external formalization exists.

Before `H0`, an independent reviewer must approve the selected edition, theorem/page, all
hypotheses, definitions, sign/orientation conventions, errata, and row-by-row mapping. Before
statement credit, every source component must map to an elaborated Lean expression, including both
existence and uniqueness and all degenerate-case decisions.
