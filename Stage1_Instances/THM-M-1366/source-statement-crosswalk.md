# Source-statement crosswalk

## Repository source records

The only repository-supplied source is secondary catalog metadata. The same record appears at
`Docs/researches/math_theorems.md:9957-9962` and
`Docs/researches/math_theorems.md:10208-10213`:

| Catalog field | Received value | Statement consequence |
|---|---|---|
| title | `结构稳定性` | Identifies a topic family, not a proposition. |
| attribution | `Andronov/Pontryagin` | Historical orientation only; no work, edition, theorem, or page is cited. |
| year | `1937` | Does not identify a source variant or its assumptions. |
| statement | `系统在扰动下的稳定性` | Leaves "system," "perturbation," and "stability" undefined. |
| importance | `高` | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted under rev-5.6; no H or M credit. |

Both copies originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the source blob is
`5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf`. Duplication does not create independent evidence or
select a canonical root.

The Stage0 projection at `Docs/Stage0_Blueprint.md:37155-37180` repeats the gloss and explicitly
marks the formal system, logic, precise definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links as open. It therefore cannot fill the
missing proposition.

## Phrase-to-statement map

| Received component | Required source decision | Candidate Lean surface | Current result |
|---|---|---|---|
| "system" | vector field, flow, map, diffeomorphism, invariant set, and phase space | `Flow`, functions, homeomorphisms, ODE interfaces | unresolved |
| "perturbation" | space of systems, regularity, metric/topology, neighborhood, and quantifier order | no selected canonical structure | unresolved |
| "stability" | conjugacy, semiconjugacy, orbit equivalence, time change, or classification | `Homeomorph`, `Function.Semiconj`, `Flow.IsSemiconjugacy` are only generic candidates | unresolved |
| Andronov/Pontryagin | exact primary work, edition/translation, theorem, page, proof, and corrections | not applicable until source selection | unresolved |
| 1937 | source-version identity | not applicable | unresolved |

Because each material component is unresolved, there are no ordered binders, hypotheses,
truth-valued conclusion, alternate-encoding transports, or statement fingerprint to credit.

## Bibliographic discovery boundary

The attribution is commonly associated with the planar rough-systems tradition. A bounded
bibliographic query also returned Crossref record `10.1201/9780367813758-12`, a 2019 selected-works
chapter titled *Rough Systems*, pages 159-164, whose record names R. V. Gamkrelidze. That is a
secondary discovery lead, not the 1937 primary source. Its theorem text was not selected or mapped,
so it supplies no source acceptance and does not raise the target above `H5`.

## Neighbor and variant boundary

The repository separately assigns Peixoto's theorem (`THM-M-1367`) the gloss "structural
stability of two-dimensional systems" and Morse-Smale systems (`THM-M-1368`) the gloss
"characteristics of structurally stable systems." Hartman-Grobman, stable manifolds, the Smale
horseshoe, hyperbolic dynamical systems, and Anosov diffeomorphisms also have separate IDs. This is
affirmative evidence against silently selecting any of those results merely because it is related
to structural stability.

## Human-source gate

No source receives H0 or H1 credit. To leave `H5`, a source record must identify an immutable
primary or authoritative edition, stable identifier, exact theorem/section/page, all incorporated
definitions and premises, the conclusion and proof boundary, dependent source IDs, correction and
errata status, and an independent reviewer. The reviewer must also approve the map from every
material source clause to the eventual mathematical and Lean statement. A title, attribution,
secondary chapter, URL, or famous theorem family is insufficient.

## Current statement boundary

The authoritative intake therefore keeps `canonical_statement`, `canonical_claim`, Lean module,
declaration/expression, elaborated-expression hash, and environment fingerprint null. The root
vector `[H5, M4, R4]` classifies only this received unstable target. It does not classify any future
source-corrected structural-stability theorem and does not claim that such theorems lack human
proofs.
