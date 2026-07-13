# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2118-2123` supplies exactly the title `豪斯多夫-杨不等式`,
attribution to Felix Hausdorff and William Young, the year 1923, the gloss
`傅里叶变换的L^p估计`, importance `高`, and status `已验证`. Git history places all six uncited
fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:8143-8168` repeats the gloss but explicitly leaves the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axiom
policy, machine-checked status, and artifact links as `待补充`. Rev-5.6 retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

| Catalog component | Prospective formal component | Intake assessment |
|---|---|---|
| "Fourier transform" | a specified transform from a measured group/space to its dual | domain, dual, kernel, sign, and measures absent |
| "`L^p` estimate" | an exact input-`L^p` to output-`L^q` membership and norm bound | output exponent, spaces, binders, and constant absent |
| Hausdorff/Young, 1923 | provenance and source selection | bibliography absent; source/result mapping unreviewed |
| `已验证` | kernel or human-source evidence | explicitly untrusted; no receipt or proof body |

The repository wording identifies a recognizable theorem family, but it is not a truth-valued,
binder-complete statement. In particular, neither `1 <= p <= 2` nor a conjugate-exponent equation
may be inserted into the canonical target without a source decision.

## Duplicate target boundary

The same corpus independently contains `THM-M-0103`, titled `豪斯多夫-杨定理`, under
algebra/representation theory (`Docs/researches/math_theorems.md:754-759`). It has the same
attribution and year but the different gloss `傅里叶变换的范数不等式`. Its manifest rank is 1118
and it remains a separate L0 target. The two records are likely semantic duplicates, but neither
record cites a source or fixes a proposition. This dossier records the collision without importing
`THM-M-0103`'s wording, scope, status, or evidence.

## Primary-source leads

- Felix Hausdorff, "Eine Ausdehnung des Parsevalschen Satzes uber Fourierreihen,"
  *Mathematische Zeitschrift* 16(1), 1923, pages 163-169, DOI
  `10.1007/BF01175679`. Crossref metadata identifies Hausdorff, the Fourier-series title, journal,
  volume, issue, pages, and December 1923 publication. Its deposited reference list cites Young's
  antecedent work. The publisher PDF endpoint returned HTML access content rather than the article,
  so the exact proposition, definitions, assumptions, proof boundary, and errata were not inspected.
- W. H. Young, "On the Determination of the Summability of a Function by Means of its Fourier
  Constants," *Proceedings of the London Mathematical Society* s2-12(1), 1913, pages 71-88, DOI
  `10.1112/plms/s2-12.1.71`. Crossref metadata confirms the bibliographic record. The full article
  and exact antecedent result were not admitted or inspected.

These are primary bibliographic leads, not H0 packets. The catalog does not cite either source or
say whether its target is Hausdorff's Fourier-series formulation, a later Euclidean/LCA extension,
or another normalization. A complete source edition, exact theorem/equation/page locator,
incorporated definitions, assumption and conclusion map, proof-node boundary, errata search,
translation decisions, lawful preservation, and independent review remain open.

A later secondary lead, Michael Christ, arXiv `1406.1210v1`, introduction equations (1.1)-(1.3),
exhibits why the missing choices matter: for its stated Euclidean transform normalization it gives
a sharp Hausdorff-Young-Beckner constant depending on `p`, the conjugate exponent, and dimension.
This is an ambiguity witness only, not the uncited 1923 source and not the canonical target.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Module/declaration | Exact checked role | Credited status |
|---|---|---|
| `Mathlib.Analysis.Fourier.FourierTransform`: `Real.Lp.fourierTransformCLM` | `L1` Fourier transform to bounded continuous functions with operator-norm bound one | endpoint/API discovery only |
| `Mathlib.Analysis.Distribution.SchwartzSpace.Fourier`: `SchwartzMap.norm_fourier_Lp_top_leq_toLp_one` | Schwartz `L1 -> L-infinity` norm inequality | endpoint theorem only |
| `Mathlib.Analysis.Fourier.LpSpace`: `MeasureTheory.Lp.fourierTransform_lI` and `MeasureTheory.Lp.norm_fourier_eq` | `L2` Fourier isometry and Plancherel norm equality | endpoint theorem only |

The Lean spelling uses the Unicode declaration `fourierTransformₗᵢ`; the ASCII spelling above is a
readable label only. A bounded case-insensitive search of repo-local Lean and pinned mathlib found
no `Hausdorff-Young` or `Riesz-Thorin` declaration. These endpoints do not state the usual
intermediate `L^p -> L^q` family and cannot close an unidentified root. This search is intake
discovery, not an exhaustive candidate or transitive-trust audit.

## Required acceptance

The statement phase must first resolve the duplicate-target boundary and select one immutable
source proposition. It must then crosswalk every domain, measure, transform, exponent, function
space, hypothesis, conclusion, constant, and endpoint to the exact Lean expression, plus obtain an
independent source review. Until then the canonical statement and expression fingerprint remain
null, the human status is at most `H1`, and no machine or theorem-completion claim is legal.
