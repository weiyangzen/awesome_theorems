# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2104-2109` supplies exactly the Chinese name `赫维茨定理`, Adolf
Hurwitz, 1903, the gloss `傅里叶级数的绝对收敛`, importance "medium," and status `已验证`. All six
lines originate in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. There is no
bibliography, formula, definition chain, ordered binder list, theorem locator, proof, correction
history, or formal artifact.

`Docs/Stage0_Blueprint.md:8089-8114` repeats these fields and explicitly leaves the formal system,
precise definitions and premises, proof process, dependencies, equivalent forms, axioms, machine
status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Primary-work lead

Crossref and the inspected GDZ issue agree on the following source:

> Adolf Hurwitz, *Über die Fourierschen Konstanten integrierbarer Funktionen*, *Mathematische
> Annalen* 57 (1903), 425-446, DOI `10.1007/BF01445179`.

The complete GDZ article scan was inspected. Its PDF has 23 pages including a rights/metadata cover;
the article itself is printed pages 425-446. The source is in German. It is a primary-work lead and
supports `H1`, not `H0`: the scan is not preserved in this repository, no accountable reviewer has
approved a translation or exact root selection, and the definitions, proof boundary, corrections,
errata, and source-to-node mapping have not been completely audited.

## Pinpoint source crosswalk

| Source location | Observed mathematical content | Relationship to catalog gloss | Intake result |
|---|---|---|---|
| pp. 425-427, equations (1)-(3) | Riemann-integrable `f` on `[0, 2*pi]`; real cosine/sine Fourier constants and series notation | fixes one historical coefficient convention | definitions observed; no formal transport accepted |
| pp. 429-436, Satz IV and equations (5), (7), (26) | Parseval-type bilinear and square identities for integrable functions | adjacent Fourier-coefficient closure, not plainly the catalog gloss | candidate architecture only |
| p. 436 after equation (27) | the mixed coefficient-product series is said to be absolutely convergent, even after separating its products | a literal absolute-convergence statement, but about a bilinear coefficient series | candidate root; not selected |
| pp. 438-439, Satz VI and equations (28)-(34) | interval integrals are represented by an absolutely convergent trigonometric series | closest direct match if the intended function is an indefinite integral | candidate root; additive constant/endpoints/encoding open |
| pp. 439-440, Satz VII | Fourier constants of a function are recovered by termwise differentiation from an indefinite integral expansion under a periodicity condition | supporting bridge for the integral-series branch | not a root selection |
| pp. 441-442, Satz VIII and equation (37) | uniqueness modulo functions "of integral zero" and Fejer recovery at continuity points | neighboring uniqueness/convergence result | explicitly not absolute-summability evidence |
| pp. 442-446, Satz IX | vanishing initial Fourier coefficients force at least `2k` sign intervals | Sturm-Hurwitz theorem | excluded unless the catalog is corrected |

The paper's own title and scope concern "Fourier constants of integrable functions," not a single
modern theorem called "absolute convergence of Fourier series." The catalog gloss could refer to
the p. 436 product series, the pp. 438-440 indefinite-integral expansion, or a later theorem-family
summary. That ambiguity is proposition-changing.

## Literal catalog-to-Lean crosswalk

| Catalog element | Candidate mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `赫维茨定理` | one of several Hurwitz theorems | exact declaration tied to one reviewed source theorem | identity open |
| Adolf Hurwitz, 1903 | 1903 *Mathematische Annalen* paper | immutable source revision, translation, page/formula map, reviewer receipt | primary scan inspected; review open |
| `傅里叶级数` | real sine/cosine series on `[0,2*pi]` or complex series on a circle | `AddCircle`, `fourierCoeff`, and checked normalization/domain transports | adjacent APIs elaborate; transport absent |
| `绝对收敛` | coefficient-norm summability, evaluated-term absolute convergence, uniform absolute convergence, or absolute mixed-product convergence | precise `Summable`/`HasSum` expression and topology/norm | meaning open |
| `已验证` | untrusted inventory metadata | primary proof audit plus kernel and receipt evidence | no H0 or M0 credit |

## Pinned Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Fourier.AddCircle` provides:

- `fourierCoeff`, a complex Fourier-coefficient function on `AddCircle T`;
- `hasSum_sq_fourierCoeff` and `tsum_sq_fourierCoeff`, Parseval/L2 interfaces;
- `hasSum_fourier_series_of_summable`, which assumes `Summable (fourierCoeff f)` and concludes
  uniform convergence of the Fourier series of continuous `f`; and
- `has_pointwise_sum_fourier_series_of_summable`, its pointwise consequence.

`IntakeProbe.lean` elaborates these exact interfaces. They establish `M3` statement/interface
availability only. In particular, the convergence theorem consumes absolute summability rather
than deriving it from source-selected Hurwitz hypotheses. No exact source-mapped statement,
normalization transport, terminal proof body, provenance, axiom closure, or proof credit is claimed.

## Retry condition

An independent source reviewer must decide whether the catalog denotes the p. 436 coefficient-
product claim, the pp. 438-440 indefinite-integral series, another exact passage, or a corrected
later theorem. The reviewer must approve the German transcription/translation, definitions,
ordered binders, hypotheses, conclusion, proof boundary, corrections and errata, and exact meaning
of absolute convergence. Only then may the statement phase encode and mutation-test a Lean target.
