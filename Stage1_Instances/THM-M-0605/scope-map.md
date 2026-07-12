# Scope map

## Root boundary

The intended human root is:

> There exists a smooth seven-dimensional manifold homeomorphic to the
> standard topological 7-sphere but not diffeomorphic to the standard smooth
> 7-sphere.

This makes dimension seven and the two different comparison relations part of
the target. A witness that is only homotopy equivalent to the sphere is too
weak. Conversely, a proof about an arbitrary exotic sphere in an unspecified
dimension would broaden rather than exactly encode this repository item.

| Surface | In scope | Boundary at intake |
|---|---|---|
| `MES7-ROOT` | Existence of one exotic smooth 7-sphere | Provisional exact expression: `Stage1.THM_M_0605.ExoticSevenSphereExists` |
| `MES7-DEF` | A smooth real 7-manifold and a fixed standard smooth 7-sphere | Abstract `Type 0` manifold modeled on `EuclideanSpace Real (Fin 7)`; standard unit sphere in `EuclideanSpace Real (Fin 8)` |
| `MES7-CONSTR` | An explicit Milnor construction if required, commonly via an `S^3`-bundle over `S^4` | Bundle parameters and total-space APIs are not frozen and are not root assumptions |
| `MES7-TOPO` | A homeomorphism from the witness to the topological 7-sphere | `Nonempty Homeomorph`; homotopy equivalence alone is excluded |
| `MES7-SMOOTH` | Nonexistence of any diffeomorphism with the standard smooth sphere | `IsEmpty` of the infinity-smooth `Diffeomorph` type; obstruction proof remains open |
| `MES7-BOUND` | Dimension seven, standard structure, and oriented/unoriented comparison mutations | The root is unoriented; statement mutations are recorded in `statement-receipt.json` |

## Formal and trust boundary

Lean 4 with the repository's pinned mathlib is the selected backend. The
minimal import, universes, structures, options, serialized expression, and
environment fingerprint are frozen in `statement-receipt.json`. Classical reasoning, quotients,
characteristic classes, computation, and any external formal artifact receive
no credit until their foundation, TCB, and provenance records are frozen.

## Exclusions

- Classification or enumeration of all exotic 7-spheres is not part of this
  existence root.
- The Kervaire-Milnor classification of homotopy spheres is a distinct target.
- The explicit bundle construction is proof architecture, not additional
  content silently conjoined to the root.
- Orientation-preserving non-diffeomorphism does not by itself establish the
  absence of every diffeomorphism.
- The generated `已验证` status is not machine evidence.

No node above is an accepted obligation, terminal proof body, or `<=100`-step
leaf. Those identities and budgets can be frozen only after the statement and
anchor-audit phases.
