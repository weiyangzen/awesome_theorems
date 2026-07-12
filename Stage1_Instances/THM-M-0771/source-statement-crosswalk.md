# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Ernst Zermelo, dates the result to 1904, and states
`任何集合可良序化` ("every set can be well-ordered"). The manifest preserves `已验证` only as an
untrusted inventory label. Neither file supplies a proof, exact source passage, assumptions, or an
accepted formal target.

## Located primary source

The historical locator is Ernst Zermelo, *Beweis, dass jede Menge wohlgeordnet werden kann*,
`Mathematische Annalen` 59 (1904), 514-516. Its title directly identifies the well-ordering claim.
This intake does not claim `H0`: a stable edition or scan, exact page-level statement, controlled
translation, definitions, assumptions, errata/corrections, and independent review remain open.

## Crosswalk

| Repository/source component | Mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| "every set" | arbitrary carrier, including empty and finite carriers | `(alpha : Type u)` | scope fixed; set-to-type interpretation and universe freeze open |
| "can be ordered" | existence, not a pre-existing order assumption | `Nonempty` subtype or `Exists` structure | existential scope fixed; exact surface open |
| "well" | every nonempty subset has a least element, equivalently strict order is well-founded in a linear order | `IsWellOrder alpha r` or `WellFoundedLT alpha` with `LinearOrder alpha` | candidate APIs elaborated; equivalence transport not credited |
| Zermelo / 1904 | historical source locator | no proof term | primary work located; passage and assumptions audit open |
| `已验证` | untrusted inventory status | no proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.SetTheory.Cardinal.Order` exposes `exists_wellOrder`, `WellOrderingRel`, and the
`WellOrderingRel.isWellOrder` instance. The source defines `WellOrderingRel` by pulling cardinal
order back along `embeddingToCardinal`; that embedding uses `Classical.choice`. The intake probe
also elaborates the direct relation proposition.

These are discovery and scope evidence only. Exact declaration selection, normalized expression,
checked transports, mutation tests, `#print axioms`, terminal-body provenance, and theorem credit
belong to downstream phases. No `H0` or `M0` claim is made.
