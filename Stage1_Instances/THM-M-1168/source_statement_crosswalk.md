# Source-statement crosswalk

| Claim component | Repository source anchor | Primary source anchor | Lean target | Intake assessment |
|---|---|---|---|---|
| Name | Stage0 `THM-M-1168`: `内部估计` | None supplied | None | Names a broad PDE theorem family |
| Human claim | Stage0: `解在内部的正则性` (regularity of solutions in the interior) | None supplied | None | Insufficient to distinguish elliptic/parabolic systems or weak/classical solutions |
| Provenance | Stage0 proposer/source: `众多数学家` | None supplied | None | No author, work, edition, theorem, or page can be audited |
| Formal status | Stage0: `已验证` | No evidence receipt supplied | None | Untrusted discovery metadata; grants no H or M closure |
| Rev-5.6 scope | Legacy Stage1 profile `partial_differential_equations` | To be identified | Lean 4 + mathlib | Allows source/statement work but does not define the root |

## Missing statement fields

The exact-source audit must recover all of the following before statement
normalization: PDE/operator; elliptic or parabolic regime; scalar versus system;
ambient dimension and domain hypotheses; coefficient regularity and uniform
ellipticity/parabolicity constants; forcing-term space; weak, strong, or
classical solution notion; compactly-contained subdomain or nested-ball
geometry; source and target norms; derivative and regularity orders; constants'
dependencies; and all boundary/degenerate exclusions.

## Non-equivalent candidate families

Classical Schauder, Calderon-Zygmund/`W^{2,p}`, De Giorgi-Nash-Moser, harmonic,
and parabolic interior estimates are useful discovery headings, but none is a
crosswalked source for this target. They differ in assumptions and conclusion,
so choosing one at intake would broaden or substitute the inherited claim.

No `H0` or exact-statement claim is made. The next phase must locate a primary
source whose wording can be justified as the catalog referent, record immutable
edition/page/theorem and errata data, and only then construct a binder-by-binder
Lean crosswalk and mutation tests.
