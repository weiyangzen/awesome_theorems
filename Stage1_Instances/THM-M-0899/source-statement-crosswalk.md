# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6579-6584` supplies exactly:

| Catalog field | Verbatim value | Intake interpretation |
|---|---|---|
| title | `Wilson定理` | ambiguous name without a theorem locator |
| attribution | `Richard Wilson` | points toward the combinatorialist, but not one publication |
| time | `1972` | catalog year only |
| statement | `t-设计的存在性` | underspecified design-existence family |
| importance | `高` | metadata only |
| formalization status | `已验证` | explicitly untrusted under rev-5.6 |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The source-record blob is
`5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf`; the exact six-line extract has SHA-256
`8e9acf9467705a995a1355ecae6499ba515792a2507454d26a5a70dde439b8e3`. The record contains no
bibliography, definition, parameter tuple, hypotheses, conclusion, proof locator, correction or
errata information, or formal artifact.

`Docs/Stage0_Blueprint.md:24521-24546` is a generated projection rather than an independent source.
It repeats the gloss and attribution while leaving exact definitions and premises, proof path,
dependencies, equivalent statements, axiom policy, machine status, and artifact links open. The
exact projection extract has SHA-256
`d32a7c9c98c65e2458cc18852e71ce312324ceae8ee823a6e7b6c993643d9647`.

## Phrase-to-proposition crosswalk

| Required proposition field | Supported by repository source? | Frozen intake value |
|---|---:|---|
| design class | no | open among PBD, BIBD/`2`-design, and general `t`-design readings |
| carrier and block representation | no | open |
| ordered quantifiers | no | empty; no binders invented |
| parameter domains | no | empty; `t`, `v`, `k`, `lambda`, and allowed block sizes not selected |
| admissibility/divisibility hypotheses | no | empty |
| fixed versus varying parameters | no | open |
| threshold and exceptions | no | open |
| exact conclusion | no | open among exact, eventual, iff, and construction readings |
| multiplicity and simplicity | no | open |
| excluded degenerate cases | no | none excluded |
| canonical mathematical statement | no | `null` |
| canonical Lean target and hashes | no | `null` |
| accepted primary proof source | no | none |
| accepted formal proof body | no | none |

The literal phrase is preserved but cannot be promoted to a theorem until these missing fields are
selected from an approved source and independently reviewed.

## Bibliographic discovery candidates not credited

A bounded Crossref query for Richard Wilson and the title phrase *An existence theory for pairwise
balanced designs* returned these records:

| Part | Bibliographic metadata returned by Crossref | Identity implication only |
|---|---|---|
| I | *Composition theorems and morphisms*, J. Combinatorial Theory A 13 (1972), 220-245, DOI `10.1016/0097-3165(72)90028-3` | matches author/year, but title concerns PBDs rather than a binder-complete general `t`-design claim |
| II | *The structure of PBD-closed sets and the existence conjectures*, J. Combinatorial Theory A 13 (1972), 246-273, DOI `10.1016/0097-3165(72)90029-5` | matches author/year, but does not say which conjecture/corollary the catalog intends |
| III | *Proof of the existence conjectures*, J. Combinatorial Theory A 18 (1975), 71-79, DOI `10.1016/0097-3165(75)90067-9` | proof-title and later year expose a material source/proof-boundary question |

The observed mutable Crossref JSON was 81,724 bytes with SHA-256
`b49baca41b082b4b1ecc794080d9218c9d93137bb5599f9d5072badf683b56b2` on 2026-07-13. It is
discovery metadata, not an immutable primary theorem source. No paper body was admitted, and no
theorem statement, definitions, premise map, proof boundary, correction history, or H0 review was
inferred from the titles. The catalog cites none of the three parts.

The discovery raises two unresolved conflicts: the literal arbitrary-`t` gloss versus the located
PBD titles, and the catalog year 1972 versus the 1975 item explicitly titled as the proof. A source
review must decide whether the intended root is a PBD theorem, a BIBD/`2`-design corollary, a later
general `t`-design result, or a catalog error.

## Formal crosswalk

`IntakeProbe.lean` authenticates only generic pinned finite-subset and counting interfaces. The
bounded exact-name search found no design theorem candidate. Pinned mathlib's declarations named
for Wilson concern the factorial/primality criterion and contradict the catalog's subject boundary.
No checked relationship exists from either surface to the unresolved claim.

The provisional root is `[H5, M4, R4]`. `H5` applies to the unstable catalog proposition, not to an
identified source theorem. No H0, M0, R0, accepted state, audit completion, or theorem completion is
claimed.
