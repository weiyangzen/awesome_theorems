# Source-statement crosswalk

| Source component | Repository evidence | Possible formal counterpart | Intake assessment |
|---|---|---|---|
| Name | `THM-M-0454`, `沙法列维奇-泰特群` | A declaration defining an object named `Sha` | An object name is not a theorem statement |
| Gloss | Stage0: `椭圆曲线的Tate-Shafarevich群` | An elliptic curve over some global field | Curve and field are not quantified or fixed |
| Status | Stage0/manifest: `已验证` (manifest explicitly marks it untrusted) | No proposition follows from this label | No human- or machine-proof credit |
| Date/attribution | Stage0 says 1958 and Igor Shafarevich/John Tate | Historical discovery metadata | No edition, theorem number, page, assumptions, or errata record |
| Property | Absent | Definition, torsor classification, finiteness, duality, or a curve-specific computation | Selecting one would broaden or substitute the target |

The conventional object is often described using everywhere locally trivial cohomology classes,
but even writing that as a kernel requires a chosen global field, its places and completions, and
an elliptic curve or abelian variety. This dossier deliberately does not promote that background
description into the canonical proposition.

## Required source decision

Before statement elaboration, an authoritative source amendment must provide all of:

1. a proposition rather than an object label;
2. the precise class of global fields and elliptic curves or abelian varieties;
3. ordered assumptions and conclusion, including any finiteness or reduction hypotheses;
4. a primary-source edition, theorem/page anchor, assumptions, and errata disposition.

Until then, exact statement fidelity is `H5`, Lean encoding is `M4`, and there is no eligible proof
root. No primary-source or external formalization search result is asserted by this intake phase.
