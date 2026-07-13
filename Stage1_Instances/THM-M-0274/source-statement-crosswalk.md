# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:1971-1976` and `:2246-2251` repeat the same uncited record:

- title: `哈恩-巴拿赫定理`;
- attribution: Hans Hahn / Stefan Banach;
- year: 1927;
- gloss: `线性泛函的保范延拓`;
- importance: high;
- untrusted formalization label: `已验证`.

Both copies originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:7576-7601`
repeats the gloss while leaving definitions and premises, proof route, equivalent formulations,
axioms, machine status, and artifact links open. These records establish catalogue identity only.

## Primary-source lead

Crossref identifies Hans Hahn, the title "Uber lineare Gleichungssysteme in linearen Raumen," the
year 1927, pages 214-229, and DOI `10.1515/crll.1927.157.214`; its abbreviated container title is
`crll`. The observed payload had SHA-256
`d530282084235a98c2390d5427c5a5c4e33dfaec435199db4318c33f4a392509`. The Goettingen
Digitisation Centre metadata independently identifies the volume as *Journal fur die reine und
angewandte Mathematik* 157.

The Goettingen Digitisation Centre IIIF manifest for volume 157 was inspected outside the
repository. It is a 364,004-byte response with SHA-256
`0ae917863d2d66bac51ed8e0d0f2ca1a401a6f954518d6b9dbdc47d21a7daae9` and maps printed pages
214-229 to stable page canvases. The OCR for printed page 217 has SHA-256
`22a0808b6d0faf9d6a8fb66971cf93a7a9fb50ef8f85619e00c2eb9274ca8e67`.

Theorem III on printed page 217 says, in the paper's terminology, that if a complete linear
subspace carries a linear form of slope `M`, then there is a linear form on the ambient linear
space, also of slope `M`, agreeing on the subspace. Pages 215-216 define the real linear space,
convex metric `D`, completeness, linear form, and slope used there. This is a strong primary-source
lead for the real norm-preserving family. Intake has not accepted an exact transcription and
modern translation, determined which historical completeness assumptions are needed in the
modern formulation, audited Banach's later formulation or attribution, checked corrections or
errata, mapped the full proof, or obtained independent review. The source status is therefore H1,
not H0.

## Clause crosswalk

| Catalogue or source component | Historical lead | Pinned Lean candidate | Intake decision |
|---|---|---|---|
| "linear functional" | real-valued `Linearform` | `StrongDual Real p` or `StrongDual K p` | real versus uniform scalar scope open |
| subspace | complete linear subspace in Theorem III | `p : Subspace K E` with no completeness premise | historical-to-modern premise mapping open |
| extension | agreement on the subspace | `forall x : p, g x = f x` through subtype coercion | exact encoding and binder order open |
| "norm-preserving" | equal slope `M` | `norm g = norm f` | slope/operator-norm translation needs review |
| ambient space | complete real linear space under preceding setup | seminormed `E` over real/complex-like `K` | completeness and seminorm-kernel relationship open |
| `已验证` | untrusted inventory metadata | no proposition or proof object | no H or M credit |

## Formal candidate crosswalk

The intake probe elaborates these pinned declarations:

| Declaration | Candidate role | Unclosed gate |
|---|---|---|
| `Real.exists_extension_norm_eq` | closest real analytic norm-preserving extension form | exact source translation, canonical expression, wrapper/transport, provenance and trust audit |
| `exists_extension_norm_eq` | uniform real/complex-like extension | source scalar scope and checked relationship to the selected root |
| `exists_extension_of_le_sublinear` | algebraic domination engine used by the real proof | cannot replace the continuous norm-preserving conclusion |
| `ContinuousLinearMap.exist_extension_of_finiteDimensional_range` | vector-valued finite-range corollary | explicitly lacks a norm estimate and is not the catalogue root |

The pinned `docs/1000.yaml` maps "Hahn-Banach theorem" to `exists_extension_norm_eq`; that index is
secondary discovery metadata, not statement identity. Before leaving H1, an independent reviewer
must approve one immutable source edition, pinpoint theorem and definition chain, every premise and
conclusion, translation, proof boundary, attribution, and errata result. Before statement
acceptance, Lean work must freeze minimal imports and an elaborated expression and pass removed-
hypothesis, changed-domain, binder-scope, scalar-field, and boundary mutations.
