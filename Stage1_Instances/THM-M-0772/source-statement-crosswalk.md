# Source-statement crosswalk

## Repository record and primary-source boundary

The repository source inventory (`Docs/researches/math_theorems.md`) attributes the principle to
Felix Hausdorff, dates it to 1914, and states: "a maximal chain exists in a partially ordered set."
The Stage0 projection repeats "existence of a maximal chain in a partially ordered set." Its
`已验证` label is untrusted metadata under rev-5.6 and supplies neither human-proof nor kernel credit.

The historical primary-source candidate is Felix Hausdorff, *Grundzüge der Mengenlehre* (1914).
This intake has not inspected an immutable scan to identify the exact section/page, terminology,
hypotheses, proof boundaries, or later errata. It is therefore only a discovery candidate. Before
`H0`, an independent reviewer must inspect a fixed edition and approve the exact locator,
assumptions, proof, translation of terminology, and row-by-row mapping below.

## Crosswalk

| Repository/source phrase | Frozen mathematical meaning | Required Lean component | Intake status |
|---|---|---|---|
| "partially ordered set" | a carrier with reflexive, antisymmetric, transitive `≤` | `P : Type u` and `[PartialOrder P]` | included; binder freeze open |
| "chain" | a subset whose distinct elements are comparable | `IsChain (· ≤ ·) c` | pinned definition found |
| "maximal chain" | no strictly larger chain contains it | `IsMaxChain (· ≤ ·) c` | intended conclusion frozen |
| "exists" | at least one such subset, without uniqueness | `∃ c : Set P, ...` or checked constructed witness | encoding decision open |
| Hausdorff / 1914 | historical attribution and source locator | no machine credit | exact primary locator open |

## Pinned Lean discovery candidate

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Order.CompleteLattice.Chain` describes itself as proving Hausdorff's maximality principle.
It exports `maxChain_spec` with a witness `maxChain r` and result `IsMaxChain r (maxChain r)` for an
arbitrary relation `r`. The underlying `IsMaxChain` definition in
`Mathlib.Order.Preorder.Chain` pairs chainhood with equality against every containing chain.

This is strong local discovery evidence, but not statement or proof acceptance. The later statement
phase must record the exact elaborated expression and partial-order specialization. The anchor audit
must inspect imports, axioms, terminal body provenance, license, and transitive dependency closure;
the existence of a declaration name alone cannot clear `M4`.

## Proposition-changing distinctions

The source mapping must distinguish an inclusion-maximal chain from a maximum-cardinality chain and
from a maximal element of the underlying poset. It must also distinguish bare existence from the
extension formulation "every chain is contained in a maximal chain." Although standard treatments
show these formulations equivalent under choice, that equivalence must be explicitly sourced and
checked if used as a transport rather than silently assumed.
