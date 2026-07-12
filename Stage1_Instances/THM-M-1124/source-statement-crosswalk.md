# Source-statement crosswalk

## Repository record and candidate primary sources

The repository inventory supplies the title "Lawler-Schramm-Werner theorem", the authors
Lawler/Schramm/Werner, the year 2001, and the gloss "SLE and critical phenomena". Its `已验证`
field is explicitly untrusted under rev-5.6. It gives no paper, theorem number, exponent notation,
parameter range, geometric setting, hypotheses, or formula, so it cannot identify an exact claim.

Strong primary-source candidates are Gregory F. Lawler, Oded Schramm, and Wendelin Werner,
*Values of Brownian intersection exponents I: Half-plane exponents*, **Acta Mathematica** 187
(2001), 237-273, and *Values of Brownian intersection exponents II: Plane exponents*, **Acta
Mathematica** 187 (2001), 275-308. A related continuation is *Values of Brownian intersection
exponents III: Two-sided exponents*, **Annales de l'Institut Henri Poincare, Probabilites et
Statistiques** 38 (2002), 109-123. These bibliographic leads have not been inspected here against
an immutable edition theorem by theorem. They are discovery anchors, not `H0` evidence, and the
2001 metadata does not choose between the first two papers or a particular corollary.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "Lawler-Schramm-Werner" | exact paper and numbered theorem | source identity attached to canonical expression | author family known; result open |
| "SLE" | SLE parameter, geometry, and restriction/disconnection input | Loewner chain, driving process, hull/event interfaces | method indicated only |
| "critical phenomena" | exact Brownian or model-specific observable | concrete probability event and asymptotic statement | too broad to determine a claim |
| intersection exponent | avoidance event and decay exponent | stopped Brownian paths, independence, probability, limit | provisional family only |
| half-plane/plane | domain, boundary data, and crossing/disconnection convention | complex domain and measurable events | unresolved and proposition-critical |
| explicit value | formula, normalization, and parameter range | real-valued expression and quantified equality | exact formula open |
| 2001 | bibliographic disambiguation | no machine-proof credit | matches multiple candidate results |

## Human and machine boundary

Repository-wide and pinned-mathlib text searches found no theorem-specific Lean artifact under the
target name or the Brownian-intersection-exponent terminology. This negative local search is not
the later exhaustive formal-anchor audit and makes no claim about all external Lean 4 projects.

Before `H0`, an independent reviewer must inspect an immutable primary edition, select the exact
numbered result, record page and definitions, map every hypothesis and parameter restriction, check
errata and corrections, and approve the row-by-row mapping. Before statement credit, that result
must map to an elaborated Lean target without replacing the asymptotic theorem by an abstract
assumption, selecting a convenient special exponent, or changing plane and half-plane conventions.
