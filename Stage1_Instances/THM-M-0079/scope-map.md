# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0079` | frozen |
| execution item | `S56-M-0079-STATEMENT`, rank 1105 | self-tested, master acceptance open |
| catalog name | `尼尔森-施莱尔定理` | frozen |
| catalog claim | `自由群的子群仍是自由群` | frozen literally |
| English claim | every subgroup of a free group is free | faithful translation |
| catalog attribution/date | Jakob Nielsen / Otto Schreier, 1921 | untrusted and historically unresolved |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The words "subgroup" and "free" refer to groups. They do not refer to free modules, free
groupoids, Schreier domains, or unrelated Nielsen fixed-point theory. The root is the unrestricted
subgroup-freeness claim only; no rank or index formula is part of the received statement.

## Frozen formal boundary

`Statement.lean` now freezes the provisional canonical expression pending master acceptance.

| Component | Frozen representation | Statement-phase result |
|---|---|---|
| ambient carrier | `G : Type u` | universal binder in arbitrary universe |
| group structure | `[Group G]` | implicit typeclass binder |
| ambient freeness | `[IsFreeGroup G]` | same-universe free-basis property |
| subgroup | `H : Subgroup G` | universal binder with inherited group instance |
| conclusion | `IsFreeGroup H` | checked equivalent to same-universe basis existence |
| canonical proposition | every `H : Subgroup G` inherits `IsFreeGroup H` | expression fingerprint `bb109f77...a553` |

Pinned mathlib defines `IsFreeGroup G` as the existence, in the same universe as `G`, of a type of
generators and a `FreeGroupBasis` giving a multiplicative equivalence with the corresponding free
group. The statement phase selects this generic basis-based formulation as the exact canonical root.
`Statement.lean` checks it equivalent both to the literal ambient `FreeGroup X` formulation and to
the definition-level existence of a same-universe `FreeGroupBasis` for the subgroup.

## Included boundary cases

- the bottom and top subgroups of a free group;
- the trivial ambient free group and trivial subgroup;
- infinitely generated ambient free groups and subgroups;
- subgroups of arbitrary index, including infinite index;
- every Lean universe supported by the selected same-universe `IsFreeGroup` encoding;
- an arbitrary group known by a free basis, not only a carrier syntactically equal to `FreeGroup X`.

No subgroup is excluded by finite generation, nontriviality, finite index, normality, or a chosen
generating set. Statement mutations remove ambient freeness, restrict the ambient group to a
commutative domain, weaken the universal subgroup binder, and exclude the bottom subgroup.

## Explicit non-substitutions

- Nielsen's finitely generated-subgroup case in place of the unrestricted received claim;
- Schreier's finite-index rank formula or the Nielsen-Schreier rank formula added to the root;
- Schreier's lemma about a transversal and subgroup generators;
- freeness only for normal, finite-index, finitely generated, cyclic, or trivial subgroups;
- freeness of a free product, module, algebra, category, groupoid, or topological fundamental group;
- the unrelated Nielsen fixed-point theorem owned by `THM-M-0642`;
- a premise or structure that assumes the subgroup is free;
- the catalog's `已验证` label, a documentation title, or a successful `#check` used as proof credit;
- the pinned candidate reported as accepted `M0-W` before exact statement, anchor, proof,
  provenance, trust, validation, and master-acceptance gates.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.GroupTheory.FreeGroup.NielsenSchreier` declares
`subgroupIsFreeOfIsFree {G : Type u} [Group G] [IsFreeGroup G] (H : Subgroup G) : IsFreeGroup H`.
The module and mathlib's `docs/1000.yaml` explicitly label it the Nielsen-Schreier theorem. The
probe reports `propext`, `Classical.choice`, and `Quot.sound` as axioms and checks that the candidate
application elaborates.

This is strong bounded discovery evidence and a candidate future pinned-library wrapper route. It
is not the dependent anchor audit: the canonical expression is now frozen, but no proof wrapper,
terminal-body identity, transitive dependency graph, source-boundary classification, accepted
foundation profile, or master receipt is frozen here.

## Gate boundary

`S56-M-0079-STATEMENT` self-tests the binder-complete proposition, sole minimal import, universe and
typeclass order, alternate transports, elaborated expression and environment fingerprints, and
structural mutations. Master acceptance remains open. The anchor audit, obligation tree, proof
integration, validation, and release tasks remain dependency-ordered and open.
