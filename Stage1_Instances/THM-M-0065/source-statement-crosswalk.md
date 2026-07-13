# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:484-489` supplies exactly the title `若尔当-赫尔德定理`,
attribution to Camille Jordan and Otto Holder, the year 1889, the gloss
`群的合成列在同构意义下唯一` ("a group's composition series is unique up to isomorphism"),
importance "high," and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, edition,
theorem locator, definitions, ordered binders, hypotheses, conclusion, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:1893-1918` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 target manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected modern source lead

J. S. Milne, *Group Theory*, version 4.01 (2025), author-hosted PDF observed on
2026-07-13, was inspected. In Section 6:

- Definition 6.1, printed page 87, defines a subnormal series as a descending chain from `G` to
  `{1}` with each term normal in its predecessor. A composition series has no proper subnormal
  refinement, equivalently every factor is nontrivial and simple.
- Theorem 6.2, printed pages 88-89, states for a finite group that any two composition series have
  equal lengths and that a permutation matches their quotient groups up to isomorphism. A complete
  induction proof follows.
- Remark 6.3(a), printed page 89, extends the result to any possibly infinite group possessing a
  finite composition series.

The observed PDF SHA-256 is
`826a86c9faebaa3a8f398655da515a0ee8cd922a05787fdc3a1f21a16db73633`. The copy is a mutable
author-hosted source lead and was not added to the repository. Its front matter is dated November 6
while the revision history says November 7. The catalog does not cite it; its correction history
was not audited; choosing finite-group Theorem 6.2 or the conditional arbitrary-
group extension changes the target; and no independent source reviewer has approved the mapping.
Thus it supports provisional `H1`, not `H0`.

Otto Holder's 1889 paper *Zurückführung einer beliebigen algebraischen Gleichung auf eine Kette
von Gleichungen*, *Mathematische Annalen* **34**, 26-56, DOI `10.1007/BF01446791`, was identified
as a historical primary lead from publisher/Crossref metadata. The publisher reference list cites
Jordan's 1870 treatise at pages 269-270. The article body was not openly accessible in this bounded
intake, so no exact passage, transcription, assumptions, proof, translation, or correction history
was inspected or credited.

## Clause crosswalk

| Catalog component | Modern-source component | Prospective Lean component | Intake status |
|---|---|---|---|
| "group" | finite `G` in Theorem 6.2; arbitrary `G` with a finite series in Remark 6.3 | `G : Type u`, `Group G`, optional `Finite G` | exact domain open |
| "composition series" | finite subnormal chain from `G` to `{1}` with simple nontrivial factors | group-specific series, or `CompositionSeries X` after checked realization | normality, orientation, endpoints, factors open |
| "unique" | equal lengths and a permutation of factors | a bijection `Fin s₁.length ≃ Fin s₂.length` | source strength identified; encoding open |
| "up to isomorphism" | corresponding quotient groups are isomorphic | `MulEquiv` between quotient factors, or source-equivalent bundle | quotient construction and transport open |
| Jordan/Holder, 1889 | historical attribution and Milne footnote | provenance only | pinpoint primary-source audit open |
| `已验证` | untrusted inventory label | accepted H and M receipts would be required | no H0 or M0 credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Order.JordanHolder` defines `JordanHolderLattice`, `CompositionSeries`, and
`CompositionSeries.Equivalent`. Its theorem
`CompositionSeries.jordan_holder (s₁ s₂) (hb : s₁.head = s₂.head)
(ht : s₁.last = s₂.last) : s₁.Equivalent s₂` proves an abstract Jordan-Holder result. Here
`Equivalent` contains a bijection between series steps and relates each adjacent pair through the
class's abstract `Iso`.

The module prose describes subgroups as an intended example, but its TODO says that instances for
subgroups still need to be provided and discusses the missing group/module transfer API. A bounded
search found no `JordanHolderLattice (Subgroup G)` instance or group-specific composition-series
wrapper in pinned mathlib or repo-local Lean. Pinned mathlib does have
`JordanHolderModule.instJordanHolderLattice` for submodules; it cannot close the group target.
`IntakeProbe.lean` therefore checks the abstract theorem and a generic use only. This is M3
feasibility evidence, not statement identity, a group transport, proof provenance closure, or M0.

## Source gate

Before leaving `H1`, accountable reviewers must preserve an immutable approved source edition;
select the finite or conditional-arbitrary proposition; map every binder, premise, series step,
quotient factor, and conclusion; audit the historical attribution, corrections, and translation;
and independently approve fidelity to `THM-M-0065`. Only then may the statement phase freeze the
exact Lean target, minimal imports, expression and environment fingerprints, checked transports,
and removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
