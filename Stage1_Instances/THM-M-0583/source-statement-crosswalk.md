# Source-statement crosswalk

## Primary source anchor

Michael H. Freedman, "The topology of four-dimensional manifolds", *Journal of Differential
Geometry* **17** (1982), 357-453, DOI `10.4310/jdg/1214437136`. Corollary 1.3 is commonly cited as
the four-dimensional topological Poincare theorem (a homotopy 4-sphere is homeomorphic to the
4-sphere).

This bibliographic record is a discovery anchor, not an immutable evidence receipt and not an `H0`
claim. Before `H0`, a reviewer must inspect a stable scan, transcribe the exact corollary wording and
page, follow the paper's definitions and hypotheses, check published errata, and independently
approve the source-to-target mapping.

## Crosswalk

| Repository/source component | Intended mathematical meaning | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "four-dimensional" | dimension exactly 4 | explicit dimension index and manifold model | included; encoding open |
| "Poincare conjecture" | homotopy sphere is standard sphere | binder for a homotopy equivalence to `S^4` | included |
| Freedman's topological result | conclusion is homeomorphism | existential/equivalence-valued homeomorphism conclusion | included |
| source label `已验证` | untrusted metadata only | gives no kernel or human-source credit | excluded from evidence |
| "smooth" reading | diffeomorphism to the smooth sphere | materially stronger and unresolved | explicitly excluded |

## Statement-phase checks

The statement phase must verify that the primary corollary has precisely the homotopy-sphere form,
or document a checked mathematical equivalence from its printed formulation. It must audit whether
`closed`, connected, simply connected, orientation, and local-flatness assumptions are explicit,
implicit in terminology, or derived. No Lean candidate has been accepted or searched for at this
intake phase; mathlib and external declaration discovery belongs to `ANCHOR_AUDIT` after exact
elaboration.
