# Source-statement crosswalk

## Repository evidence

The authoritative manifest and its Stage0 source trace only to
`Docs/researches/math_theorems.md:1294-1299`. That record supplies the Chinese label, Shing-Tung Yau,
the year 1978, the phrase "lower-bound estimate for the first eigenvalue," and an untrusted
`已验证` status. It supplies no bibliography or mathematical formula.

| Metadata component | Repository wording | Primary-source mapping | Intake assessment |
|---|---|---|---|
| Name | `丘成桐估计` | Not identified | Not a unique bibliographic title |
| Attribution | Shing-Tung Yau | Not independently checked | Discovery key only |
| Year | 1978 | Not independently checked | Discovery key only |
| Claim | First-eigenvalue lower-bound estimate | No theorem/page or assumption map | Insufficient to define a proposition |
| Formal status | `已验证` | No project, revision, module, or declaration | Untrusted; no machine credit |

## Collision and neighboring records

The same repository source has a separate 1975 PDE entry with the same Chinese name
(`THM-M-1319`) and an almost identical gloss. Nearby entries separately name the Li-Yau and
Zhong-Yang estimates and Yau's eigenvalue conjecture. In the differential-geometry sequence,
`THM-M-0180` instead names the Cheng-Yau maximum principle and describes an eigenfunction gradient
estimate. These records narrow the bibliographic search but do not identify the 1978 result.

## Required source work

The source audit must locate candidate 1978 Yau publications, inspect an immutable edition, record
the exact theorem/section/page and any errata, and map every domain choice, binder, hypothesis,
normalization, conclusion, and degenerate case. A qualified independent reviewer must approve that
mapping before `H0`. The current `H1` is provisional source-reconstruction debt, not a claim that a
specific paper or exact proposition has been verified.

The later Lean crosswalk must then map the selected manifold/domain, operator and spectrum,
curvature and global controls, eigenvalue indexing, and numerical bound to concrete pinned APIs.
No Lean candidate is credited at intake.
