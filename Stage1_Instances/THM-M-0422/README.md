# THM-M-0422 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for global class field theory. The manifest's short
description, "abelian extensions of number fields", is not treated as a sufficiently exact theorem
statement. At intake, the intended theorem is conservatively scoped as the standard global
reciprocity theorem together with the existence/classification theorem. Neither component may be
dropped merely because one is easier to express in Lean.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Base objects | A number field `K`, its places and completions, ideles, and the idele class group `C_K` | Exact mathlib types and universes are deferred to the statement phase |
| Reciprocity | For every finite abelian extension `L/K`, the global Artin map is surjective with kernel `N_{L/K}(C_L)`, hence `C_K / N_{L/K}(C_L) \cong Gal(L/K)` | Topological quotient and continuity conventions must be frozen before elaboration |
| Existence | Finite-index open subgroups of `C_K` correspond to finite abelian extensions of `K` through norm groups, with the usual inclusion-reversing field/subgroup correspondence | Uniqueness inside a fixed algebraic closure and equality versus canonical isomorphism remain to be normalized |
| Local/global compatibility | The global Artin map is assembled from local reciprocity maps and principal ideles map trivially | This is required architecture, not proof credit |
| Archimedean and ramified places | Included under the standard idele conventions | No place may silently be removed in a later encoding |
| Foundations | Lean 4 kernel plus a versioned classical/choice/quotient policy | Exact foundation, TCB, and computation profiles remain open |

The dossier does not identify the vague phrase "all abelian extensions" with the Kronecker-Weber
theorem (which only treats `K = Q`) or with local class field theory. Those are related branches,
not substitutes for this root.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R3]`. The source label `已验证` is
untrusted metadata. The first failed theorem gate is exact-statement elaboration: there is not yet a
canonical Lean expression, environment fingerprint, checked encoding transport, or mutation test.
No proof, source acceptance, or theorem completion is claimed.

## Validation

The exact commands and results for this intake-only artifact are recorded in `validation.md`. They
establish target membership, repository-standard consistency, JSON syntax, scoped reference
integrity, and absence of prohibited proof constructs only. Master acceptance and all dependent
phases remain outstanding.
