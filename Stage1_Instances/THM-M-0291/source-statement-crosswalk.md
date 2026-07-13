# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2090-2095` supplies the title `Fejer's theorem`, attribution to
Lipot Fejer, the year 1900, the gloss `continuous function's Cesaro means converge uniformly`, high
importance, and status `verified`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:8035-8060` repeats the gloss while explicitly leaving definitions,
premises, proof route, dependencies, equivalent forms, axioms, formal status, and artifact links
open. The rev-5.6 manifest preserves `verified` only as untrusted metadata, resets the target to
`L0 / rework_required`, and accepts no legacy artifact.

The repository also has `THM-M-0347` at `Docs/researches/math_theorems.md:2528-2533`, in harmonic
analysis, with the weaker gloss "the Cesaro means of a continuous function converge." It is a
separate target. Its formal files are discovery material only and transfer no evidence here.

## Inspected primary sources

The strongest exact lead is Leopold Fejer, *Untersuchungen uber Fouriersche Reihen*,
*Mathematische Annalen* 58 (1903), pages 51-69, DOI `10.1007/BF01447779`. The complete GDZ scan is
available under stable PURL `http://resolver.sub.uni-goettingen.de/purl?GDZPPN002259443`; the
inspected PDF SHA-256 is
`c68ca6a53cc54c54265ab52c46a9dedd5b7ece16f0006dda7e8d69e0c9e83963`.
Springer and Crossref date the issue to March 1903, while the GDZ volume-level wrapper labels it
1904; this bibliographic discrepancy remains explicit rather than being silently normalized.

Page 51 fixes an everywhere-continuous real function of period `2*pi`. Page 52 displays its
symmetric Fourier partial sums `s_n`, defines the arithmetic-mean sequence
`s_0, (s_0+s_1)/2, ..., (s_0+...+s_(n-1))/n`, and states that it converges uniformly to `f(x)` on
every interval. Pages 59-60 state the broader Hauptsatz and then explicitly say that when `f` is
everywhere continuous, these means converge everywhere and uniformly; the following Zusatz gives
a local-uniform form on closed subintervals of continuity.

This 1903 article says that related short notes appeared in *Comptes rendus* in 1900 and 1902. A
separate preview of the collected-works reproduction, *Sur les fonctions bornees et integrables*,
DOI `10.1007/978-3-0348-5902-8_6`, identifies the original 1900 locator as *Comptes rendus* 131,
pages 984-987. Its two visible pages state pointwise Cesaro convergence for bounded integrable
functions at continuity points and the midpoint result at first-kind discontinuities. The preview
PDF and extracted-text SHA-256 values are
`6be38bd00c307079e685bf2b91769e0f75389873617084a2ff735fe5cd111689` and
`8cac4a06be237f036d5ed43451274b45c9ed433f83fe1649ecf8a9965757b10b`.

The 1903 uniform passage closely matches the catalog and the 1900 note explains its date, but this
is still `H1`: the catalog-to-article identity, complete definition and proof crosswalk, original
1900 versus expanded 1903 role, translation, corrections or errata, and independent review are not
accepted. Collected-work Crossref metadata attributes the chapter to P. Turan; that is editorial
metadata and must not override the embedded Fejer publication.

## Clause crosswalk

| Catalog clause | Inspected source component | Prospective Lean component | Intake status |
|---|---|---|---|
| Fejer's theorem; Fejer; 1900 | 1900 short note plus 1903 expanded article | provenance only | matching source family and exact uniform passage found; independent identity review open |
| continuous function | everywhere-continuous real `2*pi`-periodic `f` | real continuous map on `AddCircle (2*pi)` after checked transport | source scope known; exact Lean carrier open |
| Fourier series | symmetric sine/cosine partial sums through frequency `n` | `fourierCoeff`, `fourier`, finite integer-frequency sum | source convention known; normalization transport open |
| Cesaro means | arithmetic means through `s_(n-1)`, divided by `n` | finite natural-index sum and scalar division | exact index transport open |
| converge uniformly | uniform convergence to `f` on every interval | `Tendsto` in a continuous-map topology or `TendstoUniformly` | source strength located; encoding open |
| `verified` | untrusted inventory label | no Lean proposition or proof object | explicitly rejected as evidence |

The common complex-valued arbitrary-positive-period expression using averages `S_0` through `S_n`
is a plausible transported formulation, not the source-literal statement. It must be justified by
checked period scaling, real-to-complex, normalization, and indexing transports before adoption.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
the additive-circle Fourier ingredients and uniform-convergence interface. It also checks two
nearby declarations that must not be substituted:

- `hasSum_fourier_series_of_summable` proves uniform Fourier-series convergence only after adding
  summability of the coefficients; and
- `Filter.Tendsto.cesaro_smul` proves Cesaro convergence only after assuming convergence of the
  sequence being averaged.

A bounded repo-local and pinned-mathlib search found no Fejer-named terminal declaration outside
the separate `THM-M-0347` dossier. This is intake discovery, not an exhaustive external anchor
audit or absence proof.

The statement phase must obtain independent source approval, choose source-literal or explicitly
transported scope, and elaborate and fingerprint one binder-complete Lean target. Until then the
canonical statement, claim, ordered binders, transports, and statement hashes remain null.
