# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1773-1778` contains the title `黎斯 brothers 定理`, sole
attribution Marcel Riesz, year 1916, gloss `共轭函数的L^p有界性`, high importance, and
`已验证`. All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:6815-6840`
repeats the gloss while leaving the formal system, precise definitions and premises, proof history,
equivalent forms, axiom policy, machine status, and artifact links open. The rev-5.6 manifest resets
the record to `L0 / rework_required` and explicitly marks the source status untrusted.

The same catalog separately records `THM-M-0349` as Marcel Riesz's 1927 conjugate-function theorem
with the identical gloss, `THM-M-0350` as his 1928 Hilbert-transform `L^p` boundedness theorem, and
`THM-M-0247` as Kolmogorov's weak-type estimate. These are separate targets and provide no status or
evidence to this target.

## Literal crosswalk

| Catalog element | Source implication | Prospective Lean component | Intake result |
|---|---|---|---|
| `Riesz brothers theorem` | likely an F. and M. Riesz joint boundary/analytic-measure theorem | complex measure, circle Fourier coefficients, and absolute continuity | conflicts with gloss and sole attribution; root open |
| Marcel Riesz | points to a theorem by M. Riesz alone | source-specific conjugate operator and `L^p` carrier | conflicts with “brothers”; root open |
| 1916 | points to the early boundary-value work | exact historical edition, theorem passage, and modern equivalence bridge | source passage and dating convention open |
| conjugate-function `L^p` boundedness | points to the later strong-type theorem | exact transform and bound for `1 < p < infinity` | conflicts with title/year and duplicates `THM-M-0349` |
| `已验证` | untrusted inventory metadata | no proposition or proof term | explicitly rejected as H or M evidence |

## Inspected discovery sources

An immutable Encyclopedia of Mathematics revision, *Riesz theorem* (`oldid=48569`), describes a
theorem formulated and proved by brothers F. and M. Riesz in 1916 and comments with the familiar
one-sided-Fourier-vanishing complex-measure absolute-continuity form. Its observed HTML SHA-256 was
`b58201143faf042a58f8278d5799b6a6a539c02e1259260fcf73266fec64b930`.
K10plus/GVK catalog records identify F. and M. Riesz, *Ueber die Randwerte einer analytischen
Funktion*, pages 27-44, in proceedings for the 1916 fourth Scandinavian mathematical congress,
published in 1920. The observed SRU XML SHA-256 was
`a481fb45ddee3608683cd45a7c62c388f24662a7188da5d1b011b3de31d0feb1`.

A GDZ scan of Friedrich Riesz's 1923 paper *Ueber die Randwerte einer analytischen Funktion*,
*Mathematische Zeitschrift* 18, pages 87-95, was inspected at printed page 91; its footnote cites
the joint F. and M. Riesz congress work as Stockholm 1916, pages 27-44. The PDF SHA-256 was
`a5c5af44fc680a8d3c7b223b2cb82a176f4b61d71a8ee57b866bed9d7d68644d`.

A GDZ scan of Marcel Riesz, *Sur les fonctions conjuguees*, *Mathematische Zeitschrift* 27
(1928), pages 218-244, was inspected at printed pages 218, 220, and 225. It defines the periodic
conjugate-function setting for `p > 1`; Theorems I and II give a bound with a constant depending
only on `p` and conclude that an `L^p` function's conjugate belongs to `L^p`. The PDF SHA-256 was
`aa35ac5f5421a957db386ae080eae64a5d9b7aa37b8ef397e2fa180bc7d9906b`.
Crossref metadata for DOI `10.1007/BF01171098` confirms Marcel Riesz, volume 27, issue 1, and pages
218-244 with a 1928 publication date; the observed JSON SHA-256 was
`649b0736239cd1c4813c5d318a423b254dfbc81ae4f57a12cc8555cd3eea6008`.

These inspections decisively expose the catalog mismatch but do not themselves select the target
root or reach H0. The complete original definition chain, every incorporated assumption, precise
modern reformulation, proof-node mapping, correction/errata record, duplicate-target decision, and
independent source review remain open.

## Candidate-family crosswalk

| Candidate | Required mathematical fields | Lean substrate observed | Missing source gate |
|---|---|---|---|
| F. and M. Riesz analytic-measure form | finite complex Borel measure on a selected circle; exact Fourier convention and vanishing half-line; absolute-continuity conclusion | `ComplexMeasure`, root `fourierCoeff` for functions, Haar measure, and vector-measure absolute continuity are nearby APIs | primary definition chain, measure Fourier-Stieltjes bridge, correct direction and formulation, proof boundary, errata, independent review |
| Marcel Riesz strong-type form | selected conjugate/Hilbert transform on periodic or real-line `L^p`; `1 < p < infinity`; exact boundedness statement | `MeasureTheory.Lp`, `MemLp`, circle Haar measure, and Fourier coefficients are nearby APIs | primary passage, operator construction and normalization, endpoints, constant, duplicate ownership, proof boundary, errata, independent review |

## Lean and proof boundary

`IntakeProbe.lean` elaborates generic adjacent APIs against the pinned toolchain and mathlib. It
defines no target operator or theorem and supplies no proof body. A bounded mathlib name search did
not locate an exact F. and M. Riesz or conjugate-function terminal declaration; that observation is
not the later exhaustive anchor audit and not a claim of absence from all Lean projects.

Before statement acceptance, accountable reviewers must preserve lawful immutable primary source
editions, resolve the title/attribution/year/gloss conflict and duplicate ownership, select one exact
proposition, transcribe every definition, ordered binder, hypothesis, conclusion, boundary case,
normalization, and proof boundary, inspect corrections and errata, and independently approve the
source-to-Lean mapping. Until then H5 records an ill-posed catalog root, not a claim that either
candidate theorem is false or open.
