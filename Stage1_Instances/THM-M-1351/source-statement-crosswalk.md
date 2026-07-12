# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9852-9857` records the Chinese title `Poincaré映射`, Henri
Poincare, 1881, and the gloss `周期轨道的稳定性` (stability of periodic orbits). The same catalog
repeats those six fields at lines 10306-10311. `Docs/Stage0_Blueprint.md:36750-36775` assigns
`THM-M-1351` but explicitly
leaves exact definitions, premises, proof route, axioms, and formal artifacts open. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted`.

The catalog gives no work title, edition, theorem or section, page, stable archive locator, exact
statement, proof boundary, translation provenance, errata, or reviewer. Its attribution and date do
not identify which historical construction or later stability theorem is intended.

## Inspected source-family discriminator

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, AMS, 2012, DOI `10.1090/gsm/140`, was inspected as an authoritative modern
discovery source. Section 12.2, printed pages 317-318, visibly separates:

- equation (12.9), defining a local Poincare map using a transversal and return time;
- Lemma 12.2, equivalence of (asymptotic) stability of a periodic orbit and of the fixed point;
- Corollary 12.3, a sufficient derivative-eigenvalue condition for asymptotic stability;
- Theorem 12.4, comparison of the derivative spectrum with the monodromy spectrum.

This separation is evidence that the catalog gloss is ambiguous, not evidence selecting a target.
The author-hosted preliminary edition was inspected outside the repository. Running
`pdftotext -f 328 -l 329 -layout` on that PDF produced the 6,781-byte inspected extract with
SHA-256 `990e8a5c8e7c21c1ea9ca08dd57112ba46c1328ccecb5ea75343ab1742969880`.
No mutable remote file is admitted as an immutable H0 packet, and no complete assumption/errata
mapping or independent review is claimed.

## Crosswalk

| Catalog component | Candidate mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `Poincaré映射` | first return to a local transverse section | a source-defined return-time function composed with `Flow` | construction absent; no canonical expression |
| periodic orbit | orbit of a nonconstant periodic solution | `Flow.orbit`, continuous-time periodicity, compact orbit | generic orbit API probed; exact definition open |
| fixed point of return map | the chosen orbit/section intersection | `Function.IsFixedPt` | generic predicate only |
| stability | orbital/asymptotic stability or attraction | source-specific neighborhood and convergence predicates | no matching predicate selected |
| derivative criterion | spectrum of the derivative inside/outside the unit circle | `HasFDerivAt` plus finite-dimensional spectral interfaces | one possible theorem, not selected |
| return-map existence | first return time near the base point | flow regularity, transversality, implicit-function machinery | only generic ingredients probed |
| `已验证` | untrusted inventory field | no declaration or proof body | explicitly rejected as evidence |

## Required source admission

The statement phase must select an immutable source passage, transcribe its incorporated definitions,
ordered assumptions, exact conclusion, and proof boundary, record edition/page and errata, reconcile
the 1881 attribution, and obtain independent source review. It must then explain why that passage,
rather than the other standard results above, is the intended target. Until those steps occur, H5
records an unstable catalog proposition and the canonical Lean target remains null.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe imports
generic flow, periodic-point, derivative, and implicit-function modules. A bounded name search finds
references to Poincare maps but no source-identical return-map stability declaration. This is only
intake discovery; the later immutable anchor audit remains open.
