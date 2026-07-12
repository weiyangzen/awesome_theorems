# Source-statement crosswalk

## Repository record and candidate sources

The repository inventory gives the title "conformal field theory and SLE", the attribution "many
mathematicians", the period "21st century", and the gloss "the connection between CFT and SLE".
Its `已验证` field is explicitly untrusted under rev-5.6. It supplies no authors, paper, theorem
number, CFT axioms, SLE variant, parameter range, or conclusion, and therefore does not identify an
exact proposition.

A primary candidate for the intended Virasoro/SLE family is Michel Bauer and Denis Bernard,
*Conformal Field Theories of Stochastic Loewner Evolutions*, **Communications in Mathematical
Physics** 239 (2003), 493-521, DOI `10.1007/s00220-003-0881-x`, preprint arXiv:hep-th/0210015.
It develops the Virasoro representation and martingale relationship for SLE. This intake has not
inspected an immutable edition result by result, so no formula, locator, hypothesis, or correction
from it is yet accepted.

Another primary candidate is Roland Friedrich and Wendelin Werner, *Conformal Restriction,
Highest-Weight Representations and SLE*, **Communications in Mathematical Physics** 243 (2003),
105-122, DOI `10.1007/s00220-003-0948-8`, preprint arXiv:math-ph/0301018. Its restriction and
highest-weight formulation is related but not interchangeable with every Bauer-Bernard martingale
claim. Both entries are discovery anchors, not `H0` evidence, and neither may be selected solely
because its topic matches the repository slogan.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "SLE" | variant, domain, marked points, `kappa`, Loewner/Brownian normalization | filtered probability space, Brownian driver, Loewner solution and stopping time | chordal family intended; exact setup open |
| "CFT" | rigorous algebraic/analytic CFT fragment used by the source | Virasoro algebra/module, highest-weight vector, or explicitly axiomatized correlator interface | Virasoro fragment intended; encoding open |
| central charge and weight | source-normalized `c(kappa)` and `h(kappa)` | scalar formulas with side conditions and equality in the coefficient field | expected bridge; exact convention open |
| level-two null vector | precise `L_{-2}`/`L_{-1}^2` relation | module action and exact vector equality | intended core relation; coefficients open |
| SLE/CFT connection | theorem direction linking degeneracy and stochastic evolution | checked map from the algebraic identity to an adapted local-martingale claim | slogan only; exact conclusion open |
| martingale observable | correlation/partition function, marked insertions, lifetime | measurable adapted process, localization, drift cancellation, integrability if needed | observable and strength unresolved |

## Human and machine boundary

A repository-local search found no artifact named for `THM-M-1125`. The pinned mathlib text search
found uses of "Loewner" for the order on positive operators, not Schramm-Loewner evolution; this is
only a narrow intake observation, not the later exhaustive anchor audit. Adjacent legacy CFT files
are discovery material for other theorem IDs and receive no statement or proof credit here.

Before `H0`, an independent reviewer must inspect an immutable primary edition, select an exact
numbered theorem or displayed result, map every definition and assumption, check errata and later
corrections, and approve the row-by-row mapping. Before statement credit, the selected claim must
be mapped to an elaborated Lean target without treating the desired CFT identities as hypotheses,
changing the SLE variant, deleting stopping/integrability conditions, or replacing a stochastic
theorem with a formal algebra calculation.
