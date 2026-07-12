# Source-statement crosswalk

## Primary source candidate

- M. F. Atiyah and I. M. Singer, "The Index of Elliptic Operators: IV", *Annals of Mathematics*,
  Second Series, **93** (1971), 119-138. This is the historical primary paper matching the metadata's
  authors, date, and families subject. The statement phase must inspect a stable scan, identify the
  exact theorem and page, record all definitions it incorporates, and check corrections or errata.

This bibliographic identification is discovery evidence, not `H0`: the exact theorem wording,
hypotheses, conventions, and errata have not been independently reviewed in this intake.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "families index theorem" | index theorem parameterized by a base | smooth/continuous family over `B` | included; category open |
| "fiber bundle" | compact manifolds varying as fibers of `X -> B` | fibration, vertical tangent data, compact-fiber hypotheses | included; exact source assumptions open |
| family of elliptic operators | fiberwise operators varying with the parameter | operator family plus ellipticity and symbol family | included; analytic model open |
| analytic index | virtual kernel/cokernel or stabilized Fredholm-family class | a class in the selected `K(B)` model | included; construction open |
| topological index | pushforward of the family symbol class | symbol K-class, Thom/Gysin construction, pushforward | included; orientations and K-theory flavor open |
| equality of indices | the terminal K-theory identity | equality between the two concrete constructions | intended root |
| `已验证` | untrusted generated metadata | no Lean declaration or receipt | rejected as evidence |

## Source and statement gate

Before `H0`, an independent reviewer must record edition/scan identity, theorem number and pages,
definitions, every hypothesis, notation, real/complex conventions, and errata, then approve the
row-by-row mapping. Before statement acceptance, the Lean owner must freeze the complete ordered
binders and domains, minimal imports, normalized expression hash, environment fingerprint, and
checked transports and mutations required by section 5.1 of the rev-5.6 standard.

A specialization to a one-point base is a useful boundary/mutation check, but it cannot replace the
parameterized root. A Chern-character formula or a Dirac-family formula receives credit only after
its relationship to the selected K-theory statement is source-justified and kernel-checked.
