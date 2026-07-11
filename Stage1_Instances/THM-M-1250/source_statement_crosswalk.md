# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Entry identity | `Docs/Stage0_Blueprint.md`, `THM-M-1250`: "Schwartz空间", content "速降函数空间", attributed to Laurent Schwartz, 1950 | `SchwartzMap` | Exact repository source wording recorded; its `已验证` label is explicitly untrusted by rev-5.6 |
| Smooth rapidly decreasing functions | Laurent Schwartz, *Theorie des distributions*, 1950-1951 is the named historical source family | `Mathlib.Analysis.Distribution.SchwartzSpace.Basic` | Bibliographic discovery anchor only; edition, volume, page, exact definition, and errata have not been audited |
| Weighted derivatives decay | Standard modern characterization: every derivative remains bounded after multiplication by every polynomial weight | `SchwartzMap.seminorm`, `SchwartzMap.norm_pow_mul_le_seminorm` (repo-local candidate names) | Candidate semantic bridge; no exact type inspection or checked equivalence in this phase |
| Smoothness | Membership entails smoothness | `SchwartzMap.smooth` (repo-local candidate name) | Candidate consequence, not selected as the root theorem |
| Fourier stability | Fourier transform maps Schwartz functions to Schwartz functions | candidate API under `Mathlib.Analysis.Distribution.SchwartzSpace.Fourier` | Important closure theorem but broader than the source gloss; excluded from the root unless separately justified |

The source metadata identifies a space rather than a truth-valued theorem. Several honest Lean
targets are possible: a membership characterization, smoothness, closure under derivatives, or
Fourier invariance. They are not interchangeable. The statement phase must choose one target whose
human claim is supported by a pinpointed source, inspect its exact Lean type, and test that domain,
binder, hypothesis, and dimension mutations do not silently change the claim.

No `H0` or machine-closure claim is made. Primary-source edition/page/assumption mapping, errata
review, immutable mathlib revision, terminal declaration provenance, and independent review remain
open.

