# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:470-475` supplies exactly the Chinese title `凯莱定理`, Arthur
Cayley, the year 1854, the gloss `每个群都同构于某个置换群`, importance "high," and status
`已验证`. Git history traces the six-line record to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It gives no bibliography, group or permutation-group
definition, binders, hypotheses, conclusion encoding, proof, correction history, formal system, or
machine artifact.

`Docs/Stage0_Blueprint.md:1839-1864` repeats the gloss and attribution while explicitly leaving the
formal system, logical foundation, exact definitions and premises, proof route, dependencies,
alternate formulations, axioms, machine status, and artifact links open. The rev-5.6 manifest
therefore retains `已验证` only as untrusted metadata and resets this target to
`L0 / rework_required`.

## Historical source lead

Crossref metadata was inspected on 2026-07-13 for Arthur Cayley, "VII. On the theory of groups, as
depending on the symbolic equation theta^n = 1," *The London, Edinburgh, and Dublin Philosophical
Magazine and Journal of Science*, volume 7, issue 42 (January 1854), pages 40-47, DOI
`10.1080/14786445408647421`. This is a bibliographically matching primary-paper lead, not accepted
`H0` evidence. The article body was not preserved or passage-audited here, and Crossref supplies no
theorem locator or proof. In particular, this intake does not assert that the paper states the
unrestricted modern subgroup formulation. Edition, exact passage, historical terminology,
assumptions, proof, later corrections, modern-definition transport, and independent review remain
open.

## Component crosswalk

| Catalog component | Standard reading | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "every group" | arbitrary group, finite or infinite | `(G : Type u) [Group G]` | exact universes/binder syntax open |
| "permutation group" | subgroup of the symmetric group on a set | `Subgroup (Equiv.Perm X)` | carrier `X` and existential/range encoding open |
| regular action | left multiplication on the underlying set | `MulAction.toPermHom G G` | likely intended specialization; not frozen |
| faithful | distinct group elements induce distinct permutations | `MulAction.toPerm_injective` / `FaithfulSMul G G` | pinned interface checked, statement role open |
| "isomorphic" | group isomorphism to the image subgroup | `G ≃* (MulAction.toPermHom G G).range` | exact close anchor exists; no accepted target identity |
| `已验证` | untrusted inventory label | accepted source/kernel receipts would be required | no H0 or M0 credit |

The phrase "some permutation group" must not be translated as the entire full symmetric group. The
range subtype is itself the subgroup and is the natural codomain of the isomorphism. Using `X = G`
also avoids a finite-cardinality restriction: an infinite group acts by permutations of its own
possibly infinite underlying set.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.GroupTheory.Perm.Subgroup` says in its module documentation that it proves Cayley's theorem.
Its declaration is:

```lean
Equiv.Perm.subgroupOfMulAction (G H : Type*) [Group G] [MulAction G H]
    [FaithfulSMul G H] : G ≃* (MulAction.toPermHom G H).range
```

The declaration generalizes the result to any faithful action and explicitly directs the reader to
set `H = G` for the usual theorem. `IntakeProbe.lean` checks that declaration, the permutation
homomorphism, injectivity of a faithful action, the regular-action instance, and the exact
specialization type. `#print axioms` reports `[propext, Classical.choice, Quot.sound]`. The source
file also asserts that no `Field` is imported. These are strong `M3` anchor observations, but the
intake is not an anchor audit: no canonical expression hash, exact-type receipt, source/body
provenance closure, dependency/TCB audit, placeholder audit of the transitive body, or accepted
wrapper exists.

## Status boundary

Human-source status is `H1`, not `H0`: a primary-paper lead and stable modern meaning are known, but
no pinpoint proof-and-assumption crosswalk or independent review is accepted. Machine status is
`M3`, not `M0` or `M1`: a locally elaborated, unusually close pinned anchor is present, but target
identity and integration gates remain open. Readability remains `R4`; this intake map is not a
complete, source-faithful, independently reviewed proof reconstruction.
