# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:754-759` supplies exactly the title `豪斯多夫-杨定理`, attribution
to Felix Hausdorff and William Young, the year 1923, the gloss `傅里叶变换的范数不等式`, importance
`高`, and status `已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2929-2953` repeats the gloss but explicitly leaves the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axiom
policy, machine-checked status, and artifact links as `待补充`. Rev-5.6 retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

| Catalog component | Prospective formal component | Intake assessment |
|---|---|---|
| "Fourier transform" | a specified transform from a measured group/space to its dual | domain, dual, kernel, sign, and measures absent |
| "norm inequality" | an exact `L^p` to `L^q` bound with a specified constant | spaces, exponents, membership, and constant absent |
| Hausdorff/Young, 1923 | provenance and source selection | bibliography absent; source/result mapping unreviewed |
| `已验证` | kernel or human-source evidence | explicitly untrusted; no receipt or proof body |

The repository wording identifies a recognizable theorem family, but it is not a truth-valued,
binder-complete statement. In particular, the conventional `1 <= p <= 2` and conjugate-exponent
form cannot be inserted into the canonical target without a source decision.

## Duplicate target boundary

The same corpus independently contains `THM-M-0295`, titled `豪斯多夫-杨不等式`, under
analysis/real analysis (`Docs/researches/math_theorems.md:2118-2123`). It has the same attribution
and year but the different gloss `傅里叶变换的L^p估计`. Its manifest rank is 1299; it remains a
separate L0 target. The two records are likely semantic duplicates, but neither record cites a
source or fixes a proposition. This dossier records the collision without importing `THM-M-0295`'s
wording, scope, status, or future evidence.

## Primary-source leads

- Felix Hausdorff, "Eine Ausdehnung des Parsevalschen Satzes uber Fourierreihen,"
  *Mathematische Zeitschrift* 16(1), 1923, pages 163-169, DOI
  `10.1007/BF01175679`. Crossref metadata identifies Hausdorff, the Fourier-series title, journal,
  volume, issue, pages, and December 1923 publication. Its deposited reference list directly cites
  Young's 1912 Parseval-generalization, multiplication-of-Fourier-constants, and summability work.
  That supports the historical provenance link, but not an exact result mapping. The publisher PDF
  endpoint returned an HTML access page rather than the article, so the theorem text was not
  inspected.
- W. H. Young, "On the Determination of the Summability of a Function by Means of its Fourier
  Constants," *Proceedings of the London Mathematical Society* s2-12(1), 1913, pages 71-88, DOI
  `10.1112/plms/s2-12.1.71`. Crossref metadata confirms the bibliographic record. The full article
  was not admitted or inspected.

These are primary bibliographic leads, not H0 packets. The catalog does not cite either source or
say whether its target is Hausdorff's Fourier-series formulation, a later Euclidean/LCA extension,
or another normalization. A complete source edition, exact theorem/equation/page locator,
incorporated definitions, assumption and conclusion map, proof-node boundary, errata search,
translation decisions, lawful repository preservation, and independent review remain open.

A later secondary lead, Michael Christ, arXiv `1406.1210v1`, introduction equations (1.1)-(1.3),
exhibits why the missing choices are material: for its specified Euclidean transform normalization
it records the sharp Hausdorff-Young-Beckner constant depending on `p`, its conjugate exponent, and
the dimension. This is evidence of normalization/constant ambiguity only. It is a later sharp
refinement, not the uncited 1923 catalog source and not the canonical target.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Module/declaration | Exact checked role | Credited status |
|---|---|---|
| `Mathlib.Analysis.Fourier.FourierTransform`: `Real.Lp.fourierTransformCLM` | `L1` Fourier transform to bounded continuous functions with operator-norm bound one | endpoint/API discovery only |
| `Mathlib.Analysis.Distribution.SchwartzSpace.Fourier`: `SchwartzMap.norm_fourier_Lp_top_leq_toLp_one` | Schwartz `L1 -> L-infinity` norm inequality | endpoint theorem only |
| `Mathlib.Analysis.Fourier.LpSpace`: `MeasureTheory.Lp.fourierTransform_lI` and `MeasureTheory.Lp.norm_fourier_eq` | `L2` Fourier isometry and Plancherel norm equality | endpoint theorem only |

The Lean spellings use the Unicode declaration `fourierTransformₗᵢ`; the ASCII spelling above is
only a readable label. A bounded case-insensitive search of repo-local Lean and pinned mathlib
found no `Hausdorff-Young` or `Riesz-Thorin` declaration. The endpoint results do not state the
usual intermediate `L^p -> L^q` family and cannot close an unidentified root. This search is
intake discovery, not exhaustive candidate or transitive-trust audit.

## Required acceptance

The statement phase must first resolve the duplicate-target boundary and select one immutable
source proposition. It must then crosswalk every domain, measure, transform, exponent, function
space, hypothesis, conclusion, constant, and endpoint to the exact Lean expression, plus obtain an
independent source review. Until then the canonical statement and expression fingerprint remain
null, the human status is at most `H1`, and no machine or theorem-completion claim is legal.
