# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6565-6570` supplies exactly:

| Catalog field | Verbatim value | Intake interpretation |
|---|---|---|
| title | `设计理论` | subject label, not a proposition |
| attribution | `众多数学家` | no named theorem author or source |
| time | `20世纪` | broad catalog period |
| statement | `组合设计的存在性` | an underspecified existence-family gloss |
| importance | `高` | catalog metadata only |
| formalization status | `已验证` | explicitly untrusted by the rev-5.6 manifest |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no citation, URL, theorem
number, definition, parameter tuple, hypotheses, conclusion clauses, proof locator, or formal
artifact. Its exact six-line extract has SHA-256
`54a708f4ac97c4cbbc4f3fbe68f80830098cf2a7fcdd505128e92e2ce6d08837`.

`Docs/Stage0_Blueprint.md:24467-24492` is a generated projection, not an independent source. It
repeats the gloss while leaving exact definitions and premises, proof history, dependencies,
equivalent statements, axiom policy, machine status, and artifact links `待补充` (to be supplied).

## Source phrase to proposition fields

| Required field | Supported by repository source? | Frozen intake value |
|---|---:|---|
| design class | no | open |
| domains and universes | no | open |
| ordered quantifiers | no | empty; no binders invented |
| parameters and hypotheses | no | empty; `t`, `v`, `k`, `lambda`, and admissibility not selected |
| exact conclusion | no | open among multiple inequivalent existence regimes |
| repeated-block convention | no | open |
| excluded degenerate cases | no | none excluded |
| canonical mathematical statement | no | `null` |
| canonical Lean target and hashes | no | `null` |
| accepted human proof source | no | none |
| accepted formal proof body | no | none |

The literal noun phrase is preserved without being promoted to a theorem. A statement worker must
obtain an approved target correction or source selection before it can populate these fields.

## Discovery references not credited

Peter J. Cameron's *Encyclopaedia of Design Theory* landing page was inspected at
`https://webspace.maths.qmul.ac.uk/p.j.cameron/design/encyc/`. It is edited by Cameron and explicitly
says there are many types of designs; it lists existence, uniqueness, enumeration, and random
selection as different mathematical properties. The observed HTML had SHA-256
`19fec75a3a171c4eed8404fe13539cdf96d935715ded30eda8e19c0276dad254` on 2026-07-13.

The *Encyclopedia of Mathematics* entry "Block design," revision 44388, was inspected at
`https://encyclopediaofmath.org/wiki/Block_design`. It distinguishes BIBDs, PBIBDs, symmetric
designs, Steiner systems, Latin-square block designs, and other subclasses, and says design theory
studies existence, classification, and construction with given parameters. The observed HTML had
SHA-256 `06d6f7a7721e44c85b225f53545fa2c075efafb05ac867724a10774ef5f83412` on
2026-07-13.

These sources confirm that the catalog label spans multiple object and problem families, but the
catalog cites neither one. Mutable web observations, broad reference entries, and an intake
worker's interpretation cannot select a canonical theorem or establish H0. A future source audit
must use an immutable primary source with a pinpoint statement, assumptions, proof boundary,
correction/errata status, and independent review.

## Neighbor record crosswalk

The same catalog immediately provides separate records for:

| Target | Catalog gloss | Boundary |
|---|---|---|
| `THM-M-0898` | `Steiner三元系的存在性` | specific Steiner triple-system / Kirkman target |
| `THM-M-0899` | `t-设计的存在性` | named Wilson design-existence target |
| `THM-M-0900` | `设计的渐近存在性` | named asymptotic-existence target |
| `THM-M-0901` | `拉丁方的存在性与计数` | Latin-square existence and counting target |

The boundaries prohibit silent substitution. They do not resolve what additional proposition, if
any, `THM-M-0897` was intended to denote.

## Formal crosswalk and status boundary

The pinned probe checks only finite set-family vocabulary. No checked relationship exists from
those generic APIs to the unresolved catalog claim. The root is provisionally `[H5, M4, R4]`:
the supplied target is not a stable proposition, no usable exact formal artifact is known from the
bounded intake search, and no readable proof reconstruction can attach before statement selection.
No H0, M0, R0, accepted state, audit completion, or theorem completion is claimed.
