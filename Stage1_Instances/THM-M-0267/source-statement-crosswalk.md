# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1922-1927` records the Chinese title
`阿尔泽拉-阿斯科利定理`, Cesare Arzela/Giulio Ascoli, 1889, the gloss
`函数列紧性的判别准则`, importance "high," and status `已验证`. Git blame places all six
uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula,
quantifier, domain, codomain, topology, premise, direction, theorem/page, proof, translation,
correction record, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7387-7412` repeats the gloss while explicitly leaving precise definitions
and premises, proof history, dependencies, equivalent forms, axioms, machine state, and artifact
links open. Its generic theorem-tree language is planning metadata. The rev-5.6 manifest retains
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Human-source discovery

The Encyclopedia of Mathematics permanent revision 53769 describes "Arzela-Ascoli theorem" as a
name for multiple results about conditions under which limits of sequences of continuous functions
are continuous. It cites C. Arzela, *Mem. Accad. Sci. Bologna (5)* 5 (1893), pages 225-244, and G.
Ascoli, *Rend. Accad. Lincei* 18 (1883), pages 521-586. This secondary source confirms a published
historical family and exposes a date and formulation mismatch with the catalog's 1889 compactness
gloss. It does not select or reproduce the intended compactness proposition.

The observed secondary-source response was 14,761 bytes with SHA-256
`cc74b5b2a829ec1710907a773606c86e2b0129f146739fb37a941b5ff3bcc840`. No primary text,
complete theorem passage, assumption map, proof boundary, translation, errata audit, or independent
review is admitted. The published family therefore supports provisional `H1`, not `H0`.

Pinned mathlib's general Ascoli module cites N. Bourbaki, *General Topology, Chapter X*. Its
`bourbaki1966` bibliography key resolves to *Elements of Mathematics, General Topology, Part 1*
(1966, vii+437 pages, MR0205210), while a separate Part 2 entry follows. The chapter/volume mapping,
exact theorem/page, and relationship to the catalog root remain unreconciled.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `函数列` | natural-number sequence or an arbitrary family/set | exact index type and any range/subsequence bridge | open |
| compactness | compact set, compact closure, relative compactness, total boundedness, or sequential extraction | exact function-space topology and conclusion predicate | open |
| criterion | implication or equivalence | checked direction or directions | open |
| functions | continuous scalar-, metric-, or uniform-space-valued maps | universes, domain/codomain structures, exact carrier | open |
| Arzela/Ascoli, 1889 | historical provenance | admitted editions, exact locators, translation and attribution map | 1883/1889/1893 mismatch open |
| `已验证` | untrusted inventory label | accepted human and kernel receipts | no credit |

## Formal-candidate crosswalk

All declarations below are from pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `IntakeProbe.lean` checks their interfaces and
axiom reports only; it does not inspect or credit root identity.

| Declaration | Candidate role | Why it is not selected |
|---|---|---|
| `BoundedContinuousFunction.arzela_ascoli₁` | closed equicontinuous family, compact codomain | closed-family form; catalog domain and range absent |
| `BoundedContinuousFunction.arzela_ascoli₂` | closed family with one compact common range | stronger range packaging not supplied by catalog |
| `BoundedContinuousFunction.arzela_ascoli` | compact closure from common compact range and equicontinuity | plausible sufficiency form, not a sequence or full criterion |
| `ArzelaAscoli.compactSpace_of_isClosedEmbedding` | general closed family in uniform-on-compact topology | materially more general encoding and premises |
| `ArzelaAscoli.isCompact_closure_of_isClosedEmbedding` | general closure compactness | source topology, embedding and pointwise conditions open |
| `ArzelaAscoli.isCompact_of_equicontinuous` | pointwise-image compactness plus equicontinuity implies compactness | assumes pointwise compactness and gives one direction |

The general module's unproved converse TODO is important because the catalog's word "criterion" may
mean an equivalence. A successful `#check` or axiom report cannot settle that ambiguity.

## Open gates

Before H0, reviewers must admit an immutable primary proof source, pinpoint the exact result and
incorporated definitions, map all premises, conclusions, directions and proof transitions, resolve
the historical dates and translations, audit corrections, and independently approve the mapping.
Before statement acceptance, Lean work must freeze exact binders and imports, serialize an
elaborated expression and environment fingerprint, compile any alternate-form transport, and pass
all required mutations. Formal proof-body provenance and trust inspection belong to the later
anchor-audit phase.
