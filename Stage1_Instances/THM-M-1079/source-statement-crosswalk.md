# Source-statement crosswalk

## Repository source

The repository's discoverable source is `Docs/researches/math_theorems.md`, which records the name
"martingale difference sequence", attribution to many mathematicians, the twentieth century, and
the description "properties of martingale difference sequences". `Docs/Stage0_Blueprint.md`
repeats that description but supplies no formula, hypotheses, named property, proof, or source.
Thus the metadata identifies an object family but not a unique theorem statement. Its `已验证`
label is not source or machine evidence.

## Bibliographic leads

- P. Hall and C. C. Heyde, *Martingale Limit Theory and Its Application*, Academic Press, 1980.
  This is a direct monograph lead for martingale difference sequences and their limit theory.
- D. Williams, *Probability with Martingales*, Cambridge University Press, 1991. This is a standard
  discrete-time martingale reference and a lead for the increment/partial-sum characterization.

These are discovery leads only. Exact edition, chapter/result/page, definition convention,
assumptions, proof coverage, and errata have not been directly audited, so they do not establish
`H0`. The anchor-audit phase must not use the references to retroactively choose a convenient root.

## Crosswalk

| Repository phrase | Mathematical surface | Required Lean surface | Intake status |
|---|---|---|---|
| martingale difference sequence | integrable adapted discrete-time differences with conditional mean zero | probability space, filtration, process, integrability, measurability, conditional expectation equality a.e. | object family included; indexing/codomain open |
| properties | no particular proposition is named | one exact elaborated root declaration | unresolved; first downstream blocker |
| partial-sum property | conditional-mean-zero differences produce a martingale | finite sums plus `MeasureTheory.Martingale`-compatible hypotheses | candidate only, not source-selected |
| increment property | martingale increments have conditional mean zero | subtraction process and conditional expectation law | candidate only, not source-selected |
| orthogonality/isometry | square-integrable differences give `L2` identities | second-moment hypotheses, integrals, pairwise orthogonality | excluded unless exact source selects it |
| concentration | bounded differences imply tail estimates | exponential bounds and bounded-increment hypotheses | not this intake; neighboring Azuma targets |

## Evidence boundary

No Lean declaration or terminal proof body is accepted by this intake, and no mathlib or external
search result is being claimed. The dependent statement and anchor-audit phases must record exact
modules, declaration types, immutable revisions, dependency feasibility, axioms, placeholders, and
terminal proof provenance. Human status can reach `H0` only after a primary or authoritative source
location and its complete assumption-to-node crosswalk receive independent review.
