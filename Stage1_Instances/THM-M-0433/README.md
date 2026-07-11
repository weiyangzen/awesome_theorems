# THM-M-0433 rev-5.6 intake

This is the `planned` dossier for Laurent Lafforgue's global Langlands correspondence for
`GL_n` over global function fields. Historical Stage1 files are discovery material and confer no
rev-5.6 proof or statement credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Global field | Function field of a smooth projective geometrically connected curve over a finite field | Equivalence with an algebraic function-field encoding must be checked |
| Galois side | Continuous irreducible rank-`n` l-adic representations, finite ramification implicit in continuity, finite-order determinant | Weil/Galois choice and coefficient conventions are not frozen |
| Automorphic side | Cuspidal automorphic representations of adelic `GL_n` with finite-order central character | Full adeles, quotient, smoothness and cuspidality APIs are absent locally |
| Local compatibility | Matching unramified Frobenius characteristic and Hecke/Satake polynomials | Frobenius direction and polynomial normalization need source-level pinning |
| Correspondence | Existence, uniqueness/bijection, rank preservation, and local compatibility | No abstract structure carrying the conclusion counts as its proof |
| Foundations | Lean 4 kernel and pinned mathlib | Exact dependency, axiom and computation profiles remain open |

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_061.lean` usefully inventories
function-field, finite-adele, representation, and polynomial interfaces. Its automorphic and Weil
packages are abstract statement scaffolding; fields that assume compatibility cannot close the
source theorem.

## Intake verdict

Lifecycle is `planned`, with provisional root vector `[H1, M3, R3]`. The first failed theorem gate
is the exact statement gate: there is no canonical elaborated declaration, expression hash,
environment fingerprint, checked encoding transport, or mutation record. The theorem is not
complete. The dependent statement phase must resolve source normalization before proof search.

## Validation

`validation.md` records the exact local structural checks. They validate this dossier and manifest
membership only, not the mathematical theorem.
