# Source-statement crosswalk

| Claim component | Human source anchor | Lean target candidate | Intake assessment |
|---|---|---|---|
| Terminology and attribution | Repository source row says "Schwartz对称化", Laurent Schwartz, 1950; standard references instead use *Schwarz symmetrization* or *symmetric decreasing rearrangement* | dossier canonical name only | The repository row is an untrusted discovery lead. Spelling, attribution, date, and intended result require primary-source verification. |
| Rearranged superlevel sets are centered balls of equal measure | B. Kawohl, *Rearrangements and Convexity of Level Sets in PDE*, Lecture Notes in Mathematics 1150, Springer (1985), introductory rearrangement definitions; exact pages/edition scan not yet accepted | future distribution-function and ball-volume definitions | Credible secondary monograph anchor, not H0: no immutable copy, pinpoint page, premise map, or errata audit. |
| `f*` is radial and decreasing | E. H. Lieb and M. Loss, *Analysis*, 2nd ed., AMS GSM 14 (2001), Chapter 3, "Rearrangements"; exact definition/page must be checked | future radiality and antitonicity predicates | Credible secondary textbook anchor only. |
| Equimeasurability: `mu {f* > t} = mu {f > t}` | Same rearrangement definition and layer-cake framework | future theorem over Lebesgue measure on Euclidean space | Intended root property; strict/non-strict threshold and a.e. conventions remain unresolved. |
| Existence via distribution function/generalized inverse | Standard construction in the two references above | future constructor plus measurability proof | Architecture candidate only; no Lean API or proof is credited. |

The dossier deliberately does not cite the neighboring Pólya-Szegő inequality as the target: that is
separately represented by `THM-M-1286` and is a consequence requiring Sobolev assumptions. Nor does
it infer formal verification from the source metadata label "已验证".

No `H0` claim is made. The source-audit phase must locate the intended primary historical source,
resolve Schwarz versus Schwartz and the 1950 attribution, record immutable edition/file hashes and
pinpoint pages, map every assumption and conclusion, search corrections/errata, and obtain an
independent review. The statement phase must then select the exact Euclidean-space representation,
codomain, measurability API, finite-superlevel hypothesis, threshold convention, and a.e. equality
policy before inspecting proof closure.
