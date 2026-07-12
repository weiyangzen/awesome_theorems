# Source-statement crosswalk

## Repository record and primary-source lead

The repository inventory records Shizuo Kakutani, 1941, and only the gloss “fixed-point theorem for
a set-valued map”. It leaves precise definitions, premises, proof path, foundations, and formal
artifacts unspecified. Its `已验证` value is untrusted under rev-5.6.

The historical primary-source lead is Shizuo Kakutani, *A generalization of Brouwer's fixed point
theorem*, **Duke Mathematical Journal** 8 (1941), 457-459. This intake has identified the paper but
has not independently inspected an immutable scan, exact theorem locator, definitions, or errata.
It is therefore a discovery anchor, not `H0` evidence. A later source review must quote the exact
statement and approve all premise transports.

## Crosswalk

| Repository/source component | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| “set-valued map” | correspondence whose values remain in the domain | `F : K -> Set K` or an ambient-set equivalent | family fixed; encoding open |
| Euclidean convex domain | nonempty closed bounded convex set in finite dimension | `Set.Nonempty`, `IsClosed`, `Bornology.IsBounded`, `Convex`; or checked compact reformulation | exact source wording open |
| nonempty convex values | each image is inhabited and convex | `Set.Nonempty (F x)` and `Convex ℝ (F x)` | included |
| closed/compact values | source-specific regularity of every image | `IsClosed (F x)` or `IsCompact (F x)` plus transport | choice open pending source inspection |
| upper semicontinuity | nearby values lie in neighborhoods of the current value | mathlib `UpperHemicontinuousOn` after definition audit | API located; equivalence not checked |
| fixed point | some point belongs to its image | `∃ x : K, x ∈ F x` | intended conclusion fixed |

## Formalization boundary

Pinned mathlib contains correspondence-level upper hemicontinuity definitions in
`Mathlib.Topology.Semicontinuity.Defs` and supporting results in
`Mathlib.Topology.Semicontinuity.Hemicontinuity`. The narrow name/API search found no Kakutani
fixed-point declaration. This is useful feasibility evidence only, not the later exhaustive anchor
audit and not machine-proof credit.

Before `H0`, an independent reviewer must inspect the primary edition, theorem/page, terminology,
all hypotheses, proof boundaries, and errata. Before statement credit, every approved row must map
to an elaborated Lean expression, with checked transports for closed-bounded versus compact and for
the selected upper-semicontinuity convention.
