# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9859-9864` supplies exactly the title `Floquet理论`, Gaston
Floquet, 1883, the gloss `周期线性系统的理论`, importance `high`, and status `已验证`. Git history
places all six uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:36777-36802` repeats the metadata but explicitly leaves the exact
definitions and premises, proof route, dependencies, equivalent forms, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The catalog contains no bibliography, theorem or page locator, equation model, binders,
hypotheses, conclusion, incorporated definitions, proof boundary, translation provenance, errata,
or reviewer. It therefore does not identify a stable proposition.

## Historical source-family lead

Crossref identifies G. Floquet, "Sur les équations différentielles linéaires à coefficients
périodiques," *Annales scientifiques de l'École normale supérieure*, series 2, volume 12 (1883),
pages 47-88, DOI `10.24033/asens.220`. This matches the attribution, date, and subject, but the
catalog does not cite the paper or select any proposition or passage from it. Metadata alone is E5
discovery evidence, not an H0 source crosswalk.

## Inspected modern discriminator

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, AMS, 2012, Section 3.6, printed pages 91-93, was inspected outside the repository
as a source-family discriminator. The author-hosted publisher-permitted preliminary edition has
SHA-256 `362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e` and size 4,133,331
bytes. A temporary `pdftotext -f 102 -l 104 -layout` extract of exactly those three PDF pages has
SHA-256 `4c786c2321885d6f6fb501e1552e716c8392a3dbe4bbf39b65b0086b0f4c794b`.

That section visibly separates Lemma 3.14 (time-shift periodicity of a principal matrix solution),
the monodromy relation, Theorem 3.15 (Floquet decomposition), Corollary 3.16 (real decomposition at
twice the period), multiplier and exponent definitions, Corollary 3.17 (stability criteria), and
Corollary 3.18 (reduction to constant coefficients). This separation is evidence that `Floquet
theory` is multiply ambiguous, not evidence selecting one of those results for the catalog target.
The catalog does not cite Teschl, no external file is admitted as immutable H0 evidence, and no
complete assumption, proof-boundary, errata, or independent-review mapping is claimed.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| periodic linear system | `x' = A(t)x`, higher-order equation, operator equation, or another model | `Function.Periodic`, `IsIntegralCurve`, matrix or operator action | exact model and assumptions absent |
| period | positive selected period, minimal period, multiple, or doubled period | real addition and `Function.Periodic` | positivity and period policy absent |
| solution matrix | principal matrix at a base time or arbitrary fundamental matrix | matrix-valued differentiable function plus normalization and invertibility | no canonical representation selected |
| monodromy | one-period transition matrix and its powers | source-defined matrix product/transition API | no declaration or bridge located |
| Floquet form | periodic factor times a matrix exponential | `Matrix`, `NormedSpace.exp`, multiplication | one neighboring theorem family, not the catalog claim |
| real/complex form | original-period complex logarithm or doubled-period real form | real/complex matrices and checked scalar transport | field and logarithm policy absent |
| multipliers/exponents | eigenvalues of monodromy/logarithm with branch ambiguity | finite-dimensional spectrum/eigenvalue interfaces | separately cataloged THM-M-1354 boundary |
| stability | spectral/Jordan criterion for stability or asymptotic stability | source-selected stability and spectrum predicates | separately cataloged THM-M-1355 boundary |
| `已验证` | untrusted inventory label | no declaration or proof body | explicitly rejected as evidence |

## Neighbor target crosswalk

`Docs/researches/math_theorems.md:9866-9871` separately gives `THM-M-1353` the title `Floquet定理`
and gloss `周期系统的基本解矩阵`. Lines 9873-9878 separately give `THM-M-1354` characteristic
exponents. The next catalog item names stability of linear systems. These records make a silent
choice of decomposition, exponent, or stability statement especially unsafe: target adjacency is
not a checked implication and proof credit cannot be shared.

## Required source admission

The statement phase must preserve and hash one lawful complete source, select a precise numbered
result or explicitly sourced conjunction, transcribe all incorporated definitions, ordered binders,
hypotheses, conclusion, and proof boundary, record edition/page and corrections or errata, reconcile
the historical attribution and neighboring target ownership, and obtain independent review. It
must then freeze and mutation-test the same exact Lean expression. Until then, H5 records that the
catalog theory label is not a stable proposition; the canonical mathematical and Lean targets stay
null.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
generic periodicity, ODE, matrix, determinant, and exponential APIs. A bounded exact-topic search
found no Floquet declaration in repo-local Lean or pinned mathlib. This is intake discovery only;
the precommitted exhaustive anchor audit and external-project review remain open.
