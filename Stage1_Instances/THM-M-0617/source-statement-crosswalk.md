# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4580-4585` supplies exactly the title `紧致性定理`, attribution
to many mathematicians, the nineteenth century, the gloss `紧集的闭子集紧，连续像紧`, importance
"high," and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, theorem locator,
formula, definitions, binder order, assumption list, proof boundary, corrections, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:16882-16907` repeats the gloss while explicitly leaving the formal
system, foundations, precise definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. Its generic statement that closure is known is
planning metadata. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and
resets this target to `L0 / rework_required`.

The model-theory entry at `Docs/researches/math_theorems.md:4775-4780` has the same title but says
that a theory has a model exactly when every finite subset does. It is `THM-M-0644` and is an
explicit non-source for this point-set-topology target.

## Human-source discovery boundary

The repository's broad nineteenth-century attribution is not a source. A modern general-topology
text is expected to contain complete proofs of both preservation results, and James R. Munkres,
*Topology*, second edition, Section 26 is a bibliographic discovery candidate. This worker did not
obtain and inspect an immutable lawful copy, so no theorem numbers or pages are asserted here.
No primary historical edition, complete modern theorem passage, definition chain, assumption map,
proof transition map, translation, correction or errata audit, or independent review is admitted.

This supports only provisional `H1`: the classical results are published and believed complete,
but their exact source-to-catalog statement and assumptions are not accepted. Before `H0`, an
accountable reviewer must pin and inspect a source edition, record exact theorem/section/page or
archival locators for both clauses and every incorporated definition, map assumptions and proof
steps, audit corrections, and independently approve the mapping.

## Literal clause crosswalk

| Repository component | Mathematical meaning | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| `紧集` | a compact subset `s` of an arbitrary topological space, without separation built into compactness | `IsCompact s` | direct concept located; exact source definition and target binder open |
| `闭子集` | an ambient-closed set `t` contained in `s`, or a source-approved equivalent subspace encoding | `IsClosed t` and `t ⊆ s` | `IsCompact.of_isClosed_subset` is a direct candidate; encoding transport open |
| first `紧` | compactness of `t` | `IsCompact t` | candidate conclusion located; no root or body credit |
| `连续像` | image of compact `s` under a continuous map into another topological space | `Continuous f` and `f '' s` | `IsCompact.image` is a direct candidate; binder and continuity convention open |
| second `紧` | compactness of the image | `IsCompact (f '' s)` | candidate conclusion located; no root or body credit |
| comma joining clauses | both independent preservation results belong to one catalog root | conjunction or checked composition of two children | packaging and expression fingerprint open |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H or M credit |

## Pinned formal-candidate boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.Compactness.Compact`, declares:

| Declaration | Candidate type summary | Boundary |
|---|---|---|
| `IsCompact.of_isClosed_subset` | compact `s`, closed `t`, and `t ⊆ s` imply compact `t` | direct first-clause interface; source identity, exact root composition, body provenance, and trust acceptance open |
| `IsCompact.image` | compact `s` and globally continuous `f` imply compact `f '' s` | direct second-clause interface; independent binder scope and source identity open |
| `IsCompact.image_of_continuousOn` | compact `s` and continuity on `s` imply compact `f '' s` | related stronger-local interface; not silently substituted for global continuity |

The file works over arbitrary `TopologicalSpace X` and `TopologicalSpace Y`; it does not require
Hausdorff spaces for either preservation result. `IntakeProbe.lean` checks the interfaces and their
reported axioms only. It neither declares the catalog root nor inspects terminal body provenance.
These usable statement interfaces justify provisional `M3`, not M0 and not the later exhaustive
anchor audit.

## Open source and statement gates

Source review must preserve both independent clauses and settle all definitions, assumptions,
incorporated results, locators, history, and errata. Statement work must then freeze minimal
imports, universes and ordered binders, the two exact clauses and root packaging, an elaborated
expression and environment fingerprint, checked alternate transports, and the required removed-
hypothesis, changed-domain, binder-scope, and boundary mutations. No proof evidence may be credited
before those gates pass.
