# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:4671-4676` records only:

- title: `斯通-切赫紧化`;
- attribution: Marshall Stone / Edward Cech;
- year: 1937;
- gloss: `完全正则空间的最大紧化`;
- importance: high; and
- untrusted formalization label: `已验证`.

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:17233-17258`
repeats the gloss while leaving exact definitions, assumptions, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links open. These records establish catalog
identity only.

## Primary-source leads

A bounded source inspection identified M. H. Stone, "Applications of the theory of Boolean rings
to general topology," *Transactions of the American Mathematical Society* 41 (1937), no. 3,
375-481, DOI `10.1090/S0002-9947-1937-1501905-7`. The observed publisher PDF was 11,991,984
bytes and 107 pages, SHA-256
`ee86a25958309cab889686f59c9afe42a9d5b45f85535d6fb464fdb038808e59`. Its extracted text has
SHA-256 `65772d16121915d832b892a377f4811329eff679078ca96bfb2b4dd6cb991741`.

Stone's Definition 21 (printed pp. 454-455) defines a CR-space as a T0 space with any of three
equivalent complete-regularity properties. Theorem 78 (pp. 461-463) constructs a bicompact
Hausdorff space from its bounded-continuous-function ring. Theorem 79 (pp. 463-465) makes that
space a dense Hausdorff extension and extends every bounded continuous real function. Theorem 88
(pp. 476-477) proves that any bicompact Hausdorff extension of a continuous image of the CR-space
receives a continuous map from this constructed extension; in particular, every bicompact
Hausdorff extension of the original space is its continuous image. This is strong evidence for the
catalog's "greatest" gloss.

Crossref also identifies Eduard Cech, "On Bicompact Spaces," *Annals of Mathematics* 38 (1937),
no. 4, 823-844, DOI `10.2307/1968839`. The publisher body was not obtained during this bounded
intake. Neither source has completed a full incorporated-definition map, exact theorem and proof
boundary audit, correction/errata check, modern terminology translation, Stone/Cech attribution
reconciliation, or independent review. They are H1 leads, not H0 evidence.

## Clause crosswalk

| Catalog clause | Source-family evidence | Pinned Lean interface | Intake decision |
|---|---|---|---|
| `完全正则空间` | Stone Definition 21 uses a T0 CR-space; modern conventions differ on separation | `CompletelyRegularSpace` omits T0/T1; `T35Space` adds T0 | family identified; exact convention open |
| `紧化` | Stone Theorem 79 gives an immediate/strict bicompact Hausdorff extension | `StoneCech X`, compact/T2 instances, `continuous_stoneCechUnit`, `denseRange_stoneCechUnit` | construction candidate only |
| space embedded densely | Stone's extension terminology and Theorem 79 supply the historical relation | `isDenseInducing_stoneCechUnit` under complete regularity; `isDenseEmbedding_stoneCechUnit` under T3.5 | exact separation and compactification package open |
| `最大` / greatest | Stone Theorem 88 maps the constructed extension continuously onto every competitor | `stoneCechExtend`, `stoneCechExtend_extends`, `continuous_stoneCechExtend` | factor direction supported; competitor encoding and surjectivity/uniqueness transport open |
| universal uniqueness | uniqueness is expected from density and Hausdorff codomain | `stoneCech_hom_ext`; `stoneCechEquivalence` | strong formal candidate; source-root selection open |
| `已验证` | untrusted inventory metadata | no proposition or proof object | no H or M credit |

## Formal candidate crosswalk

The intake probe elaborates these interfaces at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Declaration | Candidate role | Unclosed gate |
|---|---|---|
| `StoneCech`, `stoneCechUnit` | construction and unit | source-identical root and compactification convention |
| compact/T2 instances on `StoneCech X` | compact Hausdorff carrier | exact profile and expression serialization |
| `continuous_stoneCechUnit`, `denseRange_stoneCechUnit` | continuous dense unit | embedding is absent without stronger assumptions |
| `isDenseInducing_stoneCechUnit` | complete-regularity form | source convention and checked transport |
| `isDenseEmbedding_stoneCechUnit` | T3.5 compactification form | whether T3.5 is the intended source premise |
| `stoneCechExtend` and its continuity/extension lemmas | factor-map existence | exact competitor package and factor direction |
| `stoneCech_hom_ext` | uniqueness of continuous factors | exact commuting equation and source mapping |
| `stoneCechEquivalence` | categorical universal property | whether the adjunction is canonical or only alternate |

Before H0, independent reviewers must admit immutable source editions and approve every material
definition, premise, conclusion, proof boundary, correction, erratum, translation, and relationship
between the 1937 sources. Before statement acceptance, Lean work must freeze one exact source-
faithful expression, minimal imports, environment and expression hashes, checked alternate forms,
and all required mutations. The later anchor audit must independently inspect terminal bodies,
axioms, licenses, provenance, and dependency feasibility; this intake probe grants no proof credit.
