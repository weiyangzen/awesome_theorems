# Source-statement crosswalk

## Repository source

The catalog record at `Docs/researches/math_theorems.md:2111-2116` contains exactly:

| Catalog field | Literal value | Intake interpretation |
|---|---|---|
| name | `普朗歇尔定理` | recognizable Plancherel theorem family |
| attribution | `Michel Plancherel` | historical metadata, not a proof citation |
| time | `1910` | historical metadata; consistent with the primary-work lead below |
| statement | `L^2函数的傅里叶变换等距性` | isometry of the Fourier transform for `L^2` functions; not binder-complete |
| importance | `高` | scheduling metadata only |
| formal status | `已验证` | explicitly untrusted; grants no source or machine credit |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, exact domain, formula,
normalization, definition, ordered binder, hypothesis, conclusion, proof boundary, correction
record, reviewer, or formal artifact. `Docs/Stage0_Blueprint.md:8116-8141` repeats the gloss while
leaving those fields open. It is generated planning metadata, not an independent source.

## Clause crosswalk

| Catalog component | Candidate mathematical component | Prospective Lean surface | Intake state |
|---|---|---|---|
| `L^2` functions | square-integrable functions modulo almost-everywhere equality | `MeasureTheory.Lp` or `MemLp.toLp` at exponent `2` and a selected measure | carrier, value space, and binders open |
| Fourier transform | source-normalized transform and its extension from a dense test class | `𝓕` induced by `MeasureTheory.Lp.fourierTransformₗᵢ` | pinned candidate elaborates; normalization crosswalk open |
| isometry | preservation of distance or norm for every input | `‖𝓕 f‖ = ‖f‖` / `MeasureTheory.Lp.norm_fourier_eq` | direct interface only; no canonical target frozen |
| inner-product form | preservation of the `L^2` inner product | `MeasureTheory.Lp.inner_fourier_eq` | related candidate; not credited as an alternate encoding |
| unitary/inverse form | bijective linear isometry with inverse transform | `fourierTransformₗᵢ` and Fourier-pair instances | stronger candidate; inclusion in root open |
| `已验证` | inventory screening label | accepted source and kernel receipts would be required | no credit |

No candidate component becomes canonical merely because it is conventional or available in
mathlib. The statement phase must map every incorporated binder, definition, premise, conclusion,
normalization, transport, and boundary case to an approved source.

## Primary-work lead

Crossref's record identifies *Contribution a l'etude de la representation d'une fonction arbitraire
par des integrales definies*, Rendiconti del Circolo Matematico di Palermo 30 (1910), pages 289-335,
DOI `10.1007/BF03014877`, and names Michel Plancherel first. Its payload anomalously lists Mittag
Leffler as an additional author, so that metadata is a discovery lead rather than definitive
authorship evidence. The title, first author, year, and subject match the catalog's theorem family.

The publisher endpoint returned an HTML access page rather than article text. No immutable full
text, exact theorem/page within the article, incorporated definitions, assumptions, notation,
proof boundary, correction or errata status, translation decision, or independent review was
admitted. The citation is therefore a strong primary-work lead supporting provisional `H1`, not
`H0`.

## Duplicate collision

The corpus separately records `THM-M-0342` at `Docs/researches/math_theorems.md:2493-2498` under
harmonic analysis. It has the same name, attribution, year, importance, and untrusted status, with
the nearly identical gloss `L^2傅里叶变换的等距性`. The manifest retains both IDs, whose categories
and literal records differ. This is strong duplicate-review evidence, not authorization to merge
roots, transfer source scope, reuse accepted state, or count proof credit.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Fourier.LpSpace` defines
`MeasureTheory.Lp.fourierTransformₗᵢ` for a finite-dimensional real inner-product domain and a
complex Hilbert codomain. It is a complex linear isometry equivalence on `L^2` with volume measure.
The module proves `MeasureTheory.Lp.norm_fourier_eq` and `MeasureTheory.Lp.inner_fourier_eq`.
`Mathlib.Analysis.Fourier.FourierTransform` fixes the familiar inner-product kernel as
`exp(-2 * pi * i * <v,w>)` for the forward transform.

`IntakeProbe.lean` authenticates those three interfaces and the scalar specialization to
`EuclideanSpace Real (Fin n)`. A legacy wrapper in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_153.lean` also invokes `norm_fourier_eq`, but it
belongs to `THM-M-1214` and has a different theorem root.

The separate `THM-M-0342` dossier goes further: it contains a selected Euclidean target and a
provisional proof wrapper using `norm_fourier_eq`. Its source identity, receipts, ownership, and
target decision are not transferable. Together these artifacts justify `M3` discovery for this
intake, not M0: `THM-M-0294` still has no exact canonical expression, checked duplicate transport,
or accepted node receipt. This bounded inspection is not the downstream immutable anchor audit.

## Source gate

Before leaving `H1`, accountable reviewers must select and preserve an immutable source edition,
locate the exact theorem and definition chain, decide whether this record is identical to
`THM-M-0342`, map every domain, measure, character, binder, hypothesis, conclusion and boundary
case, audit corrections and translation, and approve the crosswalk independently. Only then may
the statement phase freeze minimal imports, an exact Lean expression, checked alternate transports,
expression/environment hashes, and the required mutations.
