# Source-statement crosswalk

## Repository source

`Docs/Stage0_Blueprint.md` names the target "cup product" and gives only "the structure of the
cohomology ring" as theorem content. It supplies no quantified proposition, coefficient convention,
or bibliographic theorem anchor. The manifest's `source_status_untrusted` value is metadata and is
not evidence that any particular statement has been proved or formalized.

## Source candidates

- J. W. Alexander, *On the Chains of a Complex and Their Duals*, Proceedings of the National
  Academy of Sciences 21 (1935), 509-511. This is a historical primary-source candidate for the
  product construction; the exact scope and wording have not yet been inspected in this intake.
- Hassler Whitney, *On Products in a Complex*, Annals of Mathematics, second series, 39 (1938),
  397-432. This is a historical primary-source candidate for the product and its laws; the exact
  theorem/page, assumptions, and errata have not yet been audited.
- Allen Hatcher, *Algebraic Topology* (2002), section 3.2, "Cup Product". This is a stable modern
  exposition candidate for selecting a precise theorem family, not a replacement for inspecting a
  primary source. Exact proposition/theorem anchors and edition pagination remain open.

These citations establish discovery provenance only. They do not clear `H0`; doing so requires
inspection of a fixed edition, exact theorem/page anchors, all assumptions and definitions, errata,
and independent review.

## Crosswalk

| Repository/source phrase | Frozen intended component | Required Lean object or proposition | Intake status |
|---|---|---|---|
| "cup product" | multiplication of degree `p` and `q` classes | cochain construction descending to `H^(p+q)` | included; API and encoding open |
| "cohomology ring" | direct sum/graded family with multiplication | bundled or componentwise graded-ring structure | included; bundling open |
| product law | associativity | equality on cohomology classes | included; proof source open |
| ring unit | class of the constant `1` cochain in degree zero | left/right unit laws | included; empty/reduced conventions open |
| graded structure | degree of a product is `p + q` | typed degree-additive multiplication | included |
| commutativity | `a cup b = (-1)^(p*q) (b cup a)` | signed equality for homogeneous classes | included; sign encoding open |
| functorial structure | pullback preserves products and unit | naturality under a continuous map | included; root bundling open |

## Exactness blockers

The source label denotes an operation and a family of structural results, not one uniquely scoped
theorem. Consequently there is no honest canonical Lean declaration or expression hash at intake.
The statement phase must resolve the source edition and theorem boundary, then map each assumption
and conclusion row to a concrete Lean expression. A wrapper that takes the multiplication or its
laws as hypotheses is not an acceptable transport or proof of this target.
