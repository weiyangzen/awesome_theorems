# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1759-1764` records the title `林德勒夫定理`, attributes it only to
Ernst Lindelof, gives the year 1908, and supplies the gloss `角区域内的Phragmen-Lindelof原理`.
All six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
`Docs/Stage0_Blueprint.md:6761-6786` repeats the gloss while explicitly leaving the exact definitions
and premises, proof route, dependencies, alternate forms, axioms, machine status, and artifacts
open. The rev-5.6 manifest retains `已验证` only as untrusted source metadata.

The catalog does not cite a paper, theorem, section, page, edition, translation, or erratum. It also
omits E. Phragmen from the attribution even though the identifiable 1908 paper is joint work. This
metadata identifies a theorem family, not a binder-complete proposition or `H0` source record.

## Inspected primary-source lead

E. Phragmen and Ernst Lindelof, *Sur une extension d'un principe classique de l'analyse et sur
quelques proprietes des fonctions monogenes dans le voisinage d'un point singulier*, Acta
Mathematica 31 (1908), 381-406, DOI `10.1007/BF02415450`, was inspected in a 26-page published scan
served by Zenodo record `2177451`. The Crossref response and scan agree on the title, journal,
volume, year, and page range. The Zenodo record agrees on title and year, identifies the same DOI,
and serves the scan; the scan confirms the joint authorship. They were observed on 2026-07-13. The
observed PDF has SHA-256
`f9eaba25b730f11a762b67e0bd8472198e08c918689ab6b9c4ad4917264989a8`.

The source contains several materially distinct candidates:

- Part II, no. 4, journal page 385, treats a holomorphic function in the centered sector
  `-pi / (2 * alpha) < arg x < pi / (2 * alpha)`. It assumes condition `(A)` at every finite
  boundary point and a positive `k < alpha` for which `exp (-r ^ k) * f x` tends uniformly to zero
  inside the sector as `r` tends to infinity, and concludes the maximum bound inside.
- Part II, no. 5, journal pages 385-387, first generalizes the growth premise and then states a theorem
  for a connected domain contained in a sector of opening `pi / alpha`, with boundary condition
  `(A)` at finite points and, for every positive `epsilon`, uniform convergence of
  `exp (-epsilon * r ^ alpha) * f x` to zero as `r` tends to infinity.
- Part I, nos. 1-2, journal pages 381-383, gives a more general exceptional-boundary-point principle from
  which later applications are derived.

At Part I, no. 1, condition `(A)` means that for each boundary point `xi` and every positive
`epsilon`, `|f x| < C + epsilon` once `x`, remaining inside the domain, is sufficiently close to
`xi`. The referenced conclusion `(1)` is the interior maximum bound, strict unless the function is
constant. These formulas are transcriptions for crosswalk and variant selection, not accepted H0
records.

This is primary mathematical evidence and a strong source lead. It is not accepted as `H0`: the
catalog does not select no. 4, no. 5, or the general principle; formula transcription needs
independent checking against the scan; exact definitions, assumptions, translation, correction and
errata status, and source-to-Lean mapping have not been independently reviewed.

## Component crosswalk

| Catalog component | Primary-source alternatives | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| `角区域` (angular region) | centered sector in Part II no. 4; arbitrary connected domain contained in a sector in Part II no. 5 | four coordinate quadrants; right half-plane; strips | exact geometry and transport open |
| Phragmen-Lindelof premise | boundary condition `(A)` plus one of several angle-sensitive growth conditions | `DiffContOnCl`, boundary norm bounds, filter-based `IsBigO` hypotheses | not one-to-one without source selection |
| boundary | two rays and finite boundary points; vertex/infinity handled through source conditions | explicit real and imaginary axes for quadrants; boundary lines for strips | source conventions and closure open |
| conclusion | maximum bound `|f| < C` or `<= C`, with variants and corollaries | norm bound, `EqOn` zero, or `EqOn` extensionality | canonical conclusion open |
| `已验证` | untrusted catalog label | no exact root identity or accepted receipt | no H or M credit |

## Pinned Lean candidate family

`Mathlib.Analysis.Complex.PhragmenLindelof` is a proof-bearing exact-topic module. The bounded intake
probe checks `PhragmenLindelof.horizontal_strip`, `vertical_strip`, `quadrant_I` through
`quadrant_IV`, `right_half_plane_of_tendsto_zero_on_real`, and
`right_half_plane_of_bounded_on_real`. Pinned mathlib's `docs/1000.yaml` maps the title
"Phragmen-Lindelof theorem" to `PhragmenLindelof.horizontal_strip`. That title mapping is discovery
metadata, not proof that the horizontal-strip declaration is the catalog's angular-region root.

The declarations are credible future `M0-W` candidates for selected variants or checked
transports. Intake does not credit an accepted exact root because no source variant is selected,
no arbitrary-angle declaration is exposed, and the required expression, transport, provenance,
trust, and master gates remain open.

Before the statement phase can close, accountable reviewers must select and preserve one exact
source theorem, transcribe its definitions, ordered binders, premises, growth and boundary
conditions, and conclusion, audit corrections and translation, and independently approve the
crosswalk. The statement phase must then elaborate the matching Lean target with minimal imports,
check every credited transport, and run the required removed-hypothesis, changed-domain,
binder-scope, and boundary mutations.
