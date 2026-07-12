# Source-statement crosswalk

The complete repository claim is `极小曲面的刚性定理` ("a rigidity theorem
for minimal surfaces"). The same record gives the title `辛格定理`, the
proposer `James Simons`, and the year 1968. This crosswalk preserves those
facts without silently choosing one of several materially different theorems.

| Claim component | Human source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Repository root and attribution | `Docs/researches/math_theorems.md`, entry `辛格定理`; reproduced as `THM-M-0167` in `Docs/Stage0_Blueprint.md` | None selected | Authoritative local wording, but not an exact proposition; `辛格`/Singer conflicts with James Simons |
| Simons 1968 minimal-submanifold theory | James Simons, "Minimal varieties in Riemannian manifolds," *Annals of Mathematics*, Second Series 88 (1968), 62-105, DOI `10.2307/1970556` | Candidate theorem family only | Primary paper matching author, year, and subject identified; exact theorem/page/formula and premise mapping are not yet pinned |
| Differential identity/inequality for the second fundamental form | The 1968 Simons paper develops the second-variation and curvature identities underlying rigidity results | No formal target | Could be the intended theorem or a proof ingredient; repository wording does not decide |
| Spherical pinching or gap conclusion | Classical results derived from Simons-type inequalities for minimal submanifolds in a sphere | Candidate strict-bound rigidity statement | Ambient radius, dimension, codimension, norm convention, threshold, compactness, and strictness are absent locally |
| Sharp equality classification | Later minimal-submanifold rigidity literature, including classifications at extremal thresholds | Unselected refinement | Must be separated from the 1968 root unless a pinpoint source proves it is part of the selected claim |
| Singer local-homogeneity theorem | I. M. Singer, "Infinitesimally homogeneous spaces," *Communications on Pure and Applied Mathematics* 13 (1960), 685-697 | Explicitly excluded candidate | Matches the literal title transliteration but not the repository's author, year, or minimal-surface description |
| Pinned Lean/mathlib substrate | Repository's pinned Lean 4/mathlib environment | None | A literal source-tree search found only Ivan Singer bibliography mentions, not this minimal-submanifold theorem; this is discovery evidence, not an anchor-audit conclusion |

The word "surface" could mean dimension exactly two, while Simons's paper and
many results called Simons theorems concern higher-dimensional minimal
submanifolds. Likewise, "rigidity" might refer to total geodesy under strict
pinching, an equality-case classification, or rigidity encoded by a
differential identity. These alternatives change the domain, binders,
hypotheses, constants, and conclusion, so they cannot share an unchecked Lean
statement.

The Simons and Singer citations above are bibliographic discovery anchors, not
immutable evidence receipts. `H1` records a published theorem family with a
matching primary source identified. It does not claim `H0`: exact
theorem/section/page, edition hash, assumptions, notation translation,
correction/errata status, source-to-node mapping, and independent review remain
open.
