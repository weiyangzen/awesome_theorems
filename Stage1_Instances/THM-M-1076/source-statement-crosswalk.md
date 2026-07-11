# Source-statement crosswalk

## Repository source

| Claim component | Source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/Stage0_Blueprint.md`, THM-M-1076, "Smith关键更新定理" | none | Fixes a name only; it is not an exact proposition |
| Attribution and date | `Docs/researches/math_theorems.md`: Walter Smith, 1954 | none | Untrusted discovery metadata; the bibliographic work and date must be checked against a primary publication |
| Mathematical description | same record: "更新过程的极限行为" | none | Omits all domains, binders, hypotheses, normalization, and the conclusion formula |
| Historical verification label | manifest field `source_status_untrusted: 已验证` | none | Explicitly untrusted under rev-5.6 and grants no H or M credit |

## Bibliographic discovery leads

- Walter L. Smith, "Renewal theory and its ramifications", *Journal of the Royal Statistical
  Society, Series B* 20 (1958), 243-302, is a candidate historical source associated with Smith's
  renewal results. The exact theorem number, pages, statement, relation to the name "key renewal
  theorem", and correction history have not been inspected or accepted here.
- William Feller, *An Introduction to Probability Theory and Its Applications*, Volume II,
  Chapter XI, is a candidate standard exposition. Edition, printing, exact section/theorem/page,
  hypotheses, conventions, and errata remain to be pinned.

These are discovery leads, not immutable evidence receipts and not `H0` evidence. In particular,
the repository's 1954 date is not reconciled by this intake.

## Candidate statement crosswalk

| Candidate mathematical component | Required formal surface | Open fidelity question |
|---|---|---|
| Interarrival distribution `F` | probability measure on a selected time/additive space | nonnegative support, properness, and arithmetic type |
| Renewal measure `U = sum F^{*n}` | convolution powers and a locally finite measure or integral interface | inclusion of `n = 0`, convergence, measurability, and local finiteness |
| Finite positive mean `mu` | integrability of the identity and a proved value `0 < mu < infinity` | exact source assumptions and extended-real coercions |
| Direct Riemann integrability of `z` | a precise predicate connected to measurable/Lebesgue integration | source definition, signed functions, and sufficient variants |
| Renewal convolution | an integral of the translated test function against `U` | integration interval, sign convention, and boundary mass |
| Asymptotic formula | a limit at infinity equal to `(1/mu) * integral z` | real versus lattice time and normalization |

## Gate boundary

The source audit must acquire immutable copies, identify an exact theorem and page range, transcribe
all assumptions and definitions, check errata, reconcile the attribution/date, and obtain
independent mathematical review. Only then may the statement phase map ordered binders and an exact
Lean expression to the human claim. Repo-local mathlib and external Lean candidates must be audited
separately by exact declaration type and revision. No `H0`, formal anchor, or theorem proof is
claimed at intake.
